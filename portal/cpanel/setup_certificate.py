"""Run as philexcel; never prints the private key. No Microsoft API calls."""
import base64
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import tempfile
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

os.umask(0o077)
if os.geteuid() != 1164:
    raise SystemExit('STOP: Run as the verified philexcel account (UID 1164).')
private = Path('/home/philexcel/.config/philexcel-hub')
config_path = private/'environment.json'
config = json.loads(config_path.read_text())
key_path = private/'entra-key.pem'
cert_path = private/'entra-certificate.pem'
if key_path.exists() != cert_path.exists():
    raise SystemExit('STOP: Incomplete certificate pair. Existing files preserved.')
if not key_path.exists():
    key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    now = datetime.now(timezone.utc)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Philexcel HUB Portals')])
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
        .public_key(key.public_key()).serial_number(x509.random_serial_number())
        .not_valid_before(now-timedelta(minutes=5)).not_valid_after(now+timedelta(days=730))
        .add_extension(x509.BasicConstraints(ca=False,path_length=None),critical=True)
        .sign(key,hashes.SHA256()))
    with key_path.open('xb') as f:
        f.write(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    with cert_path.open('xb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
else:
    key=serialization.load_pem_private_key(key_path.read_bytes(),password=None)
    cert=x509.load_pem_x509_certificate(cert_path.read_bytes())
if key.public_key().public_numbers()!=cert.public_key().public_numbers():
    raise SystemExit('STOP: Certificate/key mismatch. Configuration preserved.')
if cert.not_valid_after_utc <= datetime.now(timezone.utc):
    raise SystemExit('STOP: Existing certificate expired. Rotate explicitly.')
for path in (key_path,cert_path): path.chmod(0o600)
config.update(ENTRA_TENANT_ID='c6e4f48c-aba5-42e6-a95b-b54205d7490f',
    ENTRA_CLIENT_ID='1f4f941f-9eef-405b-9203-d6bac2dc0333',
    ENTRA_PRIVATE_KEY_PATH=str(key_path),ENTRA_CERTIFICATE_PATH=str(cert_path))
config.pop('ENTRA_CLIENT_SECRET',None)
fd, temporary=tempfile.mkstemp(dir=private,prefix='.environment-')
try:
    with os.fdopen(fd,'w') as f: json.dump(config,f,indent=2)
    os.replace(temporary,config_path)
finally:
    if os.path.exists(temporary): os.unlink(temporary)
print('PASS: Private certificate authentication configured locally.')
print('Certificate renewal due (UTC):',cert.not_valid_after_utc.isoformat())
print('PUBLIC_CERTIFICATE_BASE64:')
print(base64.b64encode(cert.public_bytes(serialization.Encoding.DER)).decode())
print('END_PUBLIC_CERTIFICATE')
