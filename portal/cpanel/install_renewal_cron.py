"""Install only the account's daily certificate maintenance entry."""
import os,subprocess
from pathlib import Path
from datetime import datetime,timezone
os.umask(0o077)
if os.geteuid()!=1164:raise SystemExit('STOP: Run as philexcel UID 1164.')
private=Path('/home/philexcel/.config/philexcel-hub')
marker='# philexcel-hub-certificate-renewal'
command='17 3 * * * /home/philexcel/apps/philexcel-hub/.venv/bin/python -I /home/philexcel/apps/philexcel-hub/portal/cpanel/renew_certificate.py >> /home/philexcel/.config/philexcel-hub/renewal.log 2>&1 '+marker
result=subprocess.run(['crontab','-l'],capture_output=True,text=True)
if result.returncode and 'no crontab' not in result.stderr.lower():raise SystemExit('STOP: Unable to read account crontab.')
existing=result.stdout if result.returncode==0 else ''
if marker in existing:
 if command in existing.splitlines():print('PASS: Renewal schedule already installed.');raise SystemExit(0)
 raise SystemExit('STOP: Different renewal schedule exists. Preserved.')
backup=private/('crontab-before-renewal-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.txt')
with backup.open('x') as f:f.write(existing)
subprocess.run(['crontab','-'],input=existing.rstrip('\n')+'\n'+command+'\n',text=True,check=True)
verified=subprocess.run(['crontab','-l'],capture_output=True,text=True,check=True).stdout
if command not in verified.splitlines():raise SystemExit('STOP: Schedule verification failed.')
print('PASS: Daily renewal check installed for philexcel only, 03:17 server time.')
