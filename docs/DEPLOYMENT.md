# Spencer step-by-step configuration guide

**Not yet executed. First inspect the actual Synology DS223.** Record completion, screenshots and reviewer in restricted Google Drive.

1. Inventory DS223 serial, two WD Red Plus 2TB drives, firmware, UPS, switch and router; test 1Gbps LAN.
2. Record NAS IP, DHCP scope/reservation, subnet, gateway and DNS privately. Do not publish internal network configuration.
3. Approve proposed two independent Basic volumes, ~4 TB raw total, no RAID redundancy. Plan versioned independent backup and restore test before business migration.
4. Set up DSM, NTP, updates, named Axon admins, separate break-glass account, DSM firewall and MFA. Store secrets in encrypted vault only.
5. Create department shares and group access: Executive, Administration-HR, Marketing, Administration-Marketing, Finance-Purchasing, Engineering; Company Shared. Validate staff spelling and department assignments; default RW within authorized department only.
6. Create local NAS accounts (no Entra sync); test own-group RW and cross-group denial with two test accounts. Check direct and inherited ACLs.
7. On staff PC, use PowerShell mapping helper with each employee's NAS credentials; verify reconnect at login.
8. Set up hub@philexcel.com licensing and restricted Company Hub SharePoint document libraries; exclude Board site. Manage SharePoint permissions separately.
9. Configure Cloud Sync with sample folder NAS-to-cloud first; test cloud edits back to NAS, concurrent edits, conflicts, deletions, exclusions and restores before enabling two-way production.
10. Set up new Tailscale Axon-only support path; no current VPN/static IP. Never expose DSM/SSH/SMB directly to internet.
11. Enable disk, sync and backup alerts; perform restore; document recovery.
12. Deploy tested admin adapter, Philexcel Admin dashboard, Axon IT dashboard and Department AI-only chatbot. Authenticate every user and check role and file access on each request.
13. UAT: onboard, change access preview/verify, disable, group isolation, chatbot unauthorized-file denial, SharePoint source URLs, sync, backup, offsite support. Collect signoff.

## Approved allocation across the two Basic volumes (21 October 2026)

Spencer reports that Amit approved balancing the six departmental shares evenly between the two independent volumes: three departments per volume. The seventh share, `CompanyShared`, is allocated to Volume 2. This balances the number of **departmental shares**, not guaranteed bytes or projected storage consumption. Monitor growth and review if usage differs substantially.

| Volume | Storage pool | Share | Access group | Windows letter |
|---|---|---|---|---|
| Volume 1 | `PHILEXCEL-DISK1` | `Executive` | `grp_executive` | X: |
| Volume 1 | `PHILEXCEL-DISK1` | `AdminHR` | `grp_adminhr` | H: |
| Volume 1 | `PHILEXCEL-DISK1` | `FinancePurchasing` | `grp_finance` | F: |
| Volume 2 | `PHILEXCEL-DISK2` | `Marketing` | `grp_marketing` | M: |
| Volume 2 | `PHILEXCEL-DISK2` | `AdminMarketing` | `grp_adminmarketing` | R: |
| Volume 2 | `PHILEXCEL-DISK2` | `Engineering` | `grp_engineering` | E: |
| Volume 2 | `PHILEXCEL-DISK2` | `CompanyShared` | `grp_companyshared` | Z: |

**Implementation status:** allocation documented, not evidence that shares exist. Verify actual Volume 1/2 placement after creating shares. Both volumes are Basic/Btrfs with no drive-failure redundancy. An independent versioned backup and tested restore remain mandatory. The existing Admin-PC Z: mapping must not be changed without separate migration and cutover approval.

Private Google Drive register fields: timestamp, responsible person, NAS model/serial, DSM build, hostname/IP/subnet/gateway, disk layouts, hardware switch ports, groups, approved user matrix, share permissions, M365 libraries, Cloud Sync settings and last success, Tailscale support method, dashboard URL, backup/restore status, credentials-vault references, audit/change log. **Never store actual passwords or recovery codes in a shared spreadsheet.**

## PHILEXCEL HUB deployment checkpoint — 21 October 2026 (Spencer-reported SSH evidence)

The seven approved local Synology groups were created and verified (`synogroup --enum local` returned 10 total including three built-in groups). After confirmation of volume allocation, Spencer ran Synology `synoshare --add` and `synoacltool -add` commands and supplied output showing **7 shares registered** via `synoshare --enum ALL`. The output showed named departmental group RW ACL entries plus `philexcelhub` and `administrators` for each newly created share. `Executive` was separately inspected earlier.

| Volume | Share | Approved group | Reported creation |
|---|---|---|---|
| 1 | Executive | grp_executive | Created; filesystem/share ACL read back |
| 1 | AdminHR | grp_adminhr | Created; share ACL read back |
| 1 | FinancePurchasing | grp_finance | Created; share ACL read back |
| 2 | Marketing | grp_marketing | Created; share ACL read back |
| 2 | AdminMarketing | grp_adminmarketing | Created; share ACL read back |
| 2 | Engineering | grp_engineering | Created; share ACL read back |
| 2 | CompanyShared | grp_companyshared | Created; share ACL read back |

**Not yet accepted:** independent readback of all share paths and effective access; actual SMB login and cross-department denial using two test users; staff email roster/membership approval and account provisioning; Recycle Bin and hide-unreadable settings (Executive showed both off); full disk-check completion; firewall/MFA; versioned independent backup and restore; Tailscale; SharePoint sync; dashboard deployments; old Admin-PC Z: cutover. Do not mark this project production-ready. Staff/credential details and actual device configuration evidence belong only in restricted Drive.

### Phase 05.7 verification — Spencer's NAS terminal output (21 October 2026)

Independent readback of all seven shares with `synoshare --get` and `synoshare --list_acl` confirmed the approved Volume 1/2 locations, SMB `WinShare=yes`, and the expected per-department Read/Write ACL plus administrator entries. **Configuration verification passed; end-user authorization testing has NOT passed yet.** All seven shares currently report `RecycleBin=no`, `RecycleBinAdminOnly=no`, and `HideUnreadable=no`. Amit subsequently approved enabling a separate Recycle Bin for every share and explicitly keeping HideUnreadable disabled. RecycleBinAdminOnly access policy has not been decided. Apply via supported DSM controls and verify, rather than assuming flags for these toggles. Full disk checks, firewall/MFA, independent backup/restore, staff enrollment, Tailscale, and M365 synchronization remain open.

### Phase 05.8 — Approved Recycle Bin and visibility policy (Amit instruction relayed by Spencer, 21 October 2026)

- Enable **Recycle Bin = yes** independently for each of the seven shares: `Executive`, `AdminHR`, `FinancePurchasing`, `Marketing`, `AdminMarketing`, `Engineering`, and `CompanyShared`. Each share has its own Synology `#recycle` folder; do not create a single company-wide bin.
- Keep **Hide unreadable subfolders and files = no** for all shares. This is explicitly approved, and is **not** permission to broaden access. Maintain per-department ACL isolation and test denied access for unauthorized users.
- **Recycle Bin administrator-only restriction:** Amit subsequently approved department users accessing and restoring deleted files within their own authorized department share. Set `RecycleBinAdminOnly=no` for all seven shares. No cross-department permissions are granted; verify with actual user accounts.
- Use supported DSM controls and verify with `sudo synoshare --get SHARE`; target `RecycleBin=yes`, `RecycleBinAdminOnly=no`, and `HideUnreadable=no`. The current CLI help did not document these controls.
- Retention/auto-empty schedule and restore UAT remain to be approved/tested. Department-level access to its own recycle bin is approved; test the resulting DSM/SMB ACLs and recovery behavior. Recycle Bin is not an independent backup.
- **Status:** approval documented; not yet enabled or verified on the NAS.

### Phase 05.9 — Recycle Bin user-access approval (Amit decision relayed by Spencer)

Amit approved departmental access to each department's **own** Recycle Bin. Keep Recycle Bin enabled and administrator-only restriction disabled for each of the seven existing shares, while leaving HideUnreadable disabled as previously approved. A user can only restore items if their own NAS identity has permissions on the corresponding share / `#recycle` content; do not assume a top-level setting alone proves isolation. Test authorized restore and cross-department denial with different staff test identities. `CompanyShared` uses its own approved shared-access group. No Recycle Bin should be used as the only backup.

**Current implementation status:** Documentation approved; no evidence that these Recycle Bin toggles have yet been applied or verified on the NAS. Configure in DSM > Control Panel > Shared Folder > Edit > General (labels may vary by build), then verify with `sudo synoshare --get SHARE` and user-level UAT. Do not grant `users` or `everyone` broad ACLs.

### Phase 05.10 — Recycle Bin settings verified (21 October 2026, Spencer SSH output)

Spencer provided `sudo synoshare --get` readbacks for all seven shares. Each reports **RecycleBin=yes**, **RecycleBinAdminOnly=no**, **HideUnreadable=no**. This matches Amit's approved policy for Executive, AdminHR, FinancePurchasing, Marketing, AdminMarketing, Engineering and CompanyShared. Configuration is complete for these settings, but user-specific restore capability and negative cross-department access remain **untested**. No Recycle Bin retention/emptying schedule is yet approved. This does not replace independent versioned backups.
