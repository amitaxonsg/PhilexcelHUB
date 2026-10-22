import pytest
import json
from test_app import server

BASE='https://localhost'

def member(client,oid='staff'):
 with client.session_transaction(base_url=BASE) as s:
  s['oid']=oid;s['name']='Example';s['csrf']='test-csrf';s['enroll_member']=True
  s['enroll_profile']={'displayName':'Verified Staff','mail':'staff@example.invalid'}

def test_public_guides_and_read_only_checks(server):
 _,client,_=server
 assert 'Set up or repair your office network drives' in client.get('/enroll',base_url=BASE).text
 landing=client.get('/enroll',base_url=BASE).text
 assert 'Office NAS connectivity check' in landing
 assert 'automatically checks whether' in landing
 assert 'NAS connection not verified' not in landing
 assert 'outside the office network' not in landing
 assert 'href="/enroll/installer"' in landing
 assert 'Manual setup (advanced)' in landing
 # The selected installer is account-local, not part of the Git checkout.
 # On the cPanel server it exists (200); on CI it may be absent (503).
 from pathlib import Path
 selected=Path('/home/philexcel/Philexcel-NAS-Setup-Repair-UAT-v5.7-DSM-Access-Sync.bat')
 r=client.get('/enroll/installer',base_url=BASE)
 if selected.is_file() and selected.stat().st_size:
  assert r.status_code==200
  assert r.headers['Content-Disposition'].endswith('Philexcel-NAS-Setup-Repair-UAT-v5.7-DSM-Access-Sync.bat')
  assert r.data==selected.read_bytes()
 else:
  assert r.status_code==503
  assert b'approved Windows installer is temporarily unavailable' in r.data
 assert 'not verified eligibility' in client.get('/enroll/manual',base_url=BASE).text
 for platform in ('windows','mac'):
  r=client.get('/enroll/check/'+platform,base_url=BASE)
  assert r.status_code==200 and 'attachment;' in r.headers['Content-Disposition']
 assert client.get('/download/windows',base_url=BASE).status_code==401

def test_unknown_member_can_enroll_but_has_no_eligible_drives(server):
 _,client,_=server;member(client,'unknown')
 r=client.get('/enroll',base_url=BASE)
 assert r.status_code==200 and 'Manual setup' in r.text and 'Verified Staff' not in r.text
 assert '/download/windows' not in r.text
 assert client.get('/download/windows',base_url=BASE).status_code==403
 for path in ('/admin','/axon','/ai'):
  assert client.get(path,base_url=BASE).status_code==403

def test_confirmed_member_plan_comes_from_server_not_query(server,monkeypatch):
 _,client,_=server;member(client);monkeypatch.setenv('NAS_HOST','nas.example.invalid')
 r=client.get('/enroll?department=Executive',base_url=BASE)
 assert r.status_code==200 and 'CompanyShared' in r.text and 'Your NAS username' not in r.text
 r=client.get('/download/windows?department=Executive',base_url=BASE)
 assert "Share='Marketing'" in r.text and "Share='Executive'" not in r.text
 assert 'Type MAP' in r.text and 'Remove-SmbMapping -LocalPath *' not in r.text


def test_disabled_registration_has_no_download(server,monkeypatch):
 module,client,_=server;member(client)
 monkeypatch.setattr(module,'records',lambda:{'staff':{'enabled':False,'nas_username':'Example','departments':['Marketing']}})
 assert client.get('/download/mac',base_url=BASE).status_code==403


def test_executive_mapping_is_explicit_server_record(server,monkeypatch):
 module,client,_=server;member(client);monkeypatch.setenv('NAS_HOST','nas.example.invalid')
 monkeypatch.setattr(module,'records',lambda:{'staff':{'enabled':True,'nas_username':'Ian','departments':['Executive'],'nas_access_level':'executive'}})
 r=client.get('/download/windows',base_url=BASE)
 assert r.status_code==200 and r.text.count("@{Share=")==7


def test_manual_helper_requires_confirmation_and_csrf_without_grant(server,monkeypatch):
 module,client,_=server;monkeypatch.setenv('NAS_HOST','nas.example.invalid')
 client.get('/enroll/manual',base_url=BASE)
 with client.session_transaction(base_url=BASE) as s: csrf=s['csrf']
 data={'name':'Staff','nas_username':'Tess','department':'Administration-HR','platform':'windows','confirmed':'yes'}
 assert client.post('/enroll/manual/download',base_url=BASE,data=data).status_code==403
 data['csrf']=csrf
 r=client.post('/enroll/manual/download',base_url=BASE,data=data)
 assert r.status_code==200 and 'self-declared, not verified' in r.text
 assert "Share='AdminHR'" in r.text and "Share='Executive'" not in r.text
 assert module.records().get('Tess') is None
 data['nas_username']="Tess';whoami"
 assert client.post('/enroll/manual/download',base_url=BASE,data=data).status_code!=200


def test_enroll_callback_rejects_guest_or_mismatched_profile(server,monkeypatch):
 module,client,_=server
 module.app.config['TRUSTED_HOSTS']=['enroll.localhost']
 class Auth:
  def acquire_token_by_auth_code_flow(self,*args):
   return {'id_token_claims':{'tid':'test-tenant','oid':'staff'},'access_token':'test-token'}
 monkeypatch.setattr(module,'entra',lambda cache=None:Auth())
 for profile in ({'id':'staff','userType':'Guest'},{'id':'someone-else','userType':'Member'}):
  with client.session_transaction(base_url='https://enroll.localhost') as s: s['flow']={}
  monkeypatch.setattr(module,'graph',lambda *args,profile=profile:profile)
  assert client.get('/auth/callback',base_url='https://enroll.localhost').status_code==403
  assert client.get('/download/windows',base_url='https://enroll.localhost').status_code==403

def test_valid_unregistered_tenant_member_can_finish_sign_in(server,monkeypatch):
 module,client,_=server
 module.app.config['TRUSTED_HOSTS']=['enroll.localhost']
 class Auth:
  def acquire_token_by_auth_code_flow(self,*args):
   return {'id_token_claims':{'tid':'test-tenant','oid':'new-member','name':'New Staff'},'access_token':'test-token'}
 monkeypatch.setattr(module,'entra',lambda cache=None:Auth())
 monkeypatch.setattr(module,'graph',lambda *args:{'id':'new-member','userType':'Member','displayName':'New Staff','mail':'new@example.invalid'})
 with client.session_transaction(base_url='https://enroll.localhost') as s: s['flow']={}
 assert client.get('/auth/callback',base_url='https://enroll.localhost').status_code==302
 r=client.get('/enroll',base_url='https://enroll.localhost')
 assert r.status_code==200 and 'Download Windows Setup' in r.text and 'New Staff' not in r.text

def test_callback_rejects_other_tenant_before_profile_lookup(server,monkeypatch):
 module,client,_=server
 class Auth:
  def acquire_token_by_auth_code_flow(self,*args):
   return {'id_token_claims':{'tid':'other-tenant','oid':'staff'},'access_token':'test-token'}
 monkeypatch.setattr(module,'entra',lambda cache=None:Auth())
 monkeypatch.setattr(module,'graph',lambda *args:pytest.fail('Wrong tenant must not query profile'))
 with client.session_transaction(base_url=BASE) as s: s['flow']={}
 assert client.get('/auth/callback',base_url=BASE).status_code==403
