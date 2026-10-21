# PHILEXCEL HUB NAS handover

Commissioning date: 21 October 2026.
Hostname: PHILEXCEL-HUB. Synology DS223, DSM 7.4.1, two 2 TB independent Basic/Btrfs volumes.

The seven approved department shares and groups were configured and verified. Each share has its own Recycle Bin enabled, department users are not restricted to admin-only restore, and Hide Unreadable is off. Staff access tests are still outstanding.

Configuration is not yet production-ready. Disk checks, firewall, secure remote support, backup restoration, and Microsoft 365 integration remain to be completed.

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
| Tailscale outbound UDP (negotiated) | Private remote connectivity | Not installed; no inbound router forwarding |

Temporary LAN addressing and equipment serials are recorded only in the restricted Drive register. NAS IP will need an approved office DHCP reservation on relocation.

## Approved volume and mapping
| Volume | Share | Local group | Windows drive |
|---|---|---|---|
| 1 | Executive | grp_executive | X: |
| 1 | AdminHR | grp_adminhr | H: |
| 1 | FinancePurchasing | grp_finance | F: |
| 2 | Marketing | grp_marketing | M: |
| 2 | AdminMarketing | grp_adminmarketing | R: |
| 2 | Engineering | grp_engineering | E: |
| 2 | CompanyShared | grp_companyshared | Z: |

These groups and shares exist, with departmental RW ACLs and administrator entries verified. All seven share Recycle Bins were confirmed enabled; administrator-only off, hide unreadable off. Effective staff SMB permissions are not yet tested. Preserve the old Admin-PC Z: mapping until cutover signoff.

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
