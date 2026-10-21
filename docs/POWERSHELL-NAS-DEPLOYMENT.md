# PHILEXCEL NAS — PowerShell-led deployment (21 October 2026)

**State:** inventory automation prepared; no remote changes performed by ChatGPT. Synology DSM 7.4.1, DS223, two independently mounted Basic/Btrfs volumes observed in Spencer's SSH output. Drive diagnostics are not yet proven complete.

## Mandatory security constraints
- This repository is **public**. Never commit internal IPs, actual employee usernames/email lists, credentials, private inventories, device serials, API tokens or generated audit outputs.
- **Urgent:** a prior private configuration register contained a plaintext administrator password and another credential-like value. Rotate any exposed secrets, review sharing and version history, and replace with vault references only.
- No DSM, SMB (TCP 445), or SSH (TCP 22) internet port forwarding.
- No unapproved storage format/RAID changes. Two Basic volumes have **no fault tolerance**; independent versioned backup and a tested restore are required before production use.
- Avoid modifying the in-use legacy Admin-PC `Z:` drive until separate migration approval.
- Validate exact Synology DSM 7.4 CLI/API capabilities before implementing account/share changes; Windows `New-LocalUser` and `New-SmbShare` do not administer the Linux-based NAS.
- Prefer named, independent admin accounts, signed-off group membership and separate break-glass procedure. Avoid shared admin passwords and enable MFA for privileged users before remote access.

## First command (run locally on Windows PowerShell)
From the repository root:

```powershell
.\\scripts\\Get-HubNasInventory.ps1 -NasHost PHILEXCEL-NAS -SshUser axonadmin
```

This is **read-only**, requires Windows OpenSSH and an already enabled LAN-only NAS SSH service. It emits a **private report** under `philexcel-private-audit/`. Never commit or paste unredacted results publicly. It does not enable SMB or provision accounts.

## Authorized NAS sharing specification (proposed pending management sign-off)
| SMB share | Department | Windows letter |
|---|---|---|
| `Executive` | Executive | X: |
| `AdminHR` | Administration / HR | H: |
| `Marketing` | Marketing | M: |
| `AdminMarketing` | Administration / Marketing | R: |
| `FinancePurchasing` | Accounting / Finance / Purchasing | F: |
| `Engineering` | Engineering | E: |
| `CompanyShared` | Approved staff | Z: |

Use separate NAS local accounts (NOT Entra ID synchronized logins); usernames should be derived only from **verified** Microsoft 365 email addresses, under an approved naming policy. A matching email address can be a contact/recovery address but is **not** automatic Microsoft 365 SSO. Confirm DSM mail relay, recovery eligibility and reset workflow before declaring 'forgot password' operational.

## Deployment gates
1. **Inventory:** run audit; privately record model, serials, drive health checks, services, IP plan, DSM build and UPS.
2. **Identity approval:** validate names/emails/departments/permissions with PHILEXCEL management. Keep the roster in restricted Drive; do not place in this public repository.
3. **NAS API/CLI verification:** on this actual DSM build determine supported share, user and group actions with non-mutating help/discovery. Implement reviewed, idempotent PowerShell wrappers with preview mode and per-change approval. Do not use arbitrary sudo scripts.
4. **SMB:** verify package installation and enable via supported DSM interface/API only after validation; confirm TCP 445 is reachable on LAN, blocked on WAN.
5. **Shares / users:** create approved shares and groups; set least-privilege access; test staff RW and cross-department denial.
6. **Remote Axon support:** The project selects **Tailscale**, an encrypted mesh VPN/overlay requiring no existing corporate VPN or inbound port forwarding. It is not accurate to call it 'no VPN technology'. Verify DS223 compatibility, approve the tenant and devices, install package via trusted Synology-supported process, and limit access to Axon support devices; test offsite access. Do not expose admin accounts publicly.
7. **M365:** separately provision and license the approved technical sync account; configure narrowly scoped Company Hub libraries. Board SharePoint stays excluded. Synology local ACLs do not propagate to SharePoint. Test upload, download, conflicts, deletes and recovery.
8. **Backups:** independent versioned backup and tested restore (cloud sync alone is not a backup).
9. **Windows drive mapping:** `scripts/Map-HubShares.ps1` previews by default. Apply only on each verified user's PC after departmental signoff. Preserve legacy Z: until approved cutover.
10. **Dashboards:** Axon IT, PHILEXCEL Admin, department landing page. Gemini AI features are **Phase 2 — Coming Soon**. Current GitHub Pages site is not a live authenticated administration console.

## Existing UAT helper
```powershell
.\\scripts\\Test-HubUAT.ps1 -NasHost PHILEXCEL-NAS -Share Marketing -OutputCsv '.\\philexcel-private-audit\\hub-uat.csv'
```
Use an actual approved share and the correct employee's credentials; this connectivity check does not replace ACL negative tests.

## Status as of 21 October 2026
- DSM installed; SSH login to named account successful; two Basic volumes mounted at `/volume1`, `/volume2`.
- `SMBService` reported **stopped** during SSH audit; do not claim SMB operational.
- Final diagnostic completion, ACLs, staff identities, backup/restore, Tailscale and dashboards remain **unverified/not deployed**.
- Maintain installation timestamps, reviewer and proof in restricted configuration register.
