# Spencer handover — MUST READ

## Single source of documentation
- **Public GitHub**: code, safe examples, general architecture and deployment instructions only. Never commit confidential operational data.
- **Amit's Google Drive folder:** https://drive.google.com/drive/folders/1fSYazqiP_jbEdeOPxQJVp6BpewiWaLEE
- **Setup register:** https://docs.google.com/document/d/1sl62oz4k16-TaB0ieEfKYXCMGKrt-vidcTIKR-CjX4E/edit
- Share the private register with Spencer (Editor) and only other authorized project participants.

Log actual DSM version, serials, installed disks, NAS private IP and hostname, router LAN/WAN topology, DNS, gateway, DHCP reservation, switch mapping, volume layout, NAS usernames/department memberships, share paths, network tests, Cloud Sync job mappings, SharePoint library permissions, backups, restore results, remote support settings, change timestamps and screenshots **in private Google Drive**.

**Secrets:** Actual passwords, API keys, MFA recovery codes, private keys and tokens must go only into an approved encrypted secrets/password vault. Record only vault item ID and account custodian in the private register. Never send passwords by email or copy them into Drive or public GitHub.

## Dashboards
1. Axon IT: technical support, health, remote support and configuration.
2. Philexcel Admin: NAS employees, departments and RO/RW/none controls.
3. Department users: AI chatbot only with suggestions and original authorized SharePoint file links. Individual password-protected identities. Six proposed department views, provisionally listed in the site visit: Executive; Admin/HR; Marketing; Admin/Marketing; Finance/Purchasing; Engineering. Company Shared document access is separately scoped.

The current index.html is **PUBLIC PREVIEW ONLY**, no real login, no document data and no working Gemini/NAS backend. Do not show it to client as a production password-protected dashboard.

## Deployment prerequisites
Review DS223 DSM packages and APIs before selecting deployment architecture. Confirm approval of volume/no-RAID risk and independent backup. Validate 2-way Cloud Sync with test files, collisions/deletions, link permissions, SharePoint library isolation and restores. No Intune or AD required. Configure Axon secure remote access separately; do not expose DSM/SSH ports. Keep Board SharePoint outside this project.
