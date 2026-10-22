# Philexcel HUB — latest commissioning checkpoint, 22 October 2026

Spencer's initial pilot remains attributed in SPENCER-HANDOVER.md and NAS-HANDOVER-2026-10-21.md. Earlier snapshots below are historical, not current instructions.

## Current status

- 18 staff confirmed plus Hub administrator. NAS email/department updates and memberships completed; Ian has all department shares. Duplicate Jannie removed, Jhojie retained. Final NAS count: 21 local accounts including admin, guest and philexcelhub.
- Amit reported the full confirmed SharePoint membership script completed in PowerShell 7. Hub remains owner; Executive has Contribute across all seven HUB libraries. See CONFIRMED-STAFF-MAPPING-2026-10-22.md.
- Seven SharePoint libraries have unique permissions/versioning. Seven bidirectional sync tasks reported configured; Company Shared test file reached cloud. Full reverse-edit/conflict/delete/restore UAT remains pending.
- Tess HR and James Engineering own/shared SMB tests passed; cross-department tests denied. Effective access for every user and direct sharing grants still require review.
- Four account-only PHP-FPM/private Python portal entry points remain in place. Enrollment revision 3402b44 was fast-forward deployed by Spencer on 22 October; 33 target-candidate Python tests and Mac shell syntax passed. The private register was imported with 19 identities; HUB and Camille live Microsoft enrollment passed. See the dated Spencer UAT addendum below for exact scope and remaining tests.
- Enrollment accepts valid tenant members without a shared enrollment password. Confirmed private records supply folder eligibility; unmatched members get a confirmation-pending message. Public manual helpers grant no permissions.
- Helpers check existing connections and require explicit continuation. Matching/unrelated mappings are kept. Windows signing and Windows/Mac replacement/rollback UAT pending.
- Portal admin roles are separate from SharePoint ownership. Confirm Hub's admin role privately; importing enrollment records preserves existing roles.
- Admin currently provides Linda settings and guidance; live NAS/M365 provisioning is not connected. Axon currently provides technical guidance/audit; live health reporting is not connected.
- Linda launches Microsoft 365. Gemini removed; Teams excluded. Org-wide sharing does not override file permissions. SharePoint retrieval/citations, licences, Outlook and own OneDrive need live verification. No automatic mailbox workflow is running.
- Daily certificate check installed at 03:17 server time; authentication check succeeded. Certificate expires 2028-10-20T23:24:46Z; live rotation unproved. Website AI trial ends 2026-11-20T22:36:05Z; Microsoft billing and access are separate.

## Addresses

| Address | Purpose |
|---|---|
| https://hub.philexcel.com | Remote NAS shortcut; personal NAS accounts |
| https://data.philexcel.com | HUB SharePoint shortcut; own Microsoft 365 sign-in |
| https://enroll.philexcel.com | Valid member welcome, confirmed NAS folder/drive plan, Windows/Mac setup and manual route |
| https://ai.philexcel.com | Linda, Philexcel AI Agent; Microsoft sign-in and separate agent access/licensing |
| https://admin.philexcel.com | Authorised client administrators; live user-management workflow pending |
| https://axon.philexcel.com | Authorised support role plus support gate; live health workflow pending |

## Next work

See PORTAL-IMPLEMENTATION-HANDOVER-2026-10-22.md for acceptance criteria. Enrollment code deployment and private 19-identity register import completed on 22 October (see Spencer addendum); priority now is office-network/device/security acceptance after NAS relocation, then Admin provisioning, then Axon health.
Keep all changes inside the philexcel account. No global packages, web-server changes, service restarts, new ports or other-domain changes. Preserve main-domain redirect, data shortcut, email DNS and origin SSL.

## Earlier commissioning record (historical)

## Addresses and hosting

| Address | Purpose | Current evidence |
|---|---|---|
| enroll.philexcel.com | Personal login, approved department/Company Shared drive setup; PC/Mac downloads, phone instructions | DNS/subdomain/TLS reported working; app publication and sign-in UAT pending |
| ai.philexcel.com | Linda, your Philexcel AI Assistant | Same hosting ready; live Gemini key/model and approved staff/library configuration pending |
| axon.philexcel.com | Authorized Axon technical support workspace | Role-protected code; live NAS administration is not connected |
| admin.philexcel.com | Approved Philexcel administrator; Linda access controls and audited changes | Role-protected code; NAS/SharePoint provisioning remains documented manual work |
| data.philexcel.com | Existing shortcut to Philexcel HUB SharePoint | User confirmed redirect works; Microsoft controls file permissions |
| hub.philexcel.com | Intended NAS remote shortcut | Earlier DNS/TLS issue; current branded shortcut not independently reverified |

Four portal A records point to 38.247.64.20. cPanel account philexcel owns
public_html/ai, /enroll, /admin and /axon. Subdomains were created via cpapi2
SubDomain/addsubdomain. AutoSSL was requested through UAPI SSL/start_autossl_check.
DNS-only was used during troubleshooting; Amit reports SSL working and restored
Cloudflare proxying. Preserve valid origin certificates and Full (strict) TLS;
verify renewal paths, avoid caching authenticated pages/API/downloads, and confirm
actual client-IP restoration before tuning throttling. Do not change email DNS,
main-domain redirect, existing data shortcut, ports or other hosting accounts.

## Server arrangement verified

Python 3.12.12 is available. Source is private under the account's apps directory;
venv packages installed and pip check passed. PHP 8.3.30 FPM-FCGI runs as the cPanel
account (UID 1164), not Apache's shared nobody user. PHP successfully executed
private Python and imported Flask under UID 1164. Public entry points will invoke
one fixed Python bridge per request. No listening Python port, NGINX, Passenger,
Redis server, Apache restart or global configuration changes are required.
Keep apps and private configuration directories mode 700; secret files mode 600.
PHP syntax and 21 tests passed on the target server for the certificate build.
Latest additional renewal tests passed locally; target verification pending.

## NAS work: Spencer then Amit

Spencer's original Marketing pilot included personal login, file creation/upload,
deletion and restoration from that share's Recycle Bin. Its original handover is
retained, not rewritten as work performed by Amit.

Amit continued provisioning and UAT: 19 approved first-name staff accounts plus
three system/support accounts, six departments plus Company Shared; professional
group names retained original group IDs. Staff have own department RW and Company
Shared RW. Four confirmed emails retained; remaining email matches await client
confirmation. NAS accounts and Microsoft identities are independent.

| Volume | NAS share | Group / SharePoint library | Planned drive |
|---|---|---|---|
| 1 | Executive | Executive | X: |
| 1 | AdminHR | Administration-HR | H: |
| 1 | FinancePurchasing | Finance-Purchasing | F: |
| 2 | Marketing | Marketing | M: |
| 2 | AdminMarketing | Administration-Marketing | R: |
| 2 | Engineering | Engineering | E: |
| 2 | CompanyShared | Company-Shared | Z: |

Two independent Basic/Btrfs volumes on DS223; this is not RAID redundancy. Each
share has its own Recycle Bin. Marketing recovery passed; administrator restore
across all bins and retention policy remain pending. Representative HR and
Engineering users passed own/shared SMB read/write tests; five other departments
were denied. Main NAS administrator contact email was updated to the dedicated
Hub mailbox and administrator membership verified. Actual identities/credentials
and private addressing belong only in the restricted operational register/vault.

QuickConnect remote DSM is user-confirmed working. It does not provide remote
SMB/SSH. Tailscale was evaluated, then superseded; cleanup unverified. Login
branding updated per user confirmation. Desktop wallpaper is separate. No public
SMB/SSH forwarding authorized. Existing office Z: mapping is preserved until
approved cutover; enrollment must not indiscriminately remove mapped drives.

## SharePoint and synchronization

Philexcel HUB site exists, owned by the dedicated Hub account. Seven libraries
have unique permissions and versioning: Owners and commissioning administrator
Full Control; matching departmental group Contribute. Groups were created empty.
Do not claim all Microsoft 365 users can access Company Shared: actual membership
must be assigned and tested after identity matching. Existing Executive & Board
site remains excluded from sync, library mapping and Linda.

Cloud Sync installed. Amit reports all seven mappings set to bidirectional and
completed. One NAS-to-Company Shared test file appeared in SharePoint. This does
not prove reverse edit, conflicts, deletion/restore, every department mapping or
cloud access isolation. Remaining tests are required. Sync is not independent
backup; establish a separate versioned backup and tested restore.

## Microsoft authentication

Separate single-tenant Philexcel HUB Portals web app created, four exact HTTPS
/auth/callback URIs configured. Existing Philexcel HUB Setup/PnP app unchanged.
RSA-3072 certificate created privately; public certificate registered in Microsoft.
Delegated User.Read and Files.Read.All consent verified as AllPrincipals. This
allows user-context retrieval, not unattended company-wide file access. The app
also restricts retrieval to approved HUB libraries and excludes Board.

Current certificate expiry: 20 October 2028 23:24:46 UTC (21 October 2028 07:24:46
Singapore/Philippines). This is separate from the fixed 30-day Linda trial ending
21 November 2026 at 06:36:05 local time. Hosting may disable AI independently;
certificate renewal affects sign-in across all four portals.

## Renewal and expired-certificate recovery

See ../portal/cpanel/CERTIFICATE-RENEWAL.md. Renewal code exists in Git and has
local mocked tests; no renewal cron has yet been installed or live rotation
proved. Schedule only under philexcel, after authentication check succeeds.
If every registered certificate expires, self-service renewal cannot work:
create a new private key/public certificate pair under the account, upload only
the public certificate using an authorized Microsoft administrator, test token
acquisition, then atomically switch environment.json paths. Preserve the old
configuration for rollback; never expose private keys in Git/email/public_html.

## What remains before the four portals work

1. Verify certificate token acquisition on the server; install account-only daily
   renewal check and prove one controlled rotation before claiming auto-renewal.
2. Obtain verified Entra object IDs and seven HUB Graph drive IDs. Approve the
   initial administrator explicitly; match remaining staff to NAS names privately.
3. Set hashed entry gates locally. Supplemental gates never replace personal login.
4. Configure the company Gemini API key/model privately and approve Linda scope.
5. Back up only portal entry points/.htaccess, merge account-only PHP routing,
   preserve cPanel handlers and ACME path. Publish only the four portal roots.
6. Test real Microsoft callbacks/sessions, correct permissions, gates, admin edits,
   Linda citations/denials, trial expiry, logout, throttling and rollback. Do not
   confuse mocked tests with real Microsoft/Gemini/browser UAT.
7. Sign enrollment scripts and complete PC/Mac/phone UAT, old Z: cutover approval,
   seven sync/restore tests, NAS security/alerts/UPS and independent backup.




## Spencer on-site Enrollment commissioning addendum — 22 October 2026

**Evidence source:** Spencer's terminal outputs and browser/DSM screenshots from on-site testing at Amit's office. NAS currently at Amit's office; planned relocation to Philexcel on 23 October 2026. This section supersedes earlier *pending deployment/import* status, while preserving prior attribution to Amit and Spencer.

### Deployment and register — completed

| Check | Result / evidence |
|---|---|
| Account isolation | Work performed as Linux user `philexcel` for application operations, under `/home/philexcel`; no reported global service restarts or root configuration changes |
| Git | Live branch `main` fast-forwarded from `fa7afa8` to `3402b44329ac49452da2be7f6583f0aecf4243a8`; tracked files clean; existing untracked `.venv/` retained |
| Candidate checks | 33 pytest cases passed in 2.20 seconds; `bash -n downloads/Enroll-Mac.command` passed; existing Python 3.12.12 used |
| Microsoft identities | Authorized Graph export verified 18 staff plus HUB as enabled tenant members; 19 unique immutable IDs |
| Register security | Private `enrollment-import.json`, owned by `philexcel` and permission `0600`, outside `public_html`; 19 JSON records and 19 unique IDs verified |
| Import | `portal/cpanel/import_enrollment.py` reported PASS; preserved existing portal roles; generated private `staff-before-enrollment-20261022T050647-2ea9b8.json` backup |
| Staff registry result | 19 entries total; HUB and Camille both enabled and matched to NAS usernames `philexcelhub` / `Camille`. Both had empty portal role arrays `[]` after import |
| Post-deployment web | Enrollment welcome page loaded over HTTPS; HUB and Camille Microsoft sign-ins displayed personalized enrollment instead of confirmation-pending page |

### NAS and Windows UAT — performed at Amit's office

| Test | Observation / outcome |
|---|---|
| NAS LAN | DSM TCP/5001 and SMB TCP/445 reachable at temporary office IP the NAS's temporary Amit-office private IP (recorded in the restricted configuration register) |
| NAS folders | Seven shares visible: Executive, AdminHR, AdminMarketing, Engineering, FinancePurchasing, Marketing, CompanyShared |
| Camille SMB/DSM | NAS username `Camille` signed in; Marketing and CompanyShared accessible, test folders/files created and edit/save/reopen reported successful. Restricted AdminHR/Executive produced access-denied/credential prompts; complete per-share deny matrix not yet evidenced |
| HUB portal plan | Executive enrollment offered seven shares and expected drive letters X:, H:, M:, R:, F:, E:, Z:; DSM permission preview displayed RW for seven shares |
| Windows mapping | Spencer's normal Windows session mapped all seven shares using `net use ... /persistent:no`; each mapped drive reported OK and `Test-Path` true; subsequent `Get-ChildItem` readability passed for all seven |
| Windows SMB diagnostic | SMB 3.1.1. `Get-SmbConnection` displayed Windows account `Amit1\\Spencer`, which does **not** independently prove NAS-side authentication as `philexcelhub`. Elevated PowerShell did not show normal-session drive letters (UAC session separation); normal session checks passed |
| Script signing | Downloaded `Check-Drives-Windows.ps1` blocked by workstation execution policy because it was unsigned. Built-in read-only PowerShell and `net use` checks used instead; policy was not bypassed |
| Old X: mapping | Disconnected `\\\\onepro-nas\\One Pro IT` mapping was manually removed by Spencer before temporary X: mapping test; no wildcard unmapping instructed |

**Scope conclusion:** Spencer's local connectivity, enrollment, manual mapping and mapped-drive readability tests passed. This does **not** constitute full rollout acceptance, complete mapping-helper UAT or proof of NAS-side SMB identity. No claim of seven-drive write UAT is made; Camille's own/shared read/write is a separate documented test.

### Items still open before full staff rollout

1. Relocate NAS to Philexcel office on 23 October 2026; verify actual office IP, reachability, office connectivity and update account-private NAS host configuration only if needed. Retest portal instructions/mappings after relocation.
2. Verify NAS-side SMB authentication specifically as `philexcelhub`, without relying on the Windows `Amit1\\Spencer` display value or mixed prior SMB sessions.
3. Test regular staff sign-in, own/shared RW, cross-department denial, and per-user effective permissions on actual Philexcel devices; separately test Ian executive access.
4. Sign Windows helper and test check-only / explicit MAP, existing matching mappings, conflicts, cancellation, wrong credentials, offline NAS, and recovery with normal execution policy. Test Mac Finder helper and manual handling of old volumes. No blanket unmapping.
5. Confirm HUB's separately authorized client portal `admin` role; HUB's imported record currently has `roles: []`. Do not auto-grant roles during enrollment.
6. Validate Cloud Sync in both directions, conflict/delete/restore behavior, admin recycle-bin restore, independent backups and alerts. The seven tasks being configured is not equivalent to full sync UAT.
7. Keep Admin Portal provisioning and Axon live health connector as **future separate phases**; no claim they are connected.

### Production boundaries and artifacts

- Production shared WHM/cPanel server hosts other clients: no root-level configuration changes, global installations, web-service restarts, new ports, other accounts or DNS changes in this work.
- Philexcel private configuration backup was verified in `/home/philexcel/.config/philexcel-hub/pre-enrollment-20261022-123705` for `environment.json`, `staff.json`, `libraries.json` before deployment. Earlier historical backups were not treated as sufficient rollback evidence.
- Two attempted SQLite backup commands failed due to incompatible system `python3` SQLite API; no successful SQLite backup was established. Do not interpret these failed attempts as database corruption or as completion of independent backup requirements. No further database operation was required for the enrollment deployment.
- Generated identity JSON and private configuration must stay outside Git, email attachments and public web roots. Preserve secrets and role separation.
- Git documentation update alone does not deploy application code or change portal access.


## End-of-day supplement — 22 October 2026

For detailed evidence see [daily progress / UAT handover](PHILEXCEL-DAILY-PROGRESS-2026-10-22.md). This supplement updates earlier commissioning checkpoints without retroactively changing historical test results.

- Windows batch mapping of CompanyShared to `Z:` passed Explorer visibility, SMB OK, Test-Path, directory listing and temporary file write/read/delete.
- cPanel account-only Git pull and 33 application tests passed at reported earlier `17e8437` checkpoint. A later Git change targets the account-uploaded AXON v5.7 DSM Access Sync batch; the server pull, download byte/hash and v5.7 Windows permission-change tests were **not yet reported complete**.
- DSM `administrators` group readback confirmed Ian added alongside built-in admin and philexcelhub.
- Camille confirmed in Marketing and Company-Shared. DSM delegated Local user/group management option was selected; the screenshot does not confirm saved state. This native delegated role permits ordinary account/group deletion. Full DSM administration was not granted to Camille.
- All seven NAS share-path and ACL readbacks completed; departmental RW groups confirmed, Recycle Bins enabled and `#recycle` entries contained broad `everyone` ACLs. Parent share ACLs may still restrict access; do not infer actual cross-department exposure without effective SMB access testing.
- Camille's requested file read-only treatment, delete prohibition, and confidential cross-department browse visibility are **not implemented** and require separate approval and a tested ACL design.

Do not represent NAS relocation, full cloud-sync conflict/restore UAT or independent backups as completed based on the above.
