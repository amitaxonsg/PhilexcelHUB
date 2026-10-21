# PHILEXCEL HUB | PHASE 1 TECHNICAL SETUP — SPENCER / AXON
Status: work instructions only. No production operation has been executed. Updated 21 Oct 2026.

## Start here: what we are building
NAS = network attached storage, a dedicated local file server.
SMB = Server Message Block, the Windows file-sharing protocol behind `\\PHILEXCEL-NAS\Marketing`; staff use mapped Windows drives and their personal NAS username/password.
DSM = DiskStation Manager, Synology's NAS operating system and control panel.
Cloud Sync = Synology package that moves selected folder contents between NAS and SharePoint. It is **not a backup**.
Basic storage pool = one HDD, one independent pool/volume. **Proposed: two Basic pools, two volumes, 2 TB each (~4 TB raw total)**. They are not one combined 4 TB volume and have no drive-failure redundancy.
JBOD combines disks without redundancy; RAID 0 stripes and loses pool data when either drive fails; RAID 1 / SHR mirrored makes ~2 TB usable and survives a single disk failure. **Do NOT select RAID 1 by mistake; do NOT select JBOD/RAID 0 unless Axon + Philexcel knowingly approve higher failure blast radius.** Synology DS223 supports Basic, JBOD, RAID 0/1, SHR and Btrfs/ext4. Recommend Btrfs on each Basic volume if supported by the actual DSM build; test snapshot options. Storage selection/formatting destroys disk data; obtain signoff and backup first.

## System roles
AXON IT: technical administration + storage/backups/network/sync/SSH remote service.
PHILEXCEL ADMIN: NAS onboarding/offboarding, access RO/RW/none, groups and audit; no unrestricted DSM/root.
DEPARTMENT: Phase 1 individual-password protected department page with **Phase 2 AI CHATBOT — COMING SOON**, nothing confidential exposed through the preview.
Microsoft 365 identities independent of NAS (no Intune, AD, Entra sync). Separate `hub@philexcel.com` Cloud Sync identity. Board SharePoint excluded.

## Step-by-step onsite procedure (record each result, executor, screenshot and approval in PRIVATE Google Drive)
1. **Physical inventory:** unbox DS223, both WD Red Plus WD20EFPX 2 TB, UPS APC BX1200MI-MS, TP-Link TL-SG1024D and Deco M4 x2. Inspect serials, cables, airflow, placement and electrical/UPS conditions. Never place NAS on floor prone to flooding.
2. **Network:** verify router actual WAN/IP type, CGNAT, LAN subnet/gateway/DNS and unused LAN IP. Configure NAS DHCP reservation at router (do not hardcode address blindly). Plug gigabit NAS port to gigabit switch. Test 1 Gbps negotiated, DNS, internet and NTP. Keep DSM/SSH/SMB unforwarded from WAN. Record actual LAN settings only in private Drive.
3. **Discovery:** on AXON Windows support PC run `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\Get-HubConnectivity.ps1 -NasHost PHILEXCEL-NAS` after reviewing script and substituting known actual NAS hostname/IP. This is read-only. Record port 445/5001/22 findings privately. Disable SSH unless actively needed.
4. **Storage plan:** obtain approval for TWO independent Basic pools/volumes or alternate choice, noting no redundancy. Install drives and DSM; Storage Manager > Storage Pool > Create > Basic using disk 1; create Btrfs volume 1. Repeat for disk 2 / volume 2. Record which shares live on which volume. Do not format until data safety signed off. Enable disk SMART tests, health alerts and Btrfs snapshots if supported; snapshots never replace independent backup.
5. **DSM hardening:** apply tested DSM security updates, correct region/timezone/NTP, HTTPS, strong named IT admin accounts + MFA, separate recovery procedure, firewall allowlist for trusted office LAN and secure support interface. Disable built-in default admin, guest SMB, SMB1 if legacy apps do not require it, unneeded services and broad external access. Keep credentials in vault only.
6. **Shares/groups:** DSM Control Panel > Shared Folder: create Executive, Administration-HR, Marketing, Administration-Marketing, Finance-Purchasing, Engineering and Company-Shared. DSM User & Group: create one group per department and optional RO/RW groups if manager needs both levels. Grant minimum ACLs. Verify effective access, not just group names.
7. **Confirm staff names:** Site register is provisional; spelling of Jhujie/Jannie/Nello/Mavel/Evain requires verification. Executive Ian; Administration/HR Tess, Aliza, Seatiel; Marketing Camille; Admin/Marketing Chloe, Clark; Finance/Purchasing Jhujie, Kevin, Ann, Jannie, Rose, Nello; Engineering Rommel, Rowell, Mavel, Evain, James, Cris. Ben/Joma not assigned yet. Create individually approved NAS accounts; initial **read/write within their approved departments only**. Do not publish staff register to public repo.
8. **SMB + drive mapping:** DSM File Services > SMB enable SMB2/3 minimum where compatible. Test `\\PHILEXCEL-NAS\Marketing` from Windows with a test NAS account. Run `Map-HubDrive.ps1` in PREVIEW mode then `-Apply`; on each PC use employee's own NAS credentials. Check drive collision and reconnection, no hard-coded passwords.
9. **Negative ACL tests:** Finance test account should NOT open Engineering, HR or Executive. Verify Company Shared only for approved users. Permission change preview, re-login and read-only denial should be checked. Do not grant staff the DSM admin role.
10. **Microsoft 365 Hub:** create/license `hub@philexcel.com` in tenant; MFA, least privilege; prepare *Company Hub* SharePoint libraries, excluding Board. Configure explicit SharePoint groups separately. Confirm total quota with live tenant; no need to consider Board's unrelated estimate.
11. **Synology Cloud Sync:** Package Center > Cloud Sync > connect supported Microsoft SharePoint Online using authorized `hub@` identity. Map a non-sensitive test NAS folder to test SharePoint library. Start NAS upload-only. Test uploads/file additions. Then enable two-way only if Cloud Sync version/connector permits and after testing SharePoint edits returning to NAS, name collisions, simultaneous edits, deletes, permissions and version recovery. Set polling (e.g. 3600 seconds for hourly cloud checks), exceptions and bandwidth settings supported by installed version. Verify actual status and alerts; no fake scheduled task or undocumented CLI writes. Cloud Sync does not transfer NAS ACLs to SharePoint.
12. **Remote Axon access:** add Tailscale via a supported Synology package/approved managed support node, restrict device access to Axon accounts and require MFA. Validate offsite access from a NON-office network. No existing VPN or fixed IP. Do not expose SSH/5001/445 to public internet. Record support route and tests in private Drive.
13. **Independent backup:** plan separate versioned/offsite backup (Hyper Backup or approved destination). Verify backup job success plus actual restore of a test file. Storage with no mirrored redundancy requires explicit documented risks and monitoring.
14. **Dashboard Phase 1:** first use native DSM controls. Deploy real dashboard only after privileged Synology operations are verified with previews/logging, account security and server-side authorization; no public static GitHub Pages site can act as an authenticated NAS management system. Axon IT view, Philexcel Admin view and department shells; department AI reads **COMING SOON (PHASE 2)**.
15. **UAT & handover:** use `Test-HubUAT.ps1` to produce PC-side evidence, and complete `docs/UAT-CHECKLIST.md` manually for permission, cloud, restore, WAN and dashboard tests. Sign off by management and Axon.

## PowerShell download and running
1. Download repository ZIP from GitHub > Code > Download ZIP; extract to trusted support PC.
2. Read the .ps1 files before executing; verify current main branch. Open PowerShell 5.1 or PowerShell 7 on Windows; `Set-Location` to the extracted project directory.
3. Prefer per-process `-ExecutionPolicy Bypass` (shown only for local reviewed script launch) rather than machinewide execution policy changes; use `-File` with parameter names.
4. Discovery: `powershell -NoProfile -File .\scripts\Get-HubConnectivity.ps1 -NasHost PHILEXCEL-NAS`
5. Preview mapping: `powershell -NoProfile -File .\scripts\Map-HubDrive.ps1 -NasHost PHILEXCEL-NAS -Share Marketing -DriveLetter M`
6. Apply mapping ONLY when approved: append `-Apply` and enter user's own NAS credentials at prompt.
7. Generate UAT CSV: `powershell -NoProfile -File .\scripts\Test-HubUAT.ps1 -NasHost PHILEXCEL-NAS -Share Company-Shared -OutputCsv .\hub-uat-private.csv`; do not commit output to public GitHub.
8. Any unexpected PowerShell execution policy message: inspect `Get-ExecutionPolicy -List` and ask Axon to review local security policy. Do not disable security software or bypass organizational controls.

## Private working notes
**Google Drive folder:** https://drive.google.com/drive/folders/1fSYazqiP_jbEdeOPxQJVp6BpewiWaLEE
**Spencer register:** https://docs.google.com/document/d/1sl62oz4k16-TaB0ieEfKYXCMGKrt-vidcTIKR-CjX4E/edit
Record IPs, usernames, hostnames, settings, logs, screenshots, results and timestamps ONLY there (restricted access). Actual passwords, private keys, API tokens, recovery codes are in encrypted vault, and only vault references belong in Drive. Public GitHub contains no private details.
