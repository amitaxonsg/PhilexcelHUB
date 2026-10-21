# Certificate renewal and recovery

Microsoft supports self-service addKey for an application's own keys with proof
of an existing valid private key; no directory-wide application permission is
required for this self-rotation. References:
https://learn.microsoft.com/en-us/graph/api/application-addkey
https://learn.microsoft.com/en-us/graph/application-rollkey-prooftoken

## Account-only schedule

Run as philexcel with its private venv. Do not install root crons, system services
or change Apache/ports. Before scheduling:

```
.venv/bin/python -I portal/cpanel/renew_certificate.py --check
```

This contacts Microsoft to test existing certificate authentication, writes a
private status file and does not replace the certificate. After success:

```
.venv/bin/python -I portal/cpanel/install_renewal_cron.py
```

The installer preserves existing account cron entries and saves a private backup.
Daily at 03:17 server time, the job authenticates, checks expiry and rotates only
within 60 days of expiry. No AI trial dates change. For one explicit commissioning
rotation test, run renew_certificate.py --rotate-now; do not put that flag in cron.

New key/certificate files stay mode 600 outside public_html. Only public DER is
sent to Microsoft's addKey endpoint, authenticated with a token and proof signed
by the old key. The new certificate must successfully authenticate before a
single atomic configuration-pointer switch. The old key and private environment
backup are preserved for rollback. No old Microsoft keys are deleted automatically.
A lock prevents simultaneous renewal jobs. Pending state supports retry after a
partial failure. Persistent provider or policy failure needs operator attention.
Expired old certificates cannot self-renew. Review inactive/expired keys during
maintenance so retained keys do not accumulate indefinitely.

Private renewal-status.json records last check/action/error type. renewal.log
holds cron output without tokens/provider messages. Cron log alone is not alerting:
arrange an existing monitoring check to flag error status or no successful check
for 48 hours. No email/monitor integration is automatically configured. Retain
normal cPanel AutoSSL checks separately: website TLS certificates are different.

## If it has already expired

1. Keep the deployed site and current private configuration; do not rerun initial
   setup_certificate.py over the original pair. It intentionally stops on expired
   or incomplete existing keys.
2. As philexcel create a NEW RSA key and public X.509 certificate at NEW private
   filenames (mode 600). An administrator must upload the public certificate.
   Use the same generation procedure as setup_certificate.py with new paths,
   rather than overwriting active files. Never upload the private key.
3. Sign in to Microsoft Graph PowerShell as an authorized tenant administrator.
   Read the portal application by its verified object/client IDs. Update its
   keyCredentials with the new public certificate, preserving any valid existing
   certificates. Alternatively use Entra > App registrations > Philexcel HUB
   Portals > Certificates & secrets > Certificates > Upload certificate.
4. Test the new pair using MSAL certificate credentials against the same tenant
   and client ID. Do not switch active paths until authentication succeeds.
5. Back up environment.json privately; atomically update ENTRA_PRIVATE_KEY_PATH
   and ENTRA_CERTIFICATE_PATH to the new matching pair. No Apache restart needed.
6. Run renew_certificate.py --check, verify the account cron still exists, and
   test sign-in/logout on the portals. Record new expiry and review monitoring.

An expired certificate is a Microsoft sign-in outage, not an AI trial extension.
Manual admin recovery remains necessary if renewal has failed until all valid
certificates expire. This procedure cannot promise renewal without monitoring.
