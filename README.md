# PhilexcelHUB — Axon IT project

**Status: planning/starter scripts only, not deployed.**

## Exactly three dashboards
- **Axon IT:** technical NAS management, secure support, cloud sync, backup, audit.
- **Philexcel Admin:** onboard/disable NAS users, assign departments, change read-only/read-write rights, review NAS state, audit.
- **Department:** individual password-protected department landing page in Phase 1; **Gemini AI chatbot — Phase 2 COMING SOON**. Phase 2 will provide authorized SharePoint document answers, suggestions and source links. No staff or infrastructure management.

## Design
Synology DS223, 2 × 2TB disks. Proposed independent Basic volumes for capacity, not redundancy; independent versioned backup required. Six provisional departments: Executive; Administration/HR; Marketing; Administration/Marketing; Accounting/Finance/Purchasing; Engineering; plus Company Shared resource. Initial approved department memberships receive read/write. Verify staff names and permissions before provisioning.

NAS logins independent of Microsoft 365, no Intune/AD/Entra account synchronization. Windows PCs access NAS SMB; Microsoft 365 SharePoint Company Hub is separate for cloud access. hub@philexcel.com is the planned technical sync identity. Board SharePoint excluded. Test Cloud Sync one-way then two-way, simultaneous edits, deletions, versioning and restore. SharePoint authorization configured separately.

Axon remote access: newly configured secure Tailscale path; no existing VPN, no fixed public IP, no DSM/SSH port forwarding.

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
