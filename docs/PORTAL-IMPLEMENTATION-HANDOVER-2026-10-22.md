# Spencer work order: Enrollment, Admin and Axon

Requested by Amit on 22 October 2026. Implement and test in this order. This document records requirements and commissioning work, not a claim that live user provisioning or health collection already works.

## Completed and evidenced

- Amit confirmed all 18 staff mappings. NAS department/email updates and department plus Company Shared groups verified; Ian has every department. Jannie duplicate deleted, Jhojie retained; final NAS list has 21 accounts.
- Amit reported full SharePoint roster membership script completed in PowerShell 7. Hub owner access remains; Executive has Contribute across the seven HUB libraries. Confirmed roster is in CONFIRMED-STAFF-MAPPING-2026-10-22.md.
- Four existing PHP/Python portal entry points published previously. New enrollment implementation passes 33 local Python tests and Mac shell syntax validation. Windows parser/device testing has not been run.
- Spencer's earlier Marketing pilot and Amit's later setup remain separately attributed in the existing handovers.

## 1. Enrollment — implement first

Address: https://enroll.philexcel.com

- Public welcome: Microsoft 365 work sign-in or setup without Microsoft 365. No shared enrollment gate is required under Amit's latest instruction.
- Microsoft validates credentials. Callback checks the configured Philexcel tenant and verifies /me object ID and Member user type. Reject guests or another tenant; do not expose account-existence information to anonymous visitors.
- Any valid tenant member can reach the welcome. Show verified Microsoft name/account. Only a server-managed, enabled NAS mapping determines the department and eligible shares; an email address, directory department or form entry never grants rights.
- Confirmed staff: show name, department, NAS username, folder names, Windows letters and office paths. Approved executives: all seven HUB folders. Other staff: own department plus Company Shared.
- Valid Microsoft identity without a matched NAS record: explain that the NAS account/department needs administrator confirmation. No personalised eligibility or authenticated helper is supplied. Do not claim their Microsoft account is missing when sign-in succeeded.
- No Microsoft account: explain that a separate approved personal NAS account is required. Provide manual steps and an optional helper based on administrator-confirmed details. Label these entries self-declared; do not present them as verified access or create an account.
- The browser cannot inspect local drives. Downloaded read-only checks show mappings locally and upload nothing. Windows setup defaults to check-only, requires MAP, keeps matching mappings (including another letter) and unrelated drives, confirms each conflicting letter before removal, probes new access first and saves old paths locally. No wildcard unmapping.
- Mac defaults to check-only, requires CONNECT and opens Finder SMB connections. Keep matching connections; never eject volumes automatically. Close files before manually ejecting an approved old connection. Aliases of the same NAS may require manual review.
- Use personal NAS credentials entered locally; never embed passwords, Microsoft tokens or entry gates in scripts. Microsoft sign-in does not authenticate SMB. Do not weaken PowerShell execution policy; sign the final Windows helper for staff rollout.
- Office mappings require office LAN/Wi-Fi or separately approved connectivity. QuickConnect is not SMB. Phones and offsite staff with Microsoft 365 use https://data.philexcel.com. No Microsoft account means no assumed cloud access; ask the administrator for an approved alternative.

### Standard letters

| Department | NAS share | Letter |
|---|---|---|
| Executive | Executive | X: |
| Administration-HR | AdminHR | H: |
| Marketing | Marketing | M: |
| Administration-Marketing | AdminMarketing | R: |
| Finance-Purchasing | FinancePurchasing | F: |
| Engineering | Engineering | E: |
| Everyone approved | CompanyShared | Z: |

### Populate the private register

1. An authorised Microsoft administrator runs scripts/Export-Enrollment-Register.ps1 in PowerShell 7 with an existing Graph User.Read.All connection to the correct tenant. It verifies 18 staff plus Hub as enabled Members and exports object-ID keyed input. It changes no memberships. Confirm all output before importing.
2. Transfer the JSON privately to /home/philexcel/.config/philexcel-hub/enrollment-import.json, owned by philexcel and mode 600. Never public_html, a public download or Git. Preserve existing private environment.json/staff.json and roles.
3. Under the philexcel account run the private importer below. It locks, validates, backs up and atomically merges. It rejects a disabled existing registration and identity/NAS collisions. Existing portal roles/AI settings are preserved; new accounts get no admin/support role and Linda is not automatically enabled.

```bash
runuser -u philexcel -- /bin/bash <<'IMPORT'
set -e
cd /home/philexcel/apps/philexcel-hub
.venv/bin/python portal/cpanel/import_enrollment.py \
  < /home/philexcel/.config/philexcel-hub/enrollment-import.json
IMPORT
```

Hub's NAS/Microsoft administration does not automatically confer portal roles. Verify Hub object ID fc1cb5db-4fe9-4d3c-b1c0-df218313d82f and explicitly configure the existing private staff record's admin role under the authorised setup. Preserve Ian's existing roles. Do not assign axon/admin to every employee. Future client Admin UI must replace this manual registry maintenance only after it is implemented and tested.

### Deployment and acceptance

- Only the philexcel account. Source /home/philexcel/apps/philexcel-hub; existing .venv Python 3.12; PHP-FPM front controllers unchanged. No NGINX, Passenger, global installation, restart, new listening port or global Apache changes.
- Fetch origin/main, inspect changes and test in a detached account-private Git worktree before pulling into the live source: changing live source immediately affects new PHP bridge requests. Require clean tracked live files, preserve private configuration and record the prior revision for rollback.
- From the candidate worktree's portal directory run /home/philexcel/apps/philexcel-hub/.venv/bin/python -m pytest tests -q and bash -n downloads/Enroll-Mac.command. After success, pull the reviewed revision with --ff-only in the live repository. Do not copy secrets or alter the fixed PHP bridge/handlers for this release.
- Test origin and proxied HTTPS separately before changing DNS. Keep Cloudflare Full (strict), valid origin AutoSSL and authenticated responses uncached. A previous check from the assistant environment returned 403; its source was not established. Do not infer a DNS or origin failure from that alone.
- Real UAT: registered regular user, valid unmatched member, guest/wrong tenant, disabled registration, Ian executive, Hub, logout and expired sessions. Confirm no other employee's record is shown.
- Windows: no prior mapping, matching target, same share on another letter, conflicting company mapping, unrelated mapping, occupied local letter, offline NAS, wrong password, cancelled confirmation, SMB credential conflict and partial-failure recovery. Close files before replacement. Sign installer after final changes; verify signature and normal-user execution on an actual staff PC.
- Mac: no volumes, matching volume, old volume/manual eject, wrong password, offline NAS and cancelling. Verify Finder actually opens each approved folder; opening a URL alone is not a completed mount.
- Verify own/shared read/write and cross-department denial using staff accounts, not admin. Record date/device/identity class/results without passwords. Phone: confirm cloud instructions and access.
- Keep rollout marked commissioning until registry, sign-in, native-device and permission tests pass. Send Amit the completed/pending checklist and evidence; report blockers clearly.

## 2. Admin — after enrollment acceptance

Address: https://admin.philexcel.com. For approved client administrators; separate from Axon.

Current page has Linda portal controls, guidance and audit only. Build the staff lifecycle: select an existing verified 365 identity or an explicitly NAS-only user; capture name, NAS login, department and manager approval; preview exact own/shared rights; create/update NAS account and groups; apply matching SharePoint membership; link by immutable object ID; show each system's success/failure separately. New 365 accounts/licences require separately authorised tenant administration, never silently purchase a licence. Do not assume a NAS account creates an email account.

Use server-side admin authorisation, CSRF protection, least-privilege connectors, audit and explicit executive approval. Offer disable/offboarding, approval-based department transfer and password reset without storing/displaying passwords. Preserve existing data and unrelated memberships; review removals. A partial failure must remain visibly pending with a safe retry, not a false success. Test with a nonadmin denial and an approved test account before production provisioning.

The SG server cannot reach office-private NAS through QuickConnect as SSH/SMB. Agree and commission an approved account-scoped connector or manual administrator workflow before claiming live NAS changes. No public NAS admin/SMB port forwarding. Portal Linda controls do not change Microsoft agent sharing or SharePoint permission enforcement.

## 3. Axon — after Admin workflow

Address: https://axon.philexcel.com. Technical support role plus the existing support gate; personal Microsoft identity still required.

Build authenticated, read-only health reporting first: NAS disks/volumes/capacity, last Cloud Sync success/errors for seven tasks, backup/restore status, certificate and renewal-job status, portal availability and outstanding tasks. Every panel must show source, last checked time and unknown/stale/error explicitly; no fabricated green status. Keep device credentials/private logs off the public browser. Add a separately approved secure collector if needed; no global services/ports or unrestricted command execution.

Permission-changing, reset, delete or repair actions need scoped authorisation, preview/confirmation, audit and tested rollback. Client admin and technical support permissions remain separate.

## Still pending outside these portals

Linda SharePoint retrieval/citation UAT, regular-user department denials, appropriate per-user Copilot licensing, Outlook/own OneDrive verification, separately built email monitoring/reply workflow, all-share reverse sync/conflict/restore checks, recycle-bin administrator restore, independent backups, security/alerts and controlled certificate-rotation testing. Teams remains excluded. Executive & Board remains excluded from Linda and these seven sync mappings.
