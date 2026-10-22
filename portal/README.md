> Current AI direction (22 October 2026): Amit requested Microsoft Copilot instead of Gemini. The Gemini generation and extraction path has been removed from the application. Linda is intentionally unavailable for answers until a supported, licensed Microsoft integration with user authentication and approved library scope is configured. Earlier Gemini deployment details below are historical and must not be followed. Enroll/Admin/Axon continue independently. See [Copilot transition](cpanel/COPILOT-TRANSITION.md).

# Philexcel portals — Singapore hosting package

Implementation source, not a deployed service. For the verified shared cPanel account, use [the PHP-FPM private Python adapter](cpanel/README.md). It requires no new ports, Apache modules or services. The Gunicorn/Redis method below is an alternative for other approved hosts and must not be applied to this shared server. No NGINX changes. Do not put the app, private configuration, session store or Python files in a public static document root.

## Trial dates
Amit explicitly requested starting today. Trial starts **22 October 2026, 06:36:05 Singapore/Philippines time**, expires **21 November 2026, 06:36:05** (UTC+08:00). Constants in policy.py enforce one fixed company trial across users/restarts. Only the AI feature is gated by expiry. Changing deployment time does not restart it. Admin-controlled renewal needs a subsequent audited configuration change; no automatic billing.

## What is implemented
- Entra tenant-only interactive sign-in; server-side token/session storage; CSRF protection and rate limiting.
- Private approved staff register keyed by immutable Entra object ID. Browser selections cannot grant a department. Axon/admin role allowlists.
- Optional hashed entry gates for enrollment and Axon, after personal sign-in. They supplement identity, never grant access by themselves. Store hashes privately; no numeric gate values in source.
- Linda question UI, company trial, citations, delegated Microsoft Graph drive-scoped search, current item access checks before/after Gemini generation, Board/source allowlist.
- First release uses SharePoint's existing search index, not a separate vector database. Search is keyword-based; a long conversational question may need shortening. TXT, text PDF and DOCX up to 5 MB, bounded excerpts. Scans, spreadsheets and larger documents are not extracted yet. No document cache/chat history retained.
- Personalised Windows mapping download: preview, connectivity check, credentials only on client, probe share access, explicit occupied-drive replacement, mapping backup and best-effort rollback. Existing letters are preserved unless the person explicitly approves replacement. No wildcard unmap.
- Mac SMB helper plus Finder steps. Phone/away instructions link to Microsoft-protected SharePoint. No script auto-execution in a browser.
- Admin/support pages give clear procedures; privileged NAS account creation/disable, live health, trial renewal automation are **not implemented**. Admin must perform the documented NAS/SharePoint steps.

## Alternative deployment needs (not for the current shared cPanel server)
1. Confirm the exact Singapore server, hosting account, OS and current Apache arrangement. Do not install globally or modify unrelated accounts. A supported Python runtime, virtual environment, Redis and per-account Gunicorn process are required. If unavailable, assess the existing account's supported application runner first.
2. Create a new Entra **web** application for these portals, separate from the PnP provisioning app. Single tenant. Delegated Microsoft Graph `User.Read`, `Files.Read.All`; authorize consent according to tenant policy. Add these exact Web callback URLs:
   - https://ai.philexcel.com/auth/callback
   - https://enroll.philexcel.com/auth/callback
   - https://admin.philexcel.com/auth/callback
   - https://axon.philexcel.com/auth/callback
3. Use HTTPS on every hostname. Configure each Apache host to proxy to the same loopback Gunicorn listener, preserving Host. Do not expose Gunicorn publicly. Use correct canonical hosts and validated TLS; app cookies are Secure and host-only, so sign-in on different portals is separate (Microsoft browser SSO can simplify it).
4. Create an app-owned private directory, mode 0700, outside document root. Store environment, sessions and private JSON files there. Real files mode 0600. Do not store them in Git or Library uploads.
5. Populate configuration from `.env.example` through the service manager, not by serving an .env file. Install dependencies in a virtual environment. Add `redis` Python client for the configured Flask-Limiter Redis backend (included below in requirements).
6. Generate a random SESSION_SECRET with `python -c 'import secrets; print(secrets.token_hex(32))'`. Generate each portal entry hash privately with:

   python -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('Entry password: ')))"

   Enter Amit's agreed entry password locally; never put its plaintext into source or command arguments. These short shared entry passwords do not replace MFA/account authentication.
7. Private `staff.json` example (replace placeholder object IDs and confirm actual emails/NAS names privately):

   {"ENTRA-OBJECT-ID": {"enabled": true, "nas_username": "CONFIRMED-NAS-NAME", "departments": ["Marketing"], "roles": []}}

   Allowed departments: Executive, Administration-HR, Marketing, Administration-Marketing, Finance-Purchasing, Engineering. `roles` may contain `admin` and/or `axon` only for specifically approved operators. Do not automatically promote the PnP commissioning administrator. An enabled user always gets Company-Shared in the portal; actual SharePoint and NAS memberships must also be provisioned. Disabled/missing records deny access.
8. Private `libraries.json`: map each of the seven exact approved library names to its Microsoft Graph drive ID, obtained from HUB only. Do not include Board. Example: {"Marketing":"DRIVE-ID", "Company-Shared":"DRIVE-ID", ...}. Verify names and IDs manually once. Each user must have the matching SharePoint group membership before chat can access files.
9. Set Gemini key/model privately after confirming a company-owned Google API project, model availability, billing and client data handling. Use paid/company-approved handling for confidential company documents. A hub mailbox is not an API credential. No credentials in chat or screenshots.
10. From portal directory, run `gunicorn --bind 127.0.0.1:8107 --workers 2 --timeout 150 app:app` through the hosting account's process manager. Workers must share Redis rate-limit storage and the private session directory; restrict that directory to the same trusted app owner.
11. DNS A/AAAA records for ai/enroll/admin/axon point to this approved Singapore host, with valid TLS. **Do not point them at the NAS.** Keep the existing data.philexcel.com SharePoint redirect unchanged until deciding whether an extra entry landing page is desired.

## data.philexcel.com entry password
The existing Cloudflare redirect cannot enforce this app's DATA_GATE_HASH. SharePoint already requires the user's Microsoft account and document permissions. A fixed entry password on a replacement landing page only gates that landing page; direct SharePoint links remain accessible according to Microsoft permissions. Do not call that an extra SharePoint access control. `/data` is available on the authenticated app for an optional landing gate, but no DNS/redirect is changed by this package.

## Enrollment release checks
Personalised downloaded scripts are currently unsigned. **Do not tell staff to bypass execution policy or SmartScreen.** Axon must sign the final per-user Windows installer or move to a signed generic installer plus authenticated configuration before rollout. Do not deploy executable scripts directly from a writable public website without release integrity/signing. Test Windows SMB 1219 credential conflicts and disconnected mappings. Windows can ask for NAS credentials again after restart; persistent mapping is not a promise that credentials are saved. Phones use SharePoint; iOS Files SMB is an optional LAN-only manual workflow, no drive letter or PowerShell. macOS script execution may require owner-execute permission; Finder instructions avoid this requirement entirely.

## Tests and remaining acceptance
Run `PYTHONPATH=. pytest tests -q`. Boundary and authorization tests run without company credentials. Before go-live test real Entra callback, consent, revoked/disabled users, department denial, wrong portal gate, missing/expired trial, CSRF, throttling, source links, unsupported documents and Gemini errors. Perform Windows and Mac device UAT and all seven sync/conflict/deletion/restore checks. Security code tests cannot prove production identity/provider wiring or actual NAS mapping.

Default Flask development server is not used. App returns generic provider errors; no documents/keys/tokens in error responses. No global administrator/cloud application permission is required for runtime file retrieval. Every document read uses that user's delegated token. NAS is never contacted by the Singapore backend.

## Linda access controls
`admin.philexcel.com` includes a working per-person Linda settings form. Only approved `admin` role holders can save changes. It can enable/disable AI, assign selected departments, or explicitly approve Executive AI scope covering all seven HUB libraries. Executive status is never inferred from a display name or NAS group. Each change records actor, target, previous settings, new settings and UTC time in the private ACCESS_DATABASE SQLite audit table. Store the database in the private directory and back it up.

These AI settings are independent of enrollment drive mappings and cannot create Microsoft file permissions. Effective Linda access is the intersection of enabled account, enabled AI, approved AI libraries, active company trial and the user's current Microsoft document rights. An Executive user needs appropriate SharePoint read permissions across the seven libraries before all-department answers work. Board is never added.

Staff are refused when choosing an unauthorized workspace. Questions explicitly naming a restricted department get a friendly routing message without querying that library. Linda cannot always classify an ambiguous topic; insufficient evidence produces a no-answer response, never a guessed claim about restricted documents. Staff should ask a colleague to use their own login, never borrow their credentials. AI access changes are rechecked before and after model generation.

Local checks completed: seventeen policy/request tests, Python compile, JS syntax and Mac shell syntax. Provider credentials, actual server runtime, browser rendering, executable signing and Windows/Mac/phone device UAT remain to be completed. No production provider request was made during local tests.


## Development checkpoint — 22 October 2026
- Department workspace buttons show only the signed-in person's approved Linda scopes. Executive has an All departments option.
- Admin and Axon pages display the last 50 Linda permission changes. Role checks protect both views; staff cannot open them or save access settings.
- Administration/Marketing routing takes precedence over generic Marketing, preventing mistaken out-of-department refusals.
- Enrollment downloads are tested for approval gate enforcement and exact assigned share lists; no passwords are embedded.
- Seventeen local tests pass, including a simulated document-to-Gemini-to-citation flow, removal of access during generation, rejection of Board documents and prevention of unauthorized Executive grants. Real Microsoft/Gemini responses are not yet tested.
- Automated GitHub checks are configured for portal changes. Workflow execution is separate from the local passing results.
- DNS, Singapore hosting and real provider credentials are deliberately deferred at Amit's instruction.

## Current cPanel deployment checkpoint
The philexcel account has Python 3.12, a private virtual environment, installed dependencies and 17 server-side passing tests. PHP-FPM runs as philexcel (UID 1164) and successfully launches that private Python. The account-only adapter adds three local tests (20 total). Its PHP syntax and end-to-end hosting checks remain pending on the target host. Secrets, Entra runtime registration, staff/library mapping and live provider UAT are still required. See cpanel/README.md. Do not relax apps directory permissions or install shared Apache modules.

## Enrollment Windows download — AXON UAT v5.6 (22 October 2026)

The public `/enroll` landing page offers automatic setup and a manual mapping guide. Its `/enroll/installer` endpoint serves **exactly** `/home/philexcel/Philexcel-NAS-Setup-Repair-UAT-v5.6-AXON.bat` (uploaded using cPanel File Manager). The endpoint deliberately has no fallback to the generic `portal/downloads/Philexcel-NAS-Setup-Repair.bat` file. A missing/empty approved file returns HTTP 503 instead of delivering a different installer. The filename is not client-selectable; do not expose arbitrary paths.

**Privacy/release warning:** This AXON UAT batch has included a staff/NAS username lookup table. Even if profile details appear only after login, a downloadable .bat is readable by anyone who downloads it. The public endpoint needs an explicit release/privacy review before opening it to general staff. The batch may also need code signing or an approved installer distribution policy. NAS ACLs independently enforce actual access. Do not mistake hostname detection on the employee PC for website authentication or a secure access gate.

Account-only deployment after Git pull: verify the uploaded file exists, is readable by `philexcel`, has expected hash/size, and the download response uses this exact filename. Run `pytest` and Windows UAT. Do not restart web servers, modify other cPanel accounts or move secrets into Git.

