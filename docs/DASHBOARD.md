# Dashboard requirements

Status: requirements and public preview only; no authenticated production dashboard deployed. Updated 22 October 2026.

## Exactly three dashboard roles

| Role | Phase 1 scope | Restrictions |
|---|---|---|
| Axon IT | NAS health/storage, remote support, sync and backup status, privileged configuration, user/group administration and audit | Axon-authorized identities/devices only; preview, verify and log privileged changes |
| Philexcel Admin | Staff create/disable, approved department assignment, RO/RW/none controls, all departmental Recycle Bin views/restores, sync/storage status and audit | Authenticated delegated controls; no unrestricted root or SSH shell |
| Department | Personal login, own authorized department and Company Shared landing page, authorized own-share Recycle Bin access/restore | No other department data or admin controls; AI is Phase 2 Coming Soon |

The operational main NAS administrator is philexcelhub, with hub@philexcel.com designated as contact email and Microsoft 365 Cloud Sync identity by Amit. NAS and M365 authentication are separate. This designation does not grant dashboard users SSH/root privileges. Separate Axon support identities and MFA remain required before production use.

## Recycle Bins

Each share has its own bin: Executive, AdminHR, FinancePurchasing, Marketing, AdminMarketing, Engineering and CompanyShared. Staff restore only within authorized shares; administrator can view/restore across all seven. Keep RecycleBin enabled, administrator-only restriction off, HideUnreadable off. Verify real user and admin restore operations. Retention/auto-empty policy pending; Recycle Bin is not independent backup.

## Philexcel Admin controls

Employees: create/disable; never automatically delete business accounts or data. Groups: assign only approved departments; RO/RW/none with before-after preview, actual effective ACL checks and unexpected-direct-grant detection. Current departmental groups are RW; RO controls require implementation and UAT before claiming support. Display actual state and freshness; unknown/unavailable never means healthy.

## Phase 2 department chatbot — Coming Soon

Each individual sees only authorized department scope. Backend checks current permissions on every request, including multi-department access. Gemini runs only after authorization-filtered SharePoint retrieval. Return authorized original document links and optional suggestions. Respect SharePoint authorization independently of NAS ACLs. Read-only initially; no AI edits or privileged NAS operations. Never expose the broad cloud sync identity or tokens to staff.

## Deployment and security

Amit selected Synology QuickConnect instead of Tailscale and reports remote DSM access complete. QuickConnect covers DSM/supported Synology apps, not general SSH/SMB tunneling or arbitrary custom dashboard hosting. Axon shell access and custom dashboard transport remain separate design tasks. Tailscale evaluation enrollment must be logged out/removed if unused; cleanup not yet verified. No public DSM/SSH/SMB forwarding. Determine dashboard host only after inspecting actual DS223 packages and backend support; do not assume Docker availability. Public GitHub Pages is preview only, not production authentication or a privileged NAS proxy. Keep DSM UI unmodified. Use least-privilege backend, TLS, secure sessions/password handling, admin MFA, CSRF/rate protections and audit logs. Cloud credentials remain server-side. Test all three roles and cross-department denial before handover.
