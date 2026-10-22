"""Merge an administrator-verified register into account-private staff.json.
Run as philexcel; JSON arrives on stdin, never through a web endpoint.
"""
import fcntl
import json
import os
from pathlib import Path
import pwd
import re
import secrets
import sys
import tempfile
from uuid import UUID
from datetime import datetime, timezone

DEPARTMENTS={'Executive','Administration-HR','Marketing','Administration-Marketing','Finance-Purchasing','Engineering'}

def merge_records(existing, incoming):
    if not isinstance(existing,dict) or not isinstance(incoming,list) or not incoming:
        raise ValueError('Expected existing object and nonempty verified record array')
    result={key:dict(value) for key,value in existing.items()}
    seen=set(); nas_seen=set()
    for item in incoming:
        oid=str(UUID(item['object_id']))
        nas=item['nas_username']; departments=item['departments']
        if oid in seen or nas.lower() in nas_seen:
            raise ValueError('Duplicate identity or NAS login in import')
        if not re.fullmatch(r'[A-Za-z0-9._-]{1,64}',nas):
            raise ValueError('Invalid NAS login')
        if not isinstance(departments,list) or not departments or not set(departments)<=DEPARTMENTS:
            raise ValueError('Invalid department')
        if item.get('nas_access_level','department') not in ('department','executive'):
            raise ValueError('Invalid NAS access level')
        if item.get('enabled') is not True or not item.get('user_principal_name'):
            raise ValueError('Import requires a verified enabled Microsoft member')
        old=result.get(oid,{})
        if old.get('enabled') is False:
            raise ValueError('Existing disabled account requires separate administrator review')
        if any(key!=oid and value.get('nas_username','').lower()==nas.lower() for key,value in result.items()):
            raise ValueError('NAS login already linked to another object ID')
        updated=dict(old)
        for key in ('nas_username','departments','display_name','user_principal_name','mail','nas_access_level'):
            if key in item: updated[key]=item[key]
        updated['enabled']=True
        updated.setdefault('roles',[])
        updated.setdefault('ai_enabled',False)
        result[oid]=updated;seen.add(oid);nas_seen.add(nas.lower())
    return result

def main():
    if pwd.getpwuid(os.geteuid()).pw_name!='philexcel':
        raise SystemExit('STOP: run as the philexcel account')
    private=Path('/home/philexcel/.config/philexcel-hub')
    config=json.loads((private/'environment.json').read_text())
    configured=Path(config['STAFF_CONFIG'])
    path=configured.resolve()
    if path.parent!=private.resolve() or configured.is_symlink():
        raise SystemExit('STOP: staff register must be inside the private configuration directory')
    incoming=json.loads(sys.stdin.read(1048577))
    with (private/'enrollment-import.lock').open('a') as lock:
        os.chmod(lock.name,0o600)
        fcntl.flock(lock,fcntl.LOCK_EX)
        original=path.read_bytes()
        result=merge_records(json.loads(original),incoming)
        backup=private/('staff-before-enrollment-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+secrets.token_hex(3)+'.json')
        with backup.open('xb') as file:
            os.chmod(backup,0o600);file.write(original)
        fd,temporary=tempfile.mkstemp(dir=private,prefix='.staff-import-')
        try:
            os.fchmod(fd,0o600)
            with os.fdopen(fd,'w') as file:
                json.dump(result,file,indent=2);file.write('\n');file.flush();os.fsync(file.fileno())
            os.replace(temporary,path)
        finally:
            if os.path.exists(temporary): os.unlink(temporary)
    print('PASS: verified enrollment records merged; existing portal roles preserved.')
    print('Private backup:',backup.name)

if __name__=='__main__': main()
