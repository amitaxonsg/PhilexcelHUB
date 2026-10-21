# PHILEXCEL HUB NAS handover

Commissioning date: 21 October 2026.
Hostname: PHILEXCEL-HUB. Synology DS223, DSM 7.4.1, two 2 TB independent Basic/Btrfs volumes.

The seven approved department shares and groups were configured and verified. Each share has its own Recycle Bin enabled, department users are not restricted to admin-only restore, and Hide Unreadable is off. Representative staff SMB access tests have now passed; see the 22 October checkpoint below.

Configuration is not yet production-ready. QuickConnect remote DSM access is reported complete; disk checks, firewall/admin MFA, shell-support route, backup restoration and Microsoft 365 integration remain open.

The private Google Drive register holds internal IPs, device serials, network details and credential-vault references. No actual passwords belong in GitHub or Google Docs.

## Ports and network policy
| Port | Function | Policy / commissioning |
|---|---|---|
| TCP 22 | SSH | LAN connection verified; admin-only, no direct WAN forwarding |
| TCP 445 | Windows SMB | LAN connection verified; SMB package running with elevated status; no WAN forwarding |
| TCP 5001 | DSM HTTPS | TCP reachability verified; certificate trust still pending |
| TCP 5000 | DSM HTTP | Used during installation; prefer HTTPS and review redirect |
| TCP 443 outbound | Updates, Microsoft 365, Tailscale control | Provider connections pending verification |
| UDP 123 outbound | Time synchronization | NTP settings pending |
| UDP/TCP 53 outbound | DNS | Office DNS settings pending |
| Tailscale outbound UDP (negotiated) | Evaluated private remote connectivity | Installed/enrolled during evaluation; superseded by QuickConnect; cleanup unverified |

Temporary LAN addressing and equipment serials are recorded only in the restricted Drive register. NAS IP will need an approved office DHCP reservation on relocation.

## Approved volume and mapping
| Volume | Share | Local group | Windows drive |
|---|---|---|---|
| 1 | Executive | Executive | X: |
| 1 | AdminHR | Administration-HR | H: |
| 1 | FinancePurchasing | Finance-Purchasing | F: |
| 2 | Marketing | Marketing | M: |
| 2 | AdminMarketing | Administration-Marketing | R: |
| 2 | Engineering | Engineering | E: |
| 2 | CompanyShared | Company-Shared | Z: |

These groups and shares exist, with departmental RW ACLs and administrator entries verified. All seven share Recycle Bins were confirmed enabled; administrator-only off, hide unreadable off. Representative SMB permissions have passed for two department identities; broader UAT remains pending. Preserve the old Admin-PC Z: mapping until cutover signoff.

## Handover runbook
DSM setup via official wizard; storage created as independent Basic/Btrfs volumes; SSH enabled after DSM reset; group provisioning via Synology synogroup and share provisioning via synoshare plus synoacltool. Confirm the result before proceeding. Read-only checks inside the NAS SSH shell:

```sh
hostname
cat /etc.defaults/VERSION
df -h /volume1 /volume2
sudo synodisk --enum -t internal
sudo synogroup --enum local
sudo synoshare --enum ALL
sudo synoshare --get Executive
sudo synoshare --list_acl Executive
sudo synopkg status SMBService
```

Do not rerun disk partitioning or pool creation. Two Basic volumes offer no redundancy; require independent versioned backup and tested restore. Next steps: finish disk checks, security and firewall, verify approved staff identities, test SMB access boundaries, configure Tailscale offsite management, then narrowly scoped Company Hub SharePoint sync (exclude Board), UAT and signed handover. Gemini chatbot remains Phase 2.

## Phase 06 handover — pause after Marketing pilot (21 October 2026)

Spencer reported successful creation of one approved named Marketing test user, membership of the Marketing department group, and login to DSM File Station. Screenshots showed the Marketing share, its separate Recycle Bin, a deleted UAT test folder, and subsequent restoration of the folder including the test text file. **PASS (observed):** pilot login, Marketing folder access, create/upload, deletion to Recycle Bin, restoration. **NOT YET TESTED:** direct access denied to other department shares, SMB login/mapped drive, permissions under a distinct non-Marketing account, password reset, and any production file access. Do not infer security isolation from other shares being absent in File Station.

**Resume next work session:** (1) verify pilot account cannot open Executive/Finance/other share UNC paths while authenticated only as that pilot; (2) test SMB Marketing RW using personal NAS credentials; (3) reconcile approved staff access matrix against the private Microsoft 365 directory and provision additional users only with approval; (4) confirm full disk checks, firewall/HTTPS/admin MFA, independent versioned backup/restore, private Tailscale support, cloud sync and final UAT. Keep legacy Admin-PC Z: drive unchanged pending cutover approval. No further NAS changes were performed after the pilot restoration in this session.


## Current checkpoint — 22 October 2026 (Amit-guided terminal evidence)

This checkpoint supersedes the earlier pending staff provisioning and sample SMB testing notes above. It does not mark the NAS production-ready.

- Seven department/resource groups renamed to the professional names in the allocation table. Group IDs were retained; all seven share ACLs read back with the renamed RW groups and administrator entries. Share paths were not renamed.
- At Amit's instruction, staff accounts now use the 19 first-name logins from the site roster; the 25 unmatched directory-style setup accounts were removed. NAS enumeration returned 22 accounts including three system/support accounts. The private register holds the actual roster and email mappings. Description fields show departments. Four confirmed email addresses retained; unresolved addresses left blank. No Microsoft 365 identity synchronization.
- All 19 staff belong to their department and Company-Shared. Their department and CompanyShared share ACLs provide RW. No general cross-department grant was added.
- PASS: first department pilot performed Windows SMB create/read/edit/delete in own department and CompanyShared; direct browsing of each of the five other department shares returned Access denied.
- PASS: second department pilot authenticated to Engineering; Amit confirmed Engineering and CompanyShared create/read/edit/delete passes. Direct access to Executive, AdminHR, FinancePurchasing, Marketing and AdminMarketing returned Access denied. These are representative tests, not exhaustive per-user acceptance.

### Recycle Bin and administrator requirements

Each of the seven shares retains its own Recycle Bin. Department members can access/restore within their authorized share; the main NAS administrator must be able to inspect and restore across all seven bins. Prior Marketing restore passed; administrator access across every bin and retention/emptying policy still require verification. RecycleBinAdminOnly remains no, HideUnreadable remains no. CompanyShared has its own bin. Recycle Bin is not independent backup.

Amit designates the existing main NAS administrator as the operational admin identity, with the dedicated company Hub Microsoft 365 email as its contact and Cloud Sync identity. Actual account names/address are recorded privately. Local NAS and Microsoft 365 credentials remain independent; cloud credentials/tokens never enter GitHub or client-side dashboards. NAS administrator contact email was updated and verified through synouser readback; administrator remains in administrators and is active.

### Next execution order requested by Amit

1. Remote method revised: QuickConnect selected and remote DSM access reported complete by Amit. Separate shell support and custom dashboard routing remain open. No public DSM/SSH/SMB forwarding.
2. Verify dedicated Hub Microsoft 365 licensing and least-privilege Company Hub access. Configure Synology Cloud Sync for NAS/cloud synchronization: start a test upload-only task, then enable bidirectional sync only after conflict, deletion, version recovery and cloud ACL tests. Board SharePoint excluded. “Dual cloud sync” is interpreted as two-way NAS/cloud synchronization; no second cloud provider has been selected. Sync is not backup.
3. Build exactly three authenticated dashboard roles: Axon IT, Philexcel Admin, Department. Phase 1 department landing page only; AI chatbot remains Phase 2 Coming Soon. Public GitHub Pages remains a preview, not a real NAS admin backend.
4. Complete disk checks, firewall/HTTPS/admin MFA and recovery, UPS/alerts, independent versioned backup/restore, recycle-bin administrator tests, reconnect/mapping tests, then approved migration/cutover and signed handover. Existing office Z: is preserved.


## Remote access and branding update — 22 October 2026

- Tailscale 1.58.2 was installed and enrollment verified during evaluation. Amit subsequently chose QuickConnect because of Tailscale's commercial trial/subscription requirement. Do not treat Tailscale as the accepted ongoing support path. Logout/device removal/package cleanup has not been confirmed.
- QuickConnect was enabled and its DSM login page observed in screenshots. Amit now reports remote access complete. This is user-confirmed completion, not an independent offsite audit; no blanket SSH/SMB or firewall acceptance implied.
- Cloudflare branded shortcut was configured as a proxied redirect-only A record (documentation placeholder 192.0.2.1) and hostname-specific static 302 redirect to QuickConnect. Public DNS lookup earlier returned NXDOMAIN and Cloudflare displayed no issued edge certificate despite Universal SSL enabled. This branded redirect remains unverified; do not mark DNS/TLS repaired without a new test. Actual hostname/endpoint details belong in the private register.
- Philexcel logo-based login wallpaper created and uploaded; revised image places branding middle-left and leaves the right clear for the DSM sign-in panel. Login title/message/footer wording supplied. Desktop wallpaper is a separate per-user Display Preferences setting; final application there is not verified. DSM customized-domain field should remain blank for the redirect-only design.
- Next task: inspect Cloud Sync package, verify Hub Microsoft 365 licensing and Company Hub destination, then pilot the seven department/resource mappings with Board excluded. No live company migration/cutover performed.

## Latest consolidated commissioning record
See [Amit's 22 October commissioning record](AMIT-COMMISSIONING-2026-10-22.md) for completed seven-library SharePoint setup, user-reported bidirectional sync, cPanel account-only deployment preparation, certificate sign-in/consent, and remaining acceptance checks. Earlier Spencer pilot notes above are retained as historical evidence. AI implementation is now a trial requested by Amit, superseding earlier Coming Soon scope; production provider/device UAT is still pending.
