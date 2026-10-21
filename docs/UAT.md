# PHILEXCEL HUB — Phase 1 on-site UAT
Record tester, date, PASS/FAIL, evidence and remedial actions in the restricted Google Drive register.

| ID | Test | Expected |
|---|---|---|
| 01 | DSM and drives | DS223 recognized, disks healthy, serials recorded |
| 02 | UPS and networking | UPS checked and switch link is 1 Gbps |
| 03 | NAS SMB login | Personal NAS user can connect |
| 04 | Authorized access | Department Read/Write works |
| 05 | Unauthorized access | Other departments are blocked |
| 06 | Read-only permission | Read works, writing denied |
| 07 | New/disabled user | Account change takes effect; files retained |
| 08 | Existing Z: migration | Backup, file verification and business signoff before remapping |
| 09 | Company Shared | Only approved employees access Z: |
| 10 | Drive mapping | Approved letters map; occupied letters never overwritten |
| 11 | SharePoint scope | Company Hub configured; Board excluded |
| 12 | NAS to cloud | Test file appears in SharePoint |
| 13 | Cloud to NAS | Two-way change tested if enabled |
| 14 | Conflict/deletion/recovery | Versions and restore verified |
| 15 | Backup | Independent backup and sample restore work |
| 16 | Offsite support | Tailscale works; no DSM/SSH/SMB public exposure |
| 17 | Axon IT dashboard | IT access only |
| 18 | Philexcel Admin | Changes logged and verified |
| 19 | Department landing pages | Individual passwords; AI Phase 2 Coming Soon |
| 20 | Private record | All site information logged in authorized Google Drive |

**Phase 2 — Coming Soon:** Gemini file search, cross-department isolation, SharePoint source links, AI activity auditing.

Run read-only connectivity report with:
```powershell
.\scripts\Test-HubUAT.ps1 -NasHost PHILEXCEL-NAS
```
Do not include passwords or secret tokens in reports.
