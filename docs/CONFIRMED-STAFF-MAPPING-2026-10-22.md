# Confirmed staff account mapping

Updated 22 October 2026 from Amit's explicit account confirmations. This supersedes earlier initial-based guesses. Latest update: NAS output and Amit's subsequent PowerShell completion confirm all 18 staff memberships applied. Effective-access testing remains separate.

| Name | Microsoft sign in | Department | Existing NAS login | SharePoint memberships |
|---|---|---|---|---|
| Ian | IanPackham@PhilexcelBusinessPark.onmicrosoft.com | Executive | Ian | Applied |
| Tess | mcunanan@philexcel.com | Administration-HR | Tess | Applied |
| Aliza | acalaguas@philexcel.com | Administration-HR | Aliza | Applied |
| Seatiel | slumbang@philexcel.com | Administration-HR | Seatiel | Applied |
| Camille | cnaguit@philexcel.com | Marketing | Camille | Applied |
| Chloe | ccastillo@philexcel.com | Administration-Marketing | Chloe | Applied |
| Clark | cgutierrez@philexcel.com | Administration-Marketing | Clark | Applied |
| Jhojie | jsoriano@philexcel.com | Finance-Purchasing | Jhojie | Applied |
| Kevin | kgutierrez@philexcel.com | Finance-Purchasing | Kevin | Applied |
| Anne | agozum@philexcel.com | Finance-Purchasing | Ann | Applied |
| Rose | rmacaraeg@philexcel.com | Finance-Purchasing | Rose | Applied |
| Nello | npineda@philexcel.com | Finance-Purchasing | Nello | Applied |
| Rommel | rpanganiban@philexcel.com | Engineering | Rommel | Applied |
| Rowell | rtalens@philexcel.com | Engineering | Rowell | Applied |
| Mavel | mbarcia@philexcel.com | Engineering | Mavel | Applied |
| Evann | lasencio@philexcel.com | Engineering | Evain | Applied |
| James | jpureza@philexcel.com | Engineering | James | Applied |
| Cris | myumul@philexcel.com | Engineering | Cris | Applied |

## Administrator and access policy

Hub: hub@philexcel.com; NAS administrator login philexcelhub. Hub owner access is applied across the seven HUB libraries. Every approved staff account receives its own department and Company-Shared. Ian's Executive group has Contribute across all seven libraries. Executive & Board remains excluded from Linda.

## Latest completion and remaining checks

- jsoriano@philexcel.com belongs to Jhojie. Duplicate Jannie removed from NAS; Jhojie retained. Amit confirmed 21 final local accounts.
- Anne retains NAS login Ann; Evann retains NAS login Evain. Their display names and email mappings are confirmed.
- All 18 staff NAS email/department updates and own-department plus Company-Shared memberships verified in Amit's terminal output. Ian additionally belongs to every department group.
- Full confirmed SharePoint roster membership script reported completed by Amit in PowerShell 7. Hub remains owner; Executive has Contribute across all seven HUB libraries.
- Enrollment register completed 22 October by Spencer: 18 staff plus HUB verified against the correct Microsoft tenant (19 unique enabled Member identities), privately imported into the portal, and post-import HUB and Camille Microsoft enrollment sign-ins passed. The server-side importer preserved existing portal roles; HUB's separate admin role still requires explicit authorization. See AMIT-COMMISSIONING-2026-10-22.md for evidence.
- Spencer's **manual** Windows SMB mapping and readability tests passed for seven shares at Amit's office on 22 October; Camille's own/shared read/write passed. Full signed Windows helper, Mac Finder, office-network workstation UAT, per-user effective permission/denial tests, and SharePoint direct-grant/sharing-link review remain pending. Membership and manual mappings alone do not certify access isolation.
- Do not assign additional directory accounts or executives by inference. Do not put passwords in Git.

