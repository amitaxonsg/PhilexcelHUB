import importlib.util,json
from pathlib import Path
from datetime import datetime,timedelta,timezone
from types import SimpleNamespace
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
spec=importlib.util.spec_from_file_location('renew',Path(__file__).parents[1]/'cpanel/renew_certificate.py')
renew=importlib.util.module_from_spec(spec);spec.loader.exec_module(renew)
@pytest.fixture
def config(tmp_path,monkeypatch):
 monkeypatch.setattr(renew,'PRIVATE',tmp_path)
 key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
 name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'test')]);now=datetime.now(timezone.utc)
 cert=(x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(1)
  .not_valid_before(now-timedelta(minutes=5)).not_valid_after(now+timedelta(days=730)).sign(key,hashes.SHA256()))
 kp=tmp_path/'key.pem';cp=tmp_path/'cert.pem'
 kp.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
 cp.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
 cfg={'ENTRA_CLIENT_ID':renew.CLIENT_ID,'ENTRA_TENANT_ID':renew.TENANT_ID,'ENTRA_PRIVATE_KEY_PATH':str(kp),'ENTRA_CERTIFICATE_PATH':str(cp)}
 (tmp_path/'environment.json').write_text(json.dumps(cfg));return cfg,cert

def test_daily_check_and_due_boundary(config,monkeypatch):
 cfg,cert=config
 assert not renew.is_due(cert)
 assert renew.is_due(cert,cert.not_valid_after_utc-timedelta(days=60))
 monkeypatch.setattr(renew,'access_token',lambda *a:'token')
 monkeypatch.setattr(renew,'rotate',lambda *a:pytest.fail('Unexpected rotation'))
 renew.execute()
 assert json.loads((renew.PRIVATE/'renewal-status.json').read_text())['action']=='checked'

def test_failed_registration_preserves_config_and_pending_pair(config,monkeypatch):
 cfg,_=config;old=Path(cfg['ENTRA_PRIVATE_KEY_PATH']).read_text()
 def access(key,cert):
  if key==old:return 'token'
  raise RuntimeError('unregistered')
 monkeypatch.setattr(renew,'access_token',access)
 monkeypatch.setattr(renew.requests,'post',lambda *a,**kw:SimpleNamespace(status_code=403))
 with pytest.raises(RuntimeError):renew.execute(rotate_now=True)
 assert json.loads((renew.PRIVATE/'environment.json').read_text())==cfg
 pending=renew.prepare_pending();assert renew.prepare_pending()==pending

def test_success_switches_only_after_authentication(config,monkeypatch):
 cfg,_=config;old=Path(cfg['ENTRA_PRIVATE_KEY_PATH']).read_text();registered=[]
 def access(key,cert):
  if key!=old and not registered:raise RuntimeError('unregistered')
  return 'token'
 def post(url,**kw):
  assert url.endswith('/'+renew.OBJECT_ID+'/addKey')
  assert json.loads((renew.PRIVATE/'environment.json').read_text())==cfg
  registered.append(True);return SimpleNamespace(status_code=200)
 monkeypatch.setattr(renew,'access_token',access);monkeypatch.setattr(renew.requests,'post',post)
 renew.execute(rotate_now=True)
 assert json.loads((renew.PRIVATE/'environment.json').read_text())['ENTRA_PRIVATE_KEY_PATH']!=cfg['ENTRA_PRIVATE_KEY_PATH']
 assert Path(cfg['ENTRA_PRIVATE_KEY_PATH']).exists()
 assert not (renew.PRIVATE/'renewal-pending.json').exists()
