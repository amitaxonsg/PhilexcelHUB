# Philexcel HUB — Amit commissioning record, 22 October 2026

This is the latest checkpoint, supplementary to Spencer's preserved notes in
SPENCER-HANDOVER.md and the 21 October Marketing pilot in NAS-HANDOVER-2026-10-21.md.
Results are from Amit's pasted terminal output or explicitly stated confirmations;
no independent live-site certification is implied.

## Current handover checkpoint — 22 October 2026

This checkpoint supersedes earlier pending/development statements below.
Teams is not used and is removed from Linda's approved scope. Turn OFF Teams in
Linda's Microsoft 365 Knowledge settings and remove Teams from her instructions;
this UI change has not been independently confirmed. No Teams licence purchase
or deployment is planned.

### Access and activation

| Address | Login / use | Activation status |
|---|---|---|
| https://hub.philexcel.com | NAS account; main support administrator username philexcelhub. Staff should use personal NAS accounts. | Remote NAS access reported working; branded shortcut not independently probed |
| https://data.philexcel.com | Each employee's own Microsoft 365 work account | SharePoint shortcut reported working; content rights depend on assigned permissions |
| https://enroll.philexcel.com | Registered personal Microsoft 365 account plus supplemental enrollment gate | Deployed for commissioning; Amit will activate for staff later |
| https://ai.philexcel.com | Registered personal Microsoft 365 account; Open Linda launches Microsoft 365 | Linda is the Philexcel AI Agent; staff activation deferred |
| https://axon.philexcel.com | Registered Microsoft 365 identity with axon role plus support gate | Commissioning only; activation deferred |
| https://admin.philexcel.com | Registered Microsoft 365 identity with admin role | Commissioning only; activation deferred |

Passwords are deliberately excluded from this public repository. They are provided
only in the authorised private handover. Supplemental gates do not replace personal
sign-in. Ian is the currently configured portal admin/support identity; Hub owning
SharePoint does not automatically register Hub in the portal's private staff file.

All four PHP/Python entry points were deployed account-only. Commit 648774f target
verification: 22 tests passed. No global server changes, new ports or restart.
Linda's button opens the Microsoft 365 agent; it is not embedded chat:
https://m365.cloud.microsoft/chat/?titleId=T_41918509-ad55-6c25-fb32-5c78e09bfeab&source=embedded-builder

Linda org-wide chat sharing is enabled per screenshot. Seven SharePoint libraries
were confirmed in saved knowledge settings; document retrieval has not passed UAT.
Outlook was OFF in the last inspected configuration; enabling and testing remains
unverified. Personal OneDrive search coverage is not confirmed. No unattended
15-minute email checking or automated sending is implemented. Eligible future
email requests are restricted to verified philexcel.com staff. No Teams sources.

Gemini was removed in commit 9433a50. Microsoft 365 Copilot Business trial was
assigned to Hub; other seat assignments and recurring billing state are unverified.
Do not share Hub's licence/session as a substitute for individual staff access.

### SharePoint memberships applied and reported successful

- Hub: HUB Owners; Full Control on all seven HUB libraries.
- Ian's verified commissioning account: Executive and Company-Shared.
- Executive group: Contribute on all seven libraries (content read/write, not
  administrator rights).
- Camille: Marketing and Company-Shared.
- Jhojie: Finance-Purchasing and Company-Shared.
- James: Engineering and Company-Shared.
- Administration-HR and Administration-Marketing groups remain empty.
- Other staff mappings require confirmed names/email identities. Do not guess.
- Executive & Board remains excluded; its permissions were not modified.

Existing direct grants, sharing links and unique item permissions still require
review and regular-user allow/deny tests. NAS memberships and SharePoint groups
are independent. Portal AI settings do not enforce the external agent's scope.

### Certificate and trial

Account-only daily renewal check installed at 03:17 server time; authentication
check succeeded. Certificate expiry remains 2028-10-20T23:24:46Z. Live rotation
has not been proved. See portal/cpanel/CERTIFICATE-RENEWAL.md.
Website trial ends 2026-11-20T22:36:05Z. It does not revoke direct Microsoft 365
agent access or cancel Microsoft's trial/subscription. Manage those separately.

### Remaining work

Confirm staff mapping and licences; test Linda retrieval and department denials;
disable Teams in Microsoft UI; verify Outlook and own OneDrive searches; implement
and test personal-context email automation; sign/test enrollment downloads; extend
the private portal register to approved staff; connect live administration/support
only when commissioned; complete sync reverse-direction and restore UAT, independent
backup, NAS security/alerts and approved old-drive cutover.

## Resume checklist — completed and pending

### Completed with reported evidence
- Spencer: initial Marketing NAS pilot, create/upload/delete and restore test;
  original attribution and notes preserved.
- Amit: 19 first-name NAS staff accounts, professional department groups, own
  department plus Company Shared permissions, Hub administrator email and branding.
- Representative Tess (HR) and James (Engineering) SMB own/shared read/write tests
  passed; other department shares denied in the pasted tests.
- Seven SharePoint HUB libraries created with unique permissions and versioning;
  Board excluded. Seven bidirectional Cloud Sync tasks reported configured.
  Company Shared NAS-to-cloud test file confirmed, not full sync UAT.
- QuickConnect remote NAS access and data.philexcel.com SharePoint shortcut reported
  working. Four account-only portal entry points published.
- Certificate-based portal Microsoft authentication, private configuration and
  daily account-only renewal check installed. Live certificate rotation not tested.
- Gemini removed; Microsoft 365 Linda agent created, org-wide chat sharing enabled,
  seven SharePoint sources visible in saved settings, portal launch link deployed.
- Server tests at commit 648774f: 22 passed. Later documentation/UI wording commits
  need pulling; no later target test result has been supplied.
- Confirmed SharePoint accounts assigned: Hub owner; Ian executive; Camille
  Marketing; Jhojie Finance-Purchasing; James Engineering. Executive group granted
  Contribute across all seven libraries; Owners Full Control.
- Teams excluded by Amit's instruction. Teams UI switch was already OFF in the last
  inspected screenshot; ensure it stays off and remove remaining instruction text.

### Identity confirmation required before remaining memberships
Do not assume similar initials identify these NAS users.

| NAS name | Approved NAS department | Microsoft mapping status |
|---|---|---|
| Ian | Executive | Confirmed and applied |
| Tess | Administration-HR | Await confirmed Microsoft account |
| Aliza | Administration-HR | Await confirmed Microsoft account |
| Seatiel | Administration-HR | Await confirmed Microsoft account |
| Camille | Marketing | Confirmed and applied |
| Chloe | Administration-Marketing | Await confirmed Microsoft account |
| Clark | Administration-Marketing | Await confirmed Microsoft account |
| Jhojie | Finance-Purchasing | Confirmed and applied |
| Kevin | Finance-Purchasing | Await confirmed Microsoft account |
| Ann | Finance-Purchasing | Await confirmed Microsoft account |
| Jannie | Finance-Purchasing | Await confirmed Microsoft account |
| Rose | Finance-Purchasing | Await confirmed Microsoft account |
| Nello | Finance-Purchasing | Await confirmed Microsoft account |
| Rommel | Engineering | Await confirmed Microsoft account |
| Rowell | Engineering | Await confirmed Microsoft account |
| Mavel | Engineering | Await confirmed Microsoft account |
| Evain | Engineering | Await confirmed Microsoft account |
| James | Engineering | Confirmed and applied |
| Cris | Engineering | Await confirmed Microsoft account |

15 of 19 NAS staff identities remain unmatched for SharePoint provisioning.
Remaining enabled Microsoft directory accounts must be reconciled too; not every
directory account should be assumed to correspond to this NAS roster or receive
Executive access. Confirm any additional executives explicitly.
Company-Shared currently lists only the four confirmed staff above; Hub has access
through Owners. HR and Administration-Marketing remain empty.

### Next session order
1. Obtain confirmed NAS-name / full-name / Microsoft-sign-in / department mapping
   for the remaining 15 staff, reconcile additional directory accounts and confirm
   executive approvals. Add approved users to own department and Company Shared.
2. Audit all seven library grants, direct file/folder grants and sharing links.
   Test one regular user's own/shared success and cross-department denial.
3. Linda: publish latest short instructions, keep Teams off, verify SharePoint
   retrieval/citations in a fresh chat. Previous responses claimed no source access;
   retrieval is not yet proved despite configured sources.
4. Verify appropriate Copilot licences per participating user; only Hub's trial
   assignment is confirmed. Review trial end/recurring billing separately.
5. Enable/test Outlook knowledge and confirm own OneDrive scope if required.
   Owner knowledge settings must not expose another employee's personal sources.
6. Implement separate mailbox workflow for 15-minute checks, exact philexcel.com
   sender filtering, trusted identity checks, personal-context authorisation,
   protected source links, recipient controls, draft commissioning and audit.
   No email monitor or automatic reply service currently runs.
7. Enroll: populate private staff object-ID/NAS mapping; sign Windows installer,
   test Windows/Mac and phone instructions, backup/restore existing mappings and
   obtain old Z: cutover approval. No indiscriminate unmapping.
8. Admin/Axon: distinguish current guidance/settings from unconnected live NAS/
   SharePoint provisioning and health reporting. Add only authorised functions.
9. Complete all seven sync mappings' reverse-edit/conflict/delete/restore UAT,
   recycle-bin admin restore, independent backup, NAS MFA/alerts/UPS/disk checks.
10. Verify branded NAS shortcut and origin SSL renewal, renewal-job health and
    controlled certificate rotation. Keep all changes within philexcel account.
11. Activate four portals for staff only after the above relevant checks. Portal
    and direct Microsoft agent access/trial controls remain separate.

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
