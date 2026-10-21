# PHILEXCEL HUB — Standard NAS drive assignments

**Source:** Philexcel Site Visit & Equipment, 20 October 2026. Staff currently use a shared Z: drive hosted on an Admin PC; preserve it until backup, migration verification and formal cutover sign-off.

| Letter | New NAS SMB share | Department | Initial authorized access |
|---|---|---|---|
| **Z:** | `CompanyShared` | Company Shared | Read/Write for approved staff |
| **X:** | `Executive` | Executive | Read/Write for approved executives |
| **H:** | `AdminHR` | Administration / HR | Read/Write for approved members |
| **M:** | `Marketing` | Marketing | Read/Write for approved members |
| **R:** | `AdminMarketing` | Administration / Marketing | Read/Write for approved members |
| **F:** | `FinancePurchasing` | Accounting / Finance / Purchasing | Read/Write for approved members |
| **E:** | `Engineering` | Engineering | Read/Write for approved members |

These are proposed new share names to configure in Synology DSM, not names found on an already-configured NAS. The six groups and the initial staff list are provisional until approved. Only map approved shares to each person; never provide every user every department drive.

## Windows staff setup

Download the reviewed script: [Map-HubShares.ps1](../scripts/Map-HubShares.ps1). Run on the user's Windows PC in normal user context:

```powershell
# Preview: Marketing plus approved Company Shared
.\scripts\Map-HubShares.ps1 -NasHost PHILEXCEL-NAS -Departments Marketing -IncludeShared
# Apply only after verifying the employee, NAS shares and unused drive letters
.\scripts\Map-HubShares.ps1 -NasHost PHILEXCEL-NAS -Departments Marketing -IncludeShared -Apply -PromptForCredentials
```

For a user approved in two departments: `-Departments Marketing,AdminMarketing`. Never copy passwords into scripts; staff use their own NAS account. For permanent connections, verify mappings survive reboot/re-login. The script refuses to overwrite occupied drive letters, notably legacy Z:.

## Existing Z: cutover procedure

1. Record the old mapped Z: target privately. Do not disclose LAN addresses on public GitHub.
2. Back up existing Admin-PC shared data and confirm recovery.
3. Create `CompanyShared` on NAS, copy approved files, validate folder/file counts and sample contents.
4. Confirm department/user access on NAS with negative tests.
5. Get Philexcel written approval for cutover.
6. Have Axon explicitly retire the old mapping during each PC's scheduled change; only then run the staff mapping script.
7. Keep old source intact until retention and decommission are approved.

No automatic Z: replacement, deletion or migration is performed by the mapping script.

**Private configuration record:** [Amit's PhilexcelHUB register](https://docs.google.com/document/d/1sl62oz4k16-TaB0ieEfKYXCMGKrt-vidcTIKR-CjX4E/edit) — all real IPs, hostnames, staff assignments, screenshots and tests. Actual passwords and recovery keys belong in the encrypted vault, not Drive or GitHub.
