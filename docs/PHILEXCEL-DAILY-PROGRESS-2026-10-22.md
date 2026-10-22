# Philexcel HUB — Daily Progress and UAT Handover
**Date:** 22 October 2026 (Asia/Manila)  
**Scope:** NAS enrollment, Windows drive-mapping UAT, DSM access delegation, cPanel enrollment portal  
**Evidence:** operator-provided Windows PowerShell, Synology SSH/DSM screenshots, and cPanel shell results. This record distinguishes observed results from unexecuted plans.

## Verified today
| Area | Evidence | Status |
|---|---|---|
| Windows NAS cleanup | Existing SMB sessions were removed; `Get-SmbMapping` empty and `net use` showed no entries. | PASS |
| Initial Windows batch mapping | Test batch mapped `Z:` to `CompanyShared`; SMB `OK`, Explorer visibility, `Test-Path Z:\` true, directory listing passed. | PASS |
| NAS file operations | Dedicated temporary UAT file was written, read, and deleted on `Z:` successfully. | PASS |
| Installer iteration | Double-click AXON .bat UAT progressed through discovery, login, repairs, consent and closing screen; operator approved v5.6 as working. | Operator-reported working; complete regression suite pending |
| Enrollment portal | Git source migrated to two-column automatic/manual instructions, with hostname-based guidance and neutral network notice. | Git updated; post-latest-commit live render not independently evidenced |
| Account-only cPanel deployment | `philexcel` fast-forward Git pull performed using `runuser` from root, with no documented other-account changes; 33 pytest cases passed (2.28 seconds) on server at that checkpoint. | PASS for reported revision `17e8437` |
| Installer selection | Git source now selects uploaded `Philexcel-NAS-Setup-Repair-UAT-v5.7-DSM-Access-Sync.bat` in `/home/philexcel`, no fallback; screenshot shows upload completed. | Git configured; latest pull, live byte check, Windows v5.7 run and DSM group-change UAT pending |
| DSM admin | Ian added to `administrators`; readback lists `admin`, `philexcelhub`, `Ian`. | PASS membership; individual DSM login/MFA pending |
| DSM delegated admin | Camille selected for `Local user and group management` in DSM screenshot, other shown roles unchecked. | Selected; click-OK/save and Camille login verification not evidenced |
| DSM user/group memberships | Camille in Marketing and Company-Shared, Ian in those plus other authorized groups, as shown in `synogroup` readbacks. | VERIFIED |
| NAS share and filesystem ACL inventory | All seven share paths, department RW ACLs, enabled Recycle Bin and group mappings inspected. Recycle Bin directories showed `everyone` ACLs. | Audit complete; effective-access/cross-department tests pending |

## Standard drive map
X: Executive; H: AdminHR; R: AdminMarketing; F: FinancePurchasing; E: Engineering; M: Marketing; Z: CompanyShared.

## Important security and authorization findings
- NAS departmental membership and actual SMB permissions are the source of truth; changing a DSM group must be reflected in mapping UAT. v5.7 intends to probe shares live and flag obsolete mappings but has not been Windows-verified after a group-change event.
- Existing authenticated Windows SMB sessions can cause error 1219 or stale permission results; sessions must only be disconnected after informed approval.
- The public site cannot reliably check a browser visitor's local SMB network. The installer performs host reachability locally; the website displays a neutral notice.
- Current external UAT .bat may contain embedded staff lookup/profile data. Downloadable source remains readable even if the interface hides profile details before sign-in. A public-release privacy review or removal of the embedded roster is outstanding.
- Camille's `Local user and group management` DSM role inherently permits ordinary user/group deletion; it cannot enforce a create/edit-only rule. Other DSM delegation boxes were not selected in the screenshot.
- Camille currently inherits RW access to Marketing and CompanyShared via groups; changing her to read-only and giving broader visibility to confidential department shares are **not done** and require explicit approved ACL design and effective-rights tests.
- `#recycle` folders show an `everyone` ACL in each of seven inspected shares, but this does **not** prove cross-department SMB access; verify effective access/denial before editing DSM-created ACLs.
- NAS storage uses two Basic volumes; Cloud Sync is not an independent backup.

## Next actions / deployment gates
1. Account-scoped pull of latest Git `main` to cPanel `/home/philexcel/apps/philexcel-hub`, then `pytest`, application syntax, and live HTTPS download name/size/hash versus the approved account-local v5.7 file.
2. Run Windows v5.7 under a regular authorized user. Test: first install, rerun with correct mappings, missing drive, wrong drive, wrong password/1219, absent NAS, new DSM group, removed DSM group, and disconnected/missing drive after Windows sign-in; confirm no unrelated drive removed.
3. Prove NAS-side per-user permissions across all seven shares including negative cross-department tests and Recycle Bin restore/denial, and verify actual NAS user in SMB session rather than inferring from local Windows display.
4. Verify Ian's independent DSM login, MFA, and backup admin accountability.
5. Verify Camille's delegated role persisted after clicking OK and login; determine whether built-in delete rights are acceptable. Do not grant full administrator membership. Review her file access as a separate approved change.
6. Retest after the NAS is moved to the client's office: DNS/hostname resolution, SMB port, DHCP reservation, and seven Cloud Sync tasks including reversals/conflict/deletion/restore. Complete separate versioned backup and recovery UAT.
7. Maintain private staff registry, credentials and any real internal IPs outside public Git. Preserve prior v5.6 UAT artifact for rollback.

**Release status:** Windows batch proof of concept, cPanel Python tests (at documented checkpoint), and Ian admin group membership passed. Full DSM entitlement synchronization, file isolation, final live v5.7 deployment, client-office commissioning and rollout approval are pending.
