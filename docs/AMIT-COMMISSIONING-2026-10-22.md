# Philexcel HUB — Amit commissioning record, 22 October 2026

This is the latest checkpoint, supplementary to Spencer's preserved notes in
SPENCER-HANDOVER.md and the 21 October Marketing pilot in NAS-HANDOVER-2026-10-21.md.
Results are from Amit's pasted terminal output or explicitly stated confirmations;
no independent live-site certification is implied.

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
