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

@pytest.fixture
def chat_providers(server,tmp_path,monkeypatch):
 module,client,sign_in=server;sign_in('staff')
 config=tmp_path/'libraries.json';config.write_text(json.dumps({'Marketing':'marketing-drive','Company-Shared':'shared-drive'}))
 monkeypatch.setenv('LIBRARY_CONFIG',str(config))
 monkeypatch.setattr(module,'token',lambda:'delegated-test-token')
 seen=[]
 def fake_graph(path,access,**kwargs):
  assert access=='delegated-test-token';seen.append(path)
  if '/root/search' in path:
   if 'shared-drive' in path: return {'value':[]}
   return {'value':[{'id':'example-item','name':'policy.txt','file':{},'size':40}]}
  return {'id':'example-item','name':'policy.txt','webUrl':'https://philexcelbusinesspark.sharepoint.com/sites/PhilexcelHUB/Marketing/policy.txt',
   '@microsoft.graph.downloadUrl':'https://philexcelbusinesspark.sharepoint.com/download/example'}
 monkeypatch.setattr(module,'graph',fake_graph)
 class Download:
  status_code=200
  def __enter__(self): return self
  def __exit__(self,*args): pass
  def raise_for_status(self): pass
  def iter_content(self,size): yield b'The document says: use the approved logo.'
 def download(url,**kwargs):
  assert 'Authorization' not in kwargs.get('headers',{})
  assert kwargs['allow_redirects'] is False
  return Download()
 monkeypatch.setattr(module.requests,'get',download)
 class Generated:
  def raise_for_status(self): pass
  def json(self): return {'candidates':[{'content':{'parts':[{'text':'Use the approved logo. [1]'}]}}]}
 calls=[]
 def generate(url,**kwargs): calls.append(kwargs);return Generated()
 monkeypatch.setattr(module.requests,'post',generate)
 return module,client,seen,calls

def test_document_answer_is_scoped_and_cited(chat_providers):
 module,client,seen,calls=chat_providers
 r=client.post('/api/chat',base_url='https://localhost',headers={'X-CSRF-Token':'test-csrf'},json={'question':'logo','library':'Marketing'})
 assert r.status_code==200 and r.json['answer']=='Use the approved logo. [1]'
 assert r.json['sources']==[{'title':'policy.txt','url':'https://philexcelbusinesspark.sharepoint.com/sites/PhilexcelHUB/Marketing/policy.txt'}]
 assert len(calls)==1
 assert len([x for x in seen if '/items/' in x])==3 # fetch plus checks before and after generation
 assert all('Executive' not in x and 'Board' not in x for x in seen)
 assert 'use the approved logo' in calls[0]['json']['contents'][0]['parts'][0]['text']

def test_access_revoked_during_generation_discards_answer(chat_providers,monkeypatch):
 module,client,seen,calls=chat_providers
 original=module.requests.post
 def generate_then_disable(*args,**kwargs):
  result=original(*args,**kwargs)
  module.access_store.set('admin','staff',{'ai_enabled':False,'ai_level':'department','ai_departments':[]})
  return result
 monkeypatch.setattr(module.requests,'post',generate_then_disable)
 r=client.post('/api/chat',base_url='https://localhost',headers={'X-CSRF-Token':'test-csrf'},json={'question':'logo','library':'Marketing'})
 assert r.status_code==403
 assert 'approved logo' not in r.text and 'sources' not in r.json

def test_unrecognized_source_never_reaches_gemini(chat_providers,monkeypatch):
 module,client,seen,calls=chat_providers
 original=module.graph
 def graph_with_board_item(path,*args,**kwargs):
  result=original(path,*args,**kwargs)
  if '/items/' in path: result['webUrl']='https://philexcelbusinesspark.sharepoint.com/sites/PhilexcelExecutiveBoard/secret.txt'
  return result
 monkeypatch.setattr(module,'graph',graph_with_board_item)
 r=client.post('/api/chat',base_url='https://localhost',headers={'X-CSRF-Token':'test-csrf'},json={'question':'logo','library':'Marketing'})
 assert r.status_code==200 and r.json['sources']==[] and calls==[]

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
