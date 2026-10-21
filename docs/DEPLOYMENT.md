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
