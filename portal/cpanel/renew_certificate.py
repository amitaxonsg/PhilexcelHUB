"""Renew only this app's certificate using proof of its existing private key.

No directory-wide/application permissions or administrator tokens are needed.
Default: rotate within 60 days of expiry. --check: authenticate only, no rotation.
--rotate-now: commissioning test; never use in cron.
"""
import argparse
import base64
from datetime import datetime, timedelta, timezone
import fcntl
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import uuid

import jwt
import msal
import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

PRIVATE = Path('/home/philexcel/.config/philexcel-hub')
OBJECT_ID = 'cda01cb8-a738-4336-9d46-e3eb32358c24'
CLIENT_ID = '1f4f941f-9eef-405b-9203-d6bac2dc0333'
TENANT_ID = 'c6e4f48c-aba5-42e6-a95b-b54205d7490f'

def atomic_json(path, value):
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.renew-')
    try:
        with os.fdopen(fd,'w') as file:
            json.dump(value,file,indent=2)
            file.flush(); os.fsync(file.fileno())
        os.replace(temporary,path)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)

def read_pair(key_path, cert_path):
    key=key_path.read_text(); public=cert_path.read_text()
    certificate=x509.load_pem_x509_certificate(public.encode())
    private=serialization.load_pem_private_key(key.encode(),password=None)
    if private.public_key().public_numbers()!=certificate.public_key().public_numbers():
        raise ValueError('Certificate/key mismatch')
    return key,public,certificate

def access_token(key, public):
    client=msal.ConfidentialClientApplication(CLIENT_ID,
        authority='https://login.microsoftonline.com/'+TENANT_ID,
        client_credential={'private_key':key,'public_certificate':public},timeout=20)
    result=client.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    if not result.get('access_token'):
        raise RuntimeError('Certificate authentication failed')
    return result['access_token']

def pop_token(key, now=None):
    now=int(time.time() if now is None else now)
    return jwt.encode({'aud':'00000002-0000-0000-c000-000000000000',
        'iss':OBJECT_ID,'nbf':now-30,'exp':now+570},key,algorithm='RS256')

def is_due(certificate, now=None):
    return certificate.not_valid_after_utc-(now or datetime.now(timezone.utc)) <= timedelta(days=60)

def prepare_pending():
    path=PRIVATE/'renewal-pending.json'
    if path.exists():
        pending=json.loads(path.read_text())
        # Paths always stay inside this private directory.
        for name in ('key','certificate'):
            candidate=Path(pending[name])
            if candidate.parent!=PRIVATE or not candidate.name.startswith('entra-rotation-'):
                raise ValueError('Invalid pending certificate path')
        return pending
    label='entra-rotation-'+uuid.uuid4().hex
    key_path=PRIVATE/(label+'-key.pem'); cert_path=PRIVATE/(label+'-certificate.pem')
    key=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    now=datetime.now(timezone.utc)
    subject=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Philexcel HUB Portals')])
    cert=(x509.CertificateBuilder().subject_name(subject).issuer_name(subject)
        .public_key(key.public_key()).serial_number(x509.random_serial_number())
        .not_valid_before(now-timedelta(minutes=5)).not_valid_after(now+timedelta(days=730))
        .add_extension(x509.BasicConstraints(ca=False,path_length=None),critical=True)
        .sign(key,hashes.SHA256()))
    with key_path.open('xb') as f:
        f.write(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    with cert_path.open('xb') as f: f.write(cert.public_bytes(serialization.Encoding.PEM))
    pending={'key':str(key_path),'certificate':str(cert_path),'created':now.isoformat()}
    atomic_json(path,pending)
    return pending

def rotate(config, old_key, old_public, token):
    pending=prepare_pending()
    new_key,new_public,cert=read_pair(Path(pending['key']),Path(pending['certificate']))
    if cert.not_valid_after_utc <= datetime.now(timezone.utc)+timedelta(days=60):
        raise ValueError('Pending certificate needs operator review')
    # A previous attempt may have registered the certificate before a crash.
    try:
        access_token(new_key,new_public)
        registered=True
    except RuntimeError:
        registered=False
    if not registered:
        response=requests.post('https://graph.microsoft.com/v1.0/applications/'+OBJECT_ID+'/addKey',
            headers={'Authorization':'Bearer '+token},timeout=30,allow_redirects=False,
            json={'keyCredential':{'type':'AsymmetricX509Cert','usage':'Verify',
                'displayName':'Philexcel automated rotation',
                'key':base64.b64encode(cert.public_bytes(serialization.Encoding.DER)).decode(),
                'startDateTime':cert.not_valid_before_utc.isoformat(),
                'endDateTime':cert.not_valid_after_utc.isoformat()},
                'passwordCredential':None,'proof':pop_token(old_key)})
        if response.status_code!=200:
            raise RuntimeError('Microsoft certificate registration failed; active configuration preserved')
        # Allow for directory propagation. Old certificate stays active meanwhile.
        for attempt in range(4):
            try:
                access_token(new_key,new_public)
                break
            except RuntimeError:
                if attempt==3: raise
                time.sleep(2)
    backup=PRIVATE/('environment-before-rotation-'+uuid.uuid4().hex+'.json')
    atomic_json(backup,config)
    config=dict(config,ENTRA_PRIVATE_KEY_PATH=pending['key'],ENTRA_CERTIFICATE_PATH=pending['certificate'])
    config.pop('ENTRA_CLIENT_SECRET',None)
    atomic_json(PRIVATE/'environment.json',config)
    (PRIVATE/'renewal-pending.json').unlink()
    return cert

def execute(check=False, rotate_now=False):
    config=json.loads((PRIVATE/'environment.json').read_text())
    if config.get('ENTRA_CLIENT_ID')!=CLIENT_ID or config.get('ENTRA_TENANT_ID')!=TENANT_ID:
        raise ValueError('Wrong portal identity')
    key,public,cert=read_pair(Path(config['ENTRA_PRIVATE_KEY_PATH']),Path(config['ENTRA_CERTIFICATE_PATH']))
    if cert.not_valid_after_utc<=datetime.now(timezone.utc):
        raise ValueError('Certificate expired; administrator recovery required')
    token=access_token(key,public)
    action='checked'
    if not check and (rotate_now or is_due(cert)):
        cert=rotate(config,key,public,token);action='rotated'
    status={'status':'ok','action':action,'checked_at':datetime.now(timezone.utc).isoformat(),
        'expires':cert.not_valid_after_utc.isoformat()}
    atomic_json(PRIVATE/'renewal-status.json',status)
    print(json.dumps(status))

def main():
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--check',action='store_true')
    group.add_argument('--rotate-now',action='store_true')
    args=parser.parse_args()
    os.umask(0o077)
    if os.geteuid()!=1164: raise ValueError('Run as philexcel UID 1164')
    with (PRIVATE/'renewal.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        execute(args.check,args.rotate_now)

if __name__=='__main__':
    try:
        main()
    except Exception as error:
        # Provider errors may contain assertions/tokens. Never print them.
        status={'status':'error','error_type':type(error).__name__,
            'checked_at':datetime.now(timezone.utc).isoformat()}
        try:
            if os.geteuid()==1164: atomic_json(PRIVATE/'renewal-status.json',status)
        except Exception: pass
        print(json.dumps(status),file=sys.stderr)
        sys.exit(1)
