"""Singapore-hosted portal. No public NAS endpoint or admin credentials required."""
import json, os, re, secrets, time
from datetime import timedelta
from functools import wraps
from pathlib import Path
from urllib.parse import quote, urlsplit
import msal, requests
from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for, Response
from flask_session import Session
from cachelib.file import FileSystemCache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash
from policy import DEPARTMENTS, allowed_libraries, allowed_source, trial_state, ai_libraries, restricted_department, RESTRICTION_MESSAGE
from access_store import AccessStore

BASE = Path(__file__).parent
app = Flask(__name__)
app.config.update(SECRET_KEY=os.environ['SESSION_SECRET'], SESSION_TYPE='cachelib',
 SESSION_CACHELIB=FileSystemCache(os.environ['SESSION_DIRECTORY'], threshold=1000, mode=0o600), SESSION_COOKIE_SECURE=True,
 SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',
 PERMANENT_SESSION_LIFETIME=timedelta(hours=1), MAX_CONTENT_LENGTH=16384,
 TRUSTED_HOSTS=os.environ['PORTAL_HOSTS'].split(','))
Session(app)
limiter = Limiter(key_func=get_remote_address, app=app,
 storage_uri=os.environ['RATE_LIMIT_STORAGE_URI'], default_limits=['120 per minute'],
 enabled=os.environ.get('CPANEL_PRIVATE_BRIDGE') != '1')
TENANT = os.environ['ENTRA_TENANT_ID']
SCOPES = ['User.Read', 'Files.Read.All']
SITE = 'https://philexcelbusinesspark.sharepoint.com/sites/PhilexcelHUB'
access_store = AccessStore(os.environ['ACCESS_DATABASE'])

def entra(cache=None):
 certificate=os.environ.get('ENTRA_CERTIFICATE_PATH')
 private_key=os.environ.get('ENTRA_PRIVATE_KEY_PATH')
 if certificate or private_key:
  if not certificate or not private_key:
   raise ValueError('Both certificate and private key paths are required')
  credential={'private_key':Path(private_key).read_text(),
   'public_certificate':Path(certificate).read_text()}
 else:
  credential=os.environ['ENTRA_CLIENT_SECRET']
 return msal.ConfidentialClientApplication(os.environ['ENTRA_CLIENT_ID'],
  authority='https://login.microsoftonline.com/'+TENANT,
  client_credential=credential, token_cache=cache)

def records():
 return json.loads(Path(os.environ['STAFF_CONFIG']).read_text())

def person():
 record=records().get(session.get('oid'), {}).copy()
 record.update(access_store.get(session.get('oid','')))
 return record

def protected(role=None):
 def decorate(fn):
  @wraps(fn)
  def wrapper(*a, **kw):
   if not session.get('oid'):
    if request.path.startswith('/api/') or request.path.startswith('/download/'):
     abort(401)
    return redirect(url_for('login'))
   p = person()
   if not p.get('enabled'): abort(403, 'Your access is awaiting administrator confirmation.')
   if role and role not in p.get('roles', []): abort(403)
   return fn(*a, **kw)
  return wrapper
 return decorate

@app.before_request
def csrf_check():
 if request.method == 'POST':
  token = request.headers.get('X-CSRF-Token') or request.form.get('csrf', '')
  if not session.get('csrf') or not secrets.compare_digest(token, session['csrf']): abort(403)

@app.after_request
def secure_headers(r):
 r.headers['Cache-Control']='no-store'
 r.headers['X-Content-Type-Options']='nosniff'
 r.headers['Referrer-Policy']='no-referrer'
 r.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
 return r

@app.get('/login')
def login():
 session.clear()
 session.permanent=True
 session['csrf']=secrets.token_urlsafe(32)
 session['flow']=entra().initiate_auth_code_flow(SCOPES,
  redirect_uri='https://'+request.host+'/auth/callback', prompt='select_account')
 return redirect(session['flow']['auth_uri'])

@app.get('/auth/callback')
def callback():
 cache=msal.SerializableTokenCache()
 try:
  result=entra(cache).acquire_token_by_auth_code_flow(session.pop('flow'), request.args)
 except (ValueError, KeyError): abort(400, 'Sign-in expired. Please sign in again.')
 claims=result.get('id_token_claims', {})
 if claims.get('tid', '').lower()!=TENANT.lower() or not claims.get('oid'): abort(403)
 session['oid']=claims['oid']
 session['name']=claims.get('name', 'Staff member')
 if request.host.split('.')[0]=='enroll':
  access=result.get('access_token')
  if not access: abort(403, 'Microsoft profile verification is unavailable. Use the manual setup guide.')
  profile=graph('/me?$select=id,displayName,userPrincipalName,mail,department,userType',access)
  if profile.get('id')!=claims['oid'] or profile.get('userType')!='Member':
   abort(403, 'Enrollment sign-in is for Philexcel organisation members. Use the manual setup guide if you have an approved NAS account.')
  session['enroll_member']=True
  session['enroll_profile']={key:profile.get(key,'') for key in ('displayName','userPrincipalName','mail','department')}
 session['cache']=cache.serialize()
 session['csrf']=secrets.token_urlsafe(32)
 app.session_interface.regenerate(session)
 return redirect(url_for('home'))

@app.post('/logout')
def logout():
 session.clear()
 return redirect(url_for('home'))

def token():
 cache=msal.SerializableTokenCache(); cache.deserialize(session['cache'])
 client=entra(cache); accounts=client.get_accounts()
 if not accounts: abort(401)
 result=client.acquire_token_silent(SCOPES, account=accounts[0])
 session['cache']=cache.serialize()
 if not result or 'access_token' not in result: abort(401)
 return result['access_token']

def graph(path, access, method='GET', payload=None):
 # Only fixed Graph API paths; never follow a user-supplied URL with bearer token.
 r=requests.request(method, 'https://graph.microsoft.com/v1.0'+path,
  headers={'Authorization':'Bearer '+access}, json=payload, timeout=25,
  allow_redirects=False)
 if r.status_code in (401,403): abort(403, 'Microsoft 365 file access is not available for this account.')
 r.raise_for_status(); return r.json()

@app.get('/')
def home():
 mode={'enroll':'enroll','axon':'axon','admin':'admin'}.get(request.host.split('.')[0], 'ai')
 return redirect('/'+mode)

def enrollment_view():
 # Only a server-managed NAS register supplies eligibility. Directory department
 # and form fields never grant NAS or SharePoint rights.
 p=records().get(session.get('oid'),{}).copy()
 approved=bool(p.get('enabled') and re.fullmatch(r'[A-Za-z0-9._-]+',p.get('nas_username','')) and
               p.get('departments') and set(p['departments']).issubset(DEPARTMENTS))
 libraries=(sorted(set(DEPARTMENTS)|{'Company-Shared'}) if p.get('nas_access_level')=='executive' else allowed_libraries(p)) if approved else []
 plan=[{'library':name,'share':DEPARTMENTS[name][0],'letter':DEPARTMENTS[name][1]} for name in libraries if name in DEPARTMENTS]
 if approved: plan.append({'library':'Company Shared','share':'CompanyShared','letter':'Z'})
 return p,approved,plan

@app.get('/enroll')
def enrollment():
 # Public instructions contain no staff register, credentials or entitlement data.
 # The Singapore host cannot attest a visitor's private LAN membership.
 session.setdefault('csrf', secrets.token_urlsafe(32))
 return render_template('enroll.html', csrf=session['csrf'])

@app.get('/enroll/installer')
@limiter.limit('30 per minute')
def enrollment_installer():
 # Serve the administrator-selected, account-local AXON UAT v5.6 release.
 # Never fall back to a different installer if the selected file is unavailable.
 # Access to this public endpoint does not establish NAS access rights.
 filename = 'Philexcel-NAS-Setup-Repair-UAT-v5.6-AXON.bat'
 installer = Path('/home/philexcel') / filename
 if not installer.is_file() or not installer.stat().st_size:
  abort(503, 'The approved Windows installer is temporarily unavailable. Contact AXON support.')
 response = Response(installer.read_bytes(), mimetype='application/octet-stream',
  headers={'Content-Disposition': 'attachment; filename=' + filename,
           'X-Content-Type-Options': 'nosniff'})
 response.headers['Content-Length'] = str(installer.stat().st_size)
 return response

@app.get('/enroll/manual')
def enrollment_manual():
 session.setdefault('csrf',secrets.token_urlsafe(32))
 return render_template('enroll_manual.html',csrf=session['csrf'],nas=os.environ.get('NAS_HOST',''),departments=DEPARTMENTS)

@app.get('/enroll/check/<platform>')
def enrollment_check(platform):
 files={'windows':'Check-Drives-Windows.ps1','mac':'Check-Drives-Mac.command'}
 if platform not in files: abort(404)
 filename=files[platform]
 return Response((BASE/'downloads'/filename).read_text(),mimetype='text/plain',
  headers={'Content-Disposition':'attachment; filename='+filename})

@app.route('/<mode>', methods=['GET','POST'])
@protected()
def portal(mode):
 if mode not in ('ai','admin','axon','data'): abort(404)
 p=person()
 if mode in ('admin','axon') and mode not in p.get('roles', []): abort(403)
 gate={'enroll':'ENROLL_GATE_HASH','axon':'AXON_GATE_HASH','data':'DATA_GATE_HASH'}.get(mode)
 if gate and not session.get('gate_'+mode):
  if request.method=='POST':
   check_gate(mode, gate)
   session['gate_'+mode]=True
   return redirect('/'+mode)
  return render_template('gate.html', mode=mode, csrf=session['csrf'])
 if mode=='data': return redirect('https://data.philexcel.com')
 return render_template('portal.html', mode=mode, person=p, name=session['name'],
  libraries=ai_libraries(p) if mode=='ai' else allowed_libraries(p), trial=trial_state(), csrf=session['csrf'],
  audit=access_store.recent_audit() if mode in ('admin','axon') else [],
  departments=list(DEPARTMENTS), staff=[dict(record, oid=oid) for oid,record in records().items()] if mode=='admin' else [],
  ai_settings={oid: {**record, **access_store.get(oid)} for oid,record in records().items()} if mode=='admin' else {},
  nas=os.environ.get('NAS_HOST',''), connected=False)

@limiter.limit('5 per minute')
def check_gate(mode, key):
 hashed=os.environ.get(key)
 if not hashed or not check_password_hash(hashed, request.form.get('password','')): abort(403, 'Entry password is incorrect.')

@app.post('/admin/ai-access')
@protected('admin')
def save_ai_access():
 oid=request.form.get('oid','')
 if oid not in records(): abort(400)
 scopes=request.form.getlist('departments')
 if not set(scopes).issubset(DEPARTMENTS): abort(400)
 level=request.form.get('level','department')
 if level not in ('department','executive'): abort(400)
 if level=='executive' and request.form.get('confirm_executive')!='yes':
  abort(400,'Please confirm approval for all-department Executive AI access.')
 value={'ai_enabled':request.form.get('ai_enabled')=='yes','ai_level':level,'ai_departments':scopes}
 access_store.set(session['oid'],oid,value)
 return redirect('/admin')

@app.get('/api/me')
@protected()
def me():
 return jsonify(name=session['name'], libraries=allowed_libraries(person()), ai_libraries=ai_libraries(person()), trial=trial_state())

@app.get('/download/<platform>')
def download(platform):
 if not session.get('oid'): abort(401)
 if not session.get('enroll_member'): abort(403)
 p,approved,plan=enrollment_view()
 if not approved: abort(403, 'Your NAS account and department need administrator confirmation. Use the manual setup guide.')
 return setup_download(platform,p)

@app.post('/enroll/manual/download')
@limiter.limit('10 per minute')
def manual_setup_download():
 # Self-entered values customise a helper, never an access grant or staff record.
 department=request.form.get('department','')
 name=request.form.get('name','').strip()
 if request.form.get('confirmed')!='yes' or department not in DEPARTMENTS or not 1<=len(name)<=100: abort(400)
 p={'enabled':True,'departments':[department],'nas_username':request.form.get('nas_username','')}
 return setup_download(request.form.get('platform',''),p,manual=True)

def setup_download(platform,p,manual=False):
 nas=os.environ.get('NAS_HOST', '')
 if not re.fullmatch(r'[A-Za-z0-9.-]+', nas): abort(503, 'NAS address is not configured.')
 user=p.get('nas_username', '')
 if not re.fullmatch(r'[A-Za-z0-9._-]+', user): abort(503, 'Your NAS account needs confirmation.')
 scopes=sorted(DEPARTMENTS) if p.get('nas_access_level')=='executive' else allowed_libraries(p)
 selected=[DEPARTMENTS[x] for x in scopes if x in DEPARTMENTS]+[('CompanyShared','Z')]
 if platform=='windows':
  body=(BASE/'downloads/Enroll-Windows.ps1').read_text().replace('__NAS__',nas).replace('__USER__',user)
  body=body.replace('__MAPS__', '\n'.join("    @{Share='%s'; Letter='%s'}" % pair for pair in selected))
  filename='Philexcel-Windows-Setup.ps1'
 elif platform=='mac':
  body=(BASE/'downloads/Enroll-Mac.command').read_text().replace('__NAS__',nas).replace('__USER__',user)
  body=body.replace('__SHARES__', ' '.join('"'+x[0]+'"' for x in selected)); filename='Philexcel-Mac-Setup.command'
 else: abort(404)
 if manual:
  notice='# Manual helper: department is self-declared, not verified. NAS permissions decide access.\n'
  body=body.replace('#!/bin/bash\n','#!/bin/bash\n'+notice,1) if platform=='mac' else notice+body
 # Never embed portal gates, cloud tokens or a NAS password in downloads.
 return Response(body, mimetype='text/plain', headers={'Content-Disposition':'attachment; filename='+filename})

@app.post('/api/chat')
@protected()
@limiter.limit('10 per minute')
def chat():
 if trial_state()['expired']: return jsonify(code='TRIAL_EXPIRED', answer='Trial Expired'),403
 body=request.get_json() or {}
 if not isinstance(body,dict): abort(400)
 question=body.get('question',''); library=body.get('library','')
 if not isinstance(body,dict): abort(400)
 if not isinstance(question,str) or not isinstance(library,str) or not 1 <= len(question.strip()) <= 1000: abort(400)
 scopes=ai_libraries(person())
 if not scopes: return jsonify(answer='Linda is not enabled for your account. Please contact your administrator.'),403
 if library=='All departments' and person().get('ai_level')=='executive':
  selected_scopes=scopes
 elif library in scopes:
  selected_scopes=sorted({library,'Company-Shared'})
 else: return jsonify(answer=RESTRICTION_MESSAGE),403
 restricted=restricted_department(question, scopes)
 if restricted: return jsonify(answer='Your question may relate to '+restricted+'. '+RESTRICTION_MESSAGE, sources=[]) 
 # Require an approved Microsoft integration using the signed-in staff identity.
 # A central mailbox owns the agent; it is not a shared document-access session.
 return jsonify(code='COPILOT_SETUP_REQUIRED',
  answer='Linda is being connected to Microsoft Copilot. Please use your company files while setup is completed.',sources=[]),503

@app.errorhandler(Exception)
def error(e):
 from werkzeug.exceptions import HTTPException
 if isinstance(e,HTTPException):
  if request.path.startswith('/api/'): return jsonify(answer=e.description),e.code
  return render_template('error.html',message=e.description),e.code
 # No provider payloads, tokens, API keys or document excerpts in errors/logs.
 return jsonify(answer='The service could not complete this request. Please contact Axon support.'),502

