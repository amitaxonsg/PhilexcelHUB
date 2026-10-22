# PhilexcelHUB — Axon IT project

**Status: NAS shares and named staff accounts configured; representative Windows RW/isolation tests passed. QuickConnect remote DSM access is reported complete by Amit; cloud sync and authenticated dashboards remain pending. Not production-ready.**

## Exactly three dashboards
- **Axon IT:** technical NAS management, secure support, cloud sync, backup, audit.
- **Philexcel Admin:** onboard/disable NAS users, assign departments, change read-only/read-write rights, review NAS state, audit.
- **Department:** individual password-protected department landing page in Phase 1; **Gemini AI chatbot — Phase 2 COMING SOON**. Phase 2 will provide authorized SharePoint document answers, suggestions and source links. No staff or infrastructure management.

## Design
Synology DS223, 2 × 2TB disks. Proposed independent Basic volumes for capacity, not redundancy; independent versioned backup required. Six provisional departments: Executive; Administration/HR; Marketing; Administration/Marketing; Accounting/Finance/Purchasing; Engineering; plus Company Shared resource. Initial approved department memberships receive read/write. Verify staff names and permissions before provisioning.

NAS logins independent of Microsoft 365, no Intune/AD/Entra account synchronization. Windows PCs access NAS SMB; Microsoft 365 SharePoint Company Hub is separate for cloud access. hub@philexcel.com is the planned technical sync identity. Board SharePoint excluded. Test Cloud Sync one-way then two-way, simultaneous edits, deletions, versioning and restore. SharePoint authorization configured separately.

Remote access decision (22 October): use Synology QuickConnect for DSM and supported apps. Amit reports remote access complete. This does not provide a general SSH/SMB tunnel or publish custom dashboards. Tailscale was installed and enrolled during evaluation, then superseded due to business subscription requirements; logout/removal remains unverified. No DSM/SSH/SMB port forwarding.

AI: Gemini API server side + prefiltered SharePoint retrieval, enforce each authenticated user's current department and actual document access before reading and again before returning links. AI read-only initially, no file editing or privileged NAS commands.

## Security
**THIS REPO IS PUBLIC.** No actual passwords, recovery keys, credentials, access tokens, internal IPs, real employee register or company data in GitHub. Private setup configuration in restricted Google Drive; secrets in encrypted vault with vault references only in Drive.

See docs/DEPLOYMENT.md, docs/DASHBOARD.md and scripts/.

## Spencer: deployment and GitHub handover discipline
**This is NOT an ordinary NAS installation.** Review the [live project overview](https://amitaxonsg.github.io/PhilexcelHUB/), [technical guide](https://amitaxonsg.github.io/PhilexcelHUB/setup.html), [full blueprint](philexcel_hub_complete_setup_blueprint.png), [drive map](docs/DRIVE-MAPPING.md), [site UAT](docs/UAT.md) and [PowerShell mapper](scripts/Map-HubShares.ps1) before configuring equipment. Amit will guide implementation; raise any blockers with Rico/Axon.

- **Phase 1:** DSM and separate Basic storage volumes (subject to explicit risk approval and independent versioned backup/restore), SMB folders, verified staff permissions, careful legacy Z: migration, NAS-to-Company Hub SharePoint sync with two-way conflict/deletion UAT, secure Axon remote access, role-based dashboard foundation, Windows drive scripts, complete UAT.
- **Phase 2:** Gemini department chatbot and permission-aware document search — **COMING SOON**. No AI activation during Phase 1.
- **Professional file hygiene:** Respect exact filenames, directory names and capitalization. Never casually rename or overwrite approved files, screenshots or client assets. Use descriptive names, consistent formats and review all spelling, link targets, script parameters, dashboard labels and diagrams before committing. Avoid duplicate confusing versions; retain traceable commit messages and test any change.
- **Record all work:** After each installation action update the [restricted Google Drive setup register](https://docs.google.com/document/d/1sl62oz4k16-TaB0ieEfKYXCMGKrt-vidcTIKR-CjX4E/edit). Include who, when, NAS/network settings, test results and change details. Actual passwords and recovery codes belong in an encrypted vault, not the public GitHub repository or Google Docs.
- **Never publish unverified status:** A public GitHub Pages preview is not an authenticated production NAS administration tool. Phase 1 and Phase 2 features must be labeled accurately, with unresolved work and defects visible.

NAS setup reference: hostname PHILEXCEL-HUB; detailed private parameters remain in the restricted setup register.

## NAS commissioning reference
See [NAS setup, ports, storage allocation and verified commands](docs/NAS-HANDOVER-2026-10-21.md). Actual onsite network parameters and the current commissioning checklist are in the [restricted Google Drive configuration register](https://docs.google.com/document/d/1sl62oz4k16-TaB0ieEfKYXCMGKrt-vidcTIKR-CjX4E/edit). Treat prior hostname/account entries as historical after the approved factory reset.


## Latest checkpoint — 22 October 2026

See the [current commissioning checkpoint](docs/NAS-HANDOVER-2026-10-21.md#current-checkpoint--22-october-2026-amit-guided-terminal-evidence). Seven professional department/resource group names are in use; 19 named staff accounts receive their own department RW and Company Shared RW. Two representative Windows pilots passed own/shared RW and other-department denial. Every share has a separate Recycle Bin; admin must be able to view all bins, subject to remaining restore UAT.

Next requested order: verify dedicated Hub identity and tested two-way Synology Cloud Sync, then the three authenticated dashboard roles. QuickConnect DSM remote access is reported complete; branded Cloudflare redirect DNS/TLS verification remains open. Department AI stays Phase 2 Coming Soon. Full backup/security/handover checks remain open. See [dashboard requirements](docs/DASHBOARD.md).


## Approved scope update — Linda and portal addresses

Amit has approved bringing the former Phase 2 Gemini assistant into the current build. **Linda, your Philexcel AI Assistant**, will answer from authorized department and Company Shared documents with source links. Earlier Phase 2 Coming Soon instructions are superseded as a scheduling decision; they do not imply AI is live. See [portal and Linda implementation requirements](docs/PORTALS-AND-LINDA.md) and the [unconnected design preview](linda-preview.html).

Enrollment, Department/Linda, Axon IT and delegated Admin entry points are specified in that document. Authentication, live Gemini API, permission-aware indexing, runtime deployment and all privileged dashboard functions remain pending. Seven Cloud Sync connections are user-reported configured; only the Company Shared NAS-to-cloud small-file test is user-confirmed. Staff cloud membership remains pending identity confirmation. Board remains excluded.

## Portal implementation package

The [portal source and Singapore deployment guide](portal/README.md) now includes Linda, per-user/admin AI controls, Executive all-HUB scope (Board excluded), enrollment downloads and a fixed trial starting 22 October 2026, expiring 21 November 2026 at 06:36:05 UTC+08:00. Nine local tests pass. This is source code, not a live deployed service; credentials, hosting, staff mapping, real provider tests, installer signing and device UAT are pending.


## Latest daily handover — 22 October 2026

See [Philexcel Daily Progress and UAT Handover](docs/PHILEXCEL-DAILY-PROGRESS-2026-10-22.md) for verified Windows mapping tests, cPanel portal deployment, Synology user/group access, Recycle Bin ACL audit, and remaining rollout gates.

- **Verified:** Clean Windows SMB state; batch-mapped CompanyShared `Z:` with successful read/write/delete test; server-side cPanel portal tests **33 passed** at reported Git revision `17e8437`; Ian has been added to Synology `administrators` and membership read back.
- **Configured in Git, not yet fully reverified live:** Enrollment portal downloads the exact account-local **v5.7 DSM Access Sync** Windows batch, replacing v5.6 in the route without fallback. User upload to cPanel was shown; new live download, byte/hash verification, and DSM group-change Windows UAT remain open.
- **Delegation in progress:** Camille's DSM `Local user and group management` role was selected onscreen, but saved status and her own login were not demonstrated; the native role also permits ordinary user/group deletion. She has inherited RW in Marketing and CompanyShared; read-only access across all folders is **not granted**.
- **Security open items:** Public UAT installer may embed staff directory; audit before distributing broadly. Check per-user effective share/Recycle Bin permissions, NAS relocation, Cloud Sync reverse/conflict/restore and independent backup.

Historical preliminary status sections above are preserved as chronology, not a statement of current acceptance.
