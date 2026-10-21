# PHILEXCEL HUB — SITE ACCEPTANCE TEST (UAT)
**Phase 1 acceptance. Phase 2 Gemini tests are reserved (COMING SOON).**
Site date: ______  Executed by: ______  Witness: ______  Result: ______
For each test enter PASS / FAIL / BLOCKED / N/A, date, proof/screenshot path in restricted Drive, and remediation ticket. No passwords in evidence.

| ID | Test / expected result | Result | Evidence / issue |
|---|---|---|---|
| P1-01 | DS223 serial and DSM version recorded; disks healthy | | |
| P1-02 | NAS power through UPS; shutdown/alerts tested safely | | |
| P1-03 | Gigabit link negotiated; LAN DNS/gateway/DHCP reservation confirmed | | |
| P1-04 | DSM login HTTPS only; admin MFA enabled and default admin disabled | | |
| P1-05 | Storage choice signed off; two Basic pools/volumes configured if selected; free space verified | | |
| P1-06 | SMB works from office PC with own NAS user credentials | | |
| P1-07 | Read/write: authorized Finance test user can create/edit/delete safe test file in Finance | | |
| P1-08 | Denial: Finance test user cannot open HR/Executive/Engineering files | | |
| P1-09 | Access change RO: selected test account cannot modify/delete files | | |
| P1-10 | Add user and disable test user; disabled account denied after sessions expire | | |
| P1-11 | Approved Company Shared access works; unapproved access fails | | |
| P1-12 | PowerShell mapped drive preview, apply, reconnect and collision test | | |
| P1-13 | SharePoint Company Hub library access is scoped; Board excluded | | |
| P1-14 | NAS -> SharePoint test file successfully uploaded | | |
| P1-15 | Cloud -> NAS edit returns if two-way enabled; polling delay measured | | |
| P1-16 | Conflicting simultaneous edits handled/documented; no silent overwrites | | |
| P1-17 | Deletion propagation and SharePoint version recovery tested | | |
| P1-18 | Cloud Sync failure/recovery and alerts visible; no false green status | | |
| P1-19 | Independent backup succeeds; actual test-file restore verified | | |
| P1-20 | Axon secure remote support from outside office works without inbound DSM/SSH port forward | | |
| P1-21 | WAN test confirms DSM/SMB/SSH not publicly accessible | | |
| P1-22 | Axon IT/Philexcel Admin/Department role isolation tested in real authenticated application | | |
| P1-23 | Each of six department pages visible; AI labeled Phase 2 Coming Soon | | |
| P1-24 | Admin change request preview, explicit apply, post-change NAS ACL verification and audit | | |
| P1-25 | Setup record, screenshot references, vault references, manager approval and staff training recorded in private Drive | | |

## Phase 2 — coming soon; NOT required for Phase 1 signoff
| ID | Planned future test |
|---|---|
| P2-01 | Gemini receives ONLY permission-filtered document snippets |
| P2-02 | Cross-department document requests denied before search |
| P2-03 | Returned SharePoint source link accessible only with existing SharePoint permission |
| P2-04 | Revoking a user's access immediately invalidates AI search authorization |
| P2-05 | AI auditing, rate limits, model data handling and prompt-injection tests |

## Sign-off
Axon IT technician: __________  Philexcel admin: __________  Approver: __________
Outstanding defects / next action: __________________________________
