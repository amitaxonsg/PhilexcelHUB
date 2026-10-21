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
 'ACCESS_DATABASE':str(tmp_path/'access.sqlite'),'GEMINI_API_KEY':'fake-test-key','GEMINI_MODEL':'test-model'}.items():
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
