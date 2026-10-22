import importlib, json, sys
import pytest

@pytest.fixture
def server(tmp_path, monkeypatch):
 staff={'staff':{'enabled':True,'nas_username':'Example','departments':['Marketing'],'ai_enabled':True,'roles':[]},
 'admin':{'enabled':True,'departments':[],'roles':['admin']}}
 private=tmp_path/'staff.json';private.write_text(json.dumps(staff))
 for key,value in {'SESSION_SECRET':'test-only-random-session-secret','SESSION_DIRECTORY':str(tmp_path/'sessions'),
 'RATE_LIMIT_STORAGE_URI':'memory://','PORTAL_HOSTS':'localhost','ENTRA_TENANT_ID':'test-tenant',
 'ENTRA_CLIENT_ID':'test-client','ENTRA_CLIENT_SECRET':'test-secret','STAFF_CONFIG':str(private),
 'ACCESS_DATABASE':str(tmp_path/'access.sqlite')}.items():
  monkeypatch.setenv(key,value)
 sys.modules.pop('app',None)
 module=importlib.import_module('app');module.app.config['TESTING']=True
 client=module.app.test_client()
 def sign_in(oid):
  with client.session_transaction(base_url='https://localhost') as s:
   s['oid']=oid;s['name']='Example';s['csrf']='test-csrf'
 return module,client,sign_in

def test_no_anonymous_chat(server):
 module,client,_=server
 assert client.post('/api/chat',base_url='https://localhost',json={}).status_code==403

def test_expired_blocks_before_providers(server,monkeypatch):
 module,client,sign_in=server;sign_in('staff')
 monkeypatch.setattr(module,'trial_state',lambda:{'expired':True})
 monkeypatch.setattr(module,'token',lambda:pytest.fail('Token/provider must not be touched'))
 r=client.post('/api/chat',base_url='https://localhost',headers={'X-CSRF-Token':'test-csrf'},json={'question':'policy','library':'Marketing'})
 assert r.status_code==403 and r.json['code']=='TRIAL_EXPIRED'

def test_out_of_scope_no_retrieval(server,monkeypatch):
 module,client,sign_in=server;sign_in('staff')
 monkeypatch.setattr(module,'token',lambda:pytest.fail('Restricted retrieval attempted'))
 r=client.post('/api/chat',base_url='https://localhost',headers={'X-CSRF-Token':'test-csrf'},json={'question':'finance payroll','library':'Marketing'})
 assert r.status_code==200 and 'Finance-Purchasing' in r.json['answer']
 r=client.post('/api/chat',base_url='https://localhost',headers={'X-CSRF-Token':'test-csrf'},json={'question':'policy','library':'Executive'})
 assert r.status_code==403

def test_admin_control_and_immediate_disable(server):
 module,client,sign_in=server;sign_in('staff')
 data={'csrf':'test-csrf','oid':'staff','ai_enabled':'yes','level':'executive','confirm_executive':'yes'}
 assert client.post('/admin/ai-access',base_url='https://localhost',data=data).status_code==403
 sign_in('admin')
 assert client.get('/admin',base_url='https://localhost').status_code==200
 assert client.post('/admin/ai-access',base_url='https://localhost',data=data).status_code==302
 assert len(module.access_store.get('staff')['ai_departments'])==0
 assert module.access_store.get('staff')['ai_level']=='executive'
 data={'csrf':'test-csrf','oid':'staff','level':'department'}
 assert client.post('/admin/ai-access',base_url='https://localhost',data=data).status_code==302
 sign_in('staff')
 assert client.get('/api/me',base_url='https://localhost').json['ai_libraries']==[]
 assert client.get('/ai',base_url='https://localhost').status_code==200

def test_user_cannot_read_admin_or_axon_pages(server):
 _,client,sign_in=server;sign_in('staff')
 for path in ['/admin','/axon']:
  assert client.get(path,base_url='https://localhost').status_code==403

def test_admin_save_needs_csrf_and_executive_confirmation(server):
 module,client,sign_in=server;sign_in('admin')
 data={'oid':'staff','level':'executive','ai_enabled':'yes'}
 assert client.post('/admin/ai-access',base_url='https://localhost',data=data).status_code==403
 data['csrf']='test-csrf'
 assert client.post('/admin/ai-access',base_url='https://localhost',data=data).status_code==400
 assert module.access_store.recent_audit()==[]
 data['confirm_executive']='yes'
 assert client.post('/admin/ai-access',base_url='https://localhost',data=data).status_code==302
 audit=module.access_store.recent_audit()
 assert len(audit)==1 and audit[0]['actor']=='admin' and audit[0]['target']=='staff'
 assert audit[0]['after']['ai_level']=='executive'
 assert client.get('/admin',base_url='https://localhost').status_code==200

def test_enrollment_download_requires_gate_and_contains_only_approved_shares(server,monkeypatch):
 _,client,sign_in=server;sign_in('staff');monkeypatch.setenv('NAS_HOST','nas.example.invalid')
 assert client.get('/download/windows',base_url='https://localhost').status_code==403
 with client.session_transaction(base_url='https://localhost') as s: s['gate_enroll']=True
 r=client.get('/download/windows',base_url='https://localhost')
 assert r.status_code==200
 assert "Share='Marketing'; Letter='M'" in r.text and "Share='CompanyShared'; Letter='Z'" in r.text
 assert "Share='Executive'" not in r.text and '__MAPS__' not in r.text
 r=client.get('/download/mac',base_url='https://localhost')
 assert r.status_code==200 and 'SHARES=("Marketing" "CompanyShared")' in r.text

def test_provider_payload_and_secrets_not_returned(server,monkeypatch):
 module,client,sign_in=server;sign_in('staff')
 monkeypatch.setattr(module,'trial_state',lambda:{'expired':False})
 def fail(): raise RuntimeError('provider payload SECRET-EXAMPLE')
 monkeypatch.setattr(module,'person',fail)
 r=client.get('/api/me',base_url='https://localhost')
 assert r.status_code==502 and 'SECRET-EXAMPLE' not in r.text

def test_copilot_setup_fails_closed_without_provider_or_file_calls(server,monkeypatch):
 module,client,sign_in=server;sign_in('staff')
 monkeypatch.setattr(module,'trial_state',lambda:{'expired':False})
 monkeypatch.setattr(module,'token',lambda:pytest.fail('No document token before setup'))
 monkeypatch.setattr(module.requests,'post',lambda *a,**k:pytest.fail('No external model call'))
 r=client.post('/api/chat',base_url='https://localhost',headers={'X-CSRF-Token':'test-csrf'},json={'question':'policy','library':'Marketing'})
 assert r.status_code==503 and r.json['code']=='COPILOT_SETUP_REQUIRED' and r.json['sources']==[]
 page=client.get('/ai',base_url='https://localhost')
 assert page.status_code==200
 assert 'titleId=T_41918509-ad55-6c25-fb32-5c78e09bfeab' in page.text
 assert 'Open Linda in Microsoft 365' in page.text
 assert '<form id="chat">' not in page.text
 assert "not disabled by this portal" in page.text
 monkeypatch.setattr(module,'trial_state',lambda:{'expired':True})
 expired=client.get('/ai',base_url='https://localhost')
 assert 'Trial Expired' in expired.text
 assert 'titleId=T_41918509-ad55-6c25-fb32-5c78e09bfeab' not in expired.text
 monkeypatch.setattr(module,'trial_state',lambda:{'expired':False})
 module.access_store.set('admin','staff',{'ai_enabled':False})
 disabled=client.get('/ai',base_url='https://localhost')
 assert 'titleId=T_41918509-ad55-6c25-fb32-5c78e09bfeab' not in disabled.text

def test_certificate_credential_and_incomplete_config_fail_closed(server, tmp_path, monkeypatch):
 module,_,_=server
 cert=tmp_path/'public.pem';cert.write_text('public-test-certificate')
 key=tmp_path/'key.pem';key.write_text('private-test-key')
 monkeypatch.setenv('ENTRA_CERTIFICATE_PATH',str(cert))
 monkeypatch.setenv('ENTRA_PRIVATE_KEY_PATH',str(key))
 monkeypatch.setattr(module.msal,'ConfidentialClientApplication',lambda *args,**kwargs:kwargs)
 result=module.entra()
 assert result['client_credential']=={'private_key':'private-test-key','public_certificate':'public-test-certificate'}
 monkeypatch.delenv('ENTRA_PRIVATE_KEY_PATH')
 with pytest.raises(ValueError): module.entra()
