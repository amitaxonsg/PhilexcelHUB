# PhilexcelHUB — Axon IT project

**Status: planning/starter scripts only, not deployed.**

## Exactly three dashboards
- **Axon IT:** technical NAS management, secure support, cloud sync, backup, audit.
- **Philexcel Admin:** onboard/disable NAS users, assign departments, change read-only/read-write rights, review NAS state, audit.
- **Department:** individual password-protected login and **AI chatbot only**. Gemini answers, suggests actions, and links to SharePoint files authorized for that person. No staff or infrastructure management.

## Design
Synology DS223, 2 × 2TB disks. Proposed independent Basic volumes for capacity, not redundancy; independent versioned backup required. Six provisional departments: Executive; Administration/HR; Marketing; Administration/Marketing; Accounting/Finance/Purchasing; Engineering; plus Company Shared resource. Initial approved department memberships receive read/write. Verify staff names and permissions before provisioning.

NAS logins independent of Microsoft 365, no Intune/AD/Entra account synchronization. Windows PCs access NAS SMB; Microsoft 365 SharePoint Company Hub is separate for cloud access. hub@philexcel.com is the planned technical sync identity. Board SharePoint excluded. Test Cloud Sync one-way then two-way, simultaneous edits, deletions, versioning and restore. SharePoint authorization configured separately.

Axon remote access: newly configured secure Tailscale path; no existing VPN, no fixed public IP, no DSM/SSH port forwarding.

AI: Gemini API server side + prefiltered SharePoint retrieval, enforce each authenticated user's current department and actual document access before reading and again before returning links. AI read-only initially, no file editing or privileged NAS commands.

## Security
**THIS REPO IS PUBLIC.** No actual passwords, recovery keys, credentials, access tokens, internal IPs, real employee register or company data in GitHub. Private setup configuration in restricted Google Drive; secrets in encrypted vault with vault references only in Drive.

See docs/DEPLOYMENT.md, docs/DASHBOARD.md and scripts/.
