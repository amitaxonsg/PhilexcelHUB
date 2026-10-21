# Account-only cPanel deployment: Philexcel

This replaces the Gunicorn/Redis deployment instructions for the existing shared
server. Do not install Passenger, NGINX, Redis or system packages; do not change
ports, the main website redirect, Apache configuration, or other accounts.

## Verified on the hosting server

- Account: philexcel, UID 1164, home /home/philexcel.
- Python 3.12.12; private venv: /home/philexcel/apps/philexcel-hub/.venv.
- PHP 8.3.30, FPM-FCGI executes as philexcel, with proc_open, SQLite, cURL, OpenSSL.
- PHP successfully launched the private Python and imported Flask as UID 1164.
- Direct CGI ran through shared Apache nobody and failed at the private apps
  directory. Keep apps mode 700; do not expose it to nobody.
- Original 17 portal tests passed on the server before adding this adapter.
- Origin TLS check succeeds using ai.philexcel.com resolved to 38.247.64.20;
  loopback 127.0.0.1 selected a different certificate. Do not disable TLS checks.

## Architecture

Each portal's index.php starts one fixed private Python entry point for one
request. No shell command construction or client-provided executable paths.
Python calls the existing Flask WSGI app with HTTPS host, cookies, CSRF header,
method, query and body. Repeated Set-Cookie headers are preserved. Python never
listens on a port. Static assets also go through the app.

Environment/secrets and staff mappings stay outside public_html. Existing
server-side sessions and authorization remain in force. A SQLite counter shared
by all workers applies 60 requests per minute per REMOTE_ADDR across all four
portals. Flask's process-local limiter is disabled only in this adapter.
Cloudflare forwarded-IP headers are not trusted by the adapter. If existing
Apache configuration does not restore real client IPs, clients sharing a proxy
address share this limit. Confirm that during UAT; do not casually trust headers.

## Stage before publishing

1. Pull main as philexcel, then run pytest from portal using ../.venv/bin/python.
2. Create /home/philexcel/.config/philexcel-hub mode 700. Save environment.json
   there, mode 600, owned by philexcel. Never place it in Git or public_html.
3. environment.json is a string-to-string JSON object using the settings in
   portal/README.md: SESSION_SECRET, SESSION_DIRECTORY, PORTAL_HOSTS,
   ENTRA_TENANT_ID, ENTRA_CLIENT_ID, ENTRA_CLIENT_SECRET, STAFF_CONFIG,
   LIBRARY_CONFIG, ACCESS_DATABASE, NAS_HOST, GEMINI_API_KEY, GEMINI_MODEL,
   ENROLL_GATE_HASH and AXON_GATE_HASH, plus DATA_GATE_HASH if used by the app.
   Use absolute private paths. PORTAL_HOSTS is a comma-separated list of the four
   hostnames. Create the private session directory mode 700. RATE_LIMIT_STORAGE_URI
   is set to memory:// by the bridge; the shared SQLite limit replaces it.
4. Keep the runtime Entra web registration separate from the PnP setup app.
   Register HTTPS /auth/callback on each of ai, enroll, admin and axon hostnames.
   Configure delegated scopes and consent as described in the main portal guide.
   Staff approval and seven SharePoint library IDs must be completed privately.
   No staff credentials are inferred and Board stays excluded.
5. Before public entry points exist, test a request as the account:

   printf '%s' '{"host":"ai.philexcel.com","uri":"/","method":"GET","remote":"127.0.0.1","body":""}' | /home/philexcel/apps/philexcel-hub/.venv/bin/python -I /home/philexcel/apps/philexcel-hub/portal/cpanel/bridge.py

   Missing configuration fails closed. Do not paste secrets in terminal output.
6. Back up each portal's index.php and .htaccess to a private directory outside
   public_html. Review existing contents; do not overwrite unrelated pages.
7. Copy cpanel/index.php to only public_html/{ai,enroll,admin,axon}/index.php.
   Merge portal.htaccess into each portal's existing .htaccess, preserving its
   cPanel-generated PHP handler. Do not edit public_html/.htaccess or data/hub DNS.
   The ACME challenge path is exempted so certificate renewal can continue.
8. Check PHP syntax with the account's PHP 8.3 CLI before copying wrappers;
   no PHP CLI was available in the development container. Run portal tests too.
9. Test HTTPS, styles, login/logout, callback, session cookies, unauthorized
   access, CSRF, AI permission boundaries, downloads and trial expiry on all
   applicable hosts. Test source IP handling and simultaneous sessions. Compare
   origin and Cloudflare requests. Run nas/client UAT separately.
10. Roll back by restoring only the four backed-up entry points/.htaccess files.
    Private source and configuration can remain while investigating. No service
    restart is needed.

## Limits and operational notes

This adapter is appropriate for an initial low-traffic trial, pending live UAT.
It starts Python on every request (including static requests); it is less
resource-efficient than a persistent WSGI server. Public access can consume PHP
workers. PHP kills the child after 90 seconds, limits output to about 12 MiB, and
accepts bodies up to 16 KiB. Hosting PHP/FPM and Cloudflare timeouts may be shorter;
check long AI replies. It does not stream responses, handle WebSockets, or provide
background indexing. SQLite implements a fixed-minute limit, not a sliding window.
There is no real-world load/performance claim yet. Existing AI trial dates are
unchanged. Do not reset the trial to deployment day.

The application/library IDs, private secrets, approval mapping, portal deployment,
and full login/AI UAT have NOT been completed merely by installing these files.

## Certificate sign-in (current Philexcel choice)
Use cpanel/setup_certificate.py as philexcel to create a private RSA-3072 key and self-signed public certificate, valid for 730 days. It prints only the public DER certificate encoded as base64. Upload that public certificate as a keyCredential on the separate portal application using Microsoft Graph PowerShell; preserve any existing public certificates. The setup stores ENTRA_PRIVATE_KEY_PATH and ENTRA_CERTIFICATE_PATH privately and removes the unused local secret setting. Re-running preserves a valid matching pair; partial or mismatched pairs stop for review. Microsoft registration and consent remain separate steps. MSAL >=1.35 uses the supplied PEM certificate to calculate a SHA-256 thumbprint. A configured incomplete certificate pair fails closed instead of falling back to a password. Keep private key mode 600 outside public_html. Certificate renewal is required before its printed date; this is unrelated to the AI trial and does not alter the fixed trial dates. Never upload the private key to Microsoft or Git. Hosting can disable the AI portal separately.

## Renewal and commissioning update
See [certificate renewal and recovery](CERTIFICATE-RENEWAL.md) and [Amit's commissioning record](../../docs/AMIT-COMMISSIONING-2026-10-22.md). Microsoft certificate registration and delegated consent now passed in Amit's terminal. 21 tests and PHP syntax passed on target; latest renewal tests are local only until pulled. Renewal cron and public app deployment are not yet installed. Preserve Spencer's original NAS pilot evidence.
