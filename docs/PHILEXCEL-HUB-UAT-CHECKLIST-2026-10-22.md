# PHILEXCEL HUB — Enrollment & NAS UAT Checklist

**Test lead:** Spencer  
**Date opened:** 22 October 2026  
**Status:** Commissioning / Not approved for full staff rollout  
**Source of truth:** [Portal implementation handover](PORTAL-IMPLEMENTATION-HANDOVER-2026-10-22.md), [Amit commissioning record](AMIT-COMMISSIONING-2026-10-22.md), [confirmed staff mapping](CONFIRMED-STAFF-MAPPING-2026-10-22.md).

**Safety:** Tests must be authorized, use non-sensitive dummy files, avoid credentials/screenshots of secrets, and preserve unrelated drive mappings and existing office data. Application/hosting changes are restricted to the Philexcel account; no server-wide restarts, root-level changes, new ports, or other cPanel customers. Do not confuse test-code passing with actual production acceptance.

## A. Completed and evidenced on 22 October (at Amit's office)

| ID | Test | Result | Evidence / qualification |
|---|---|---|---|
| A01 | Candidate code validation | PASS | 33 Python tests in 2.20 seconds; Mac script shell syntax clean |
| A02 | Deploy Enrollment patch | PASS | Fast-forward from fa7afa8 to 3402b44 as `philexcel`; no service restart reported |
| A03 | Microsoft identity registration | PASS | 18 staff plus HUB (19 distinct enabled Microsoft member identities), private register imported |
| A04 | HUB Microsoft Enrollment sign-in | PASS | Personalized executive folder/drive plan displayed |
| A05 | Camille Microsoft Enrollment sign-in | PASS | Marketing M: and CompanyShared Z: only |
| A06 | Camille NAS account sign-in/own and shared RW | PASS | Folder/file created and edited/saved/reopened in Marketing and CompanyShared |
| A07 | Camille restricted-folder denial | PRELIMINARY | AdminHR and Executive credential/access-denied prompts; complete cross-department user permission matrix remains |
| A08 | Seven temporary manual Windows mappings | PASS | X H M R F E Z mapped with /persistent:no; `Test-Path` true and `Get-ChildItem` readable in normal Windows session |
| A09 | NAS-side SMB identity | NOT VERIFIED | `Get-SmbConnection` showed Windows identity Amit1\\Spencer, not authoritative Synology login identity |
| A10 | Windows helper signing | BLOCKED | Downloaded unsigned checker was blocked by workstation execution policy; no bypass performed |
| A11 | Synology Cloud Sync tasks | STATUS OBSERVED | Seven tasks showed green status; selected Marketing task showed Up to date. Green icons are not seven verified end-to-end transfers |
| A12 | Marketing SharePoint to NAS new file | PRELIMINARY | `This is a Test - Spencer.txt` appeared on both sides; original 0-byte file. Subsequent user reported sync beginning; content parity after modification not independently evidenced yet |

## B. Marketing reverse-sync content acceptance — next immediate test

- [ ] B01: In **SharePoint Marketing**, edit a uniquely named test file and save a non-empty marker; record save time.
- [ ] B02: Close/reopen in SharePoint to confirm the marker persists at the source.
- [ ] B03: In **NAS File Station → Marketing**, refresh and open the same file (not a duplicate/download); verify identical marker.
- [ ] B04: Record Cloud Sync task status and relevant log time; compare with observed arrival time. Do not infer precise sync latency without timestamps.
- [ ] B05: Perform a separate NAS → SharePoint update using a different authorized test file; confirm source/destination contents and timestamps.
- [ ] B06: Clean up only approved UAT files after evidence capture, understanding delete propagation in two-way sync.

**Acceptance:** B01–B05 evidence captured before labeling Marketing bidirectional *content* sync PASS. File presence alone is not sufficient.

## C. Philexcel office installation — 23 October

- [ ] C01: NAS shutdown/transport without interrupting active sync; ensure all tasks idle and equipment inventoried.
- [ ] C02: Physically install NAS, power, LAN and UPS (if available); confirm network topology and final IP/DHCP reservation in **restricted register**, not public Git.
- [ ] C03: Test DSM/HTTPS and SMB/445 from an office workstation; verify correct LAN/VLAN access and DNS/shortcut.
- [ ] C04: Check NAS folder path in portal private config; change **Philexcel-only** configuration only if final address differs, with separate authorization.
- [ ] C05: Test regular staff own-department and CompanyShared read/write and cross-department denials using at least one authorized account per department; don't test privilege boundaries using an admin.
- [ ] C06: Test Ian executive permissions separately; verify NAS identity used for SMB sessions.
- [ ] C07: Re-test office mapping and read/write with the correct individual NAS login; preserve existing unrelated drives and no broad unmap.
- [ ] C08: Record workstation OS, time, share, user role, PASS/FAIL, error and evidence reference without credentials.

## D. Windows/Mac enrollment helper acceptance

- [ ] D01: Sign final Windows helper; verify publisher signature and normal-user launch without lowering execution policy.
- [ ] D02: Check-only leaves all mappings intact; explicit MAP is necessary before any change.
- [ ] D03: New mapping, matching mapping, same share on another letter, unrelated mapping and occupied local letter tested.
- [ ] D04: Conflicting company mapping requires confirmation, validates target before replacement and keeps old path for recovery.
- [ ] D05: Offline NAS, wrong password, cancel, SMB credential conflict and partial failure/rollback tested safely.
- [ ] D06: Mac check-only, CONNECT, existing volume, offline NAS, wrong password, cancellation and manual old-volume review tested on a Mac.
- [ ] D07: Phone/offsite Microsoft 365 SharePoint shortcut and no-cloud-account manual guidance tested.

## E. Portal access/security acceptance

- [ ] E01: Known staff login maps by immutable Microsoft ID to its own approved NAS record, not email/form hints.
- [ ] E02: Valid but unmatched tenant member gets confirmation pending, no personalized helper.
- [ ] E03: Guest, wrong tenant and disabled registration denied.
- [ ] E04: Test session expiry/logout and no cross-user data leakage.
- [ ] E05: Verify HUB's separately approved **portal** admin role; importing records did not grant admin (`roles: []`), and Microsoft/SharePoint ownership alone is insufficient.

## F. Cloud, resilience and next phases

- [ ] F01: Repeat bidirectional file-content test across remaining six SharePoint libraries.
- [ ] F02: Controlled conflict, deletion, retention, versioning and restore tests, with clear approvals; avoid deleting business files.
- [ ] F03: Independent backups, NAS recycle bin restore, security/alerts, UPS readiness and network recovery validated.
- [ ] F04: Verify effective Microsoft SharePoint per-user isolation (membership alone does not prove it); Executive & Board excluded from HUB sync and Linda.
- [ ] F05: Complete Linda citation/retrieval, licensing, Outlook and own OneDrive acceptance separately.
- [ ] F06: Begin Client Admin user-lifecycle implementation **after Enrollment acceptance**; current controls are not live NAS/M365 provisioning.
- [ ] F07: Begin Axon read-only health monitoring after Admin workflow; no live NAS collector claimed.

## Acceptance/sign-off

| Gate | Current decision |
|---|---|
| Account-private code + identity import | PASSED |
| Two live Microsoft login samples | PASSED |
| Local manual Windows 7-share mapping/readability | PASSED |
| Marketing reverse content sync | NOT YET ACCEPTED |
| Philexcel office/actual staff rollout | PENDING |
| Final Enrollment UAT sign-off | PENDING |

**Reviewer/approval:** Amit. **Test execution:** Spencer. Evidence is in the restricted project register/approved screenshots, not embedded in public Git. Current production code deployment and documentation commits are separate; do not merge documentation checklist changes into a claim of live rollout approval.
