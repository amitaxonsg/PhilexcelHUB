# Enrollment landing-page refresh — 22 October 2026

## Git changes
- Public `/enroll` now displays an AXON-branded two-column page: automatic Windows setup/repair on the left, manual File Explorer mapping on the right.
- New explanatory File Explorer illustration: `portal/static/map-drive-guide.svg`.
- New `/enroll/installer` endpoint downloads a standalone batch file without Microsoft 365 authentication.
- New generic public batch at `portal/downloads/Philexcel-NAS-Setup-Repair.bat`; no employee roster, NAS passwords, tokens or privileged account credentials are embedded.
- Original UAT v5.6 was verified by Spencer in conversation, but is **not** the new public artifact because the UAT variant carries an internal staff lookup list.
- Existing Microsoft 365 protected endpoints stay in source for the other portals. Old Windows downloads are not linked from the new enrollment page; do not delete rollback assets before deployment verification.

## Security and network limitations
A public Singapore-hosted website **cannot reliably detect** whether a visitor is on the LAN with `PHILEXCEL-HUB`. The browser does not offer a trustworthy, secure local-LAN-attestation API. The download is therefore publicly viewable; the Windows assistant checks hostname/SMB port 445 locally and requires personal NAS credentials. The NAS ACLs—not an installer or website—enforce share permission.

The generic build infers accessible folders via actual SMB access tests; it does **not** claim to know staff full names or departments. A production employee-specific welcome screen requires a secure NAS-side or portal-side authenticated profile API, which remains an outstanding feature. Generic installer is new code and requires full Windows UAT; do not represent it as the already tested v5.6.

## Standard letters
X: Executive; H: AdminHR; R: AdminMarketing; F: FinancePurchasing; E: Engineering; M: Marketing; Z: CompanyShared. A standard drive letter does not imply access. Do not expose the private staff register to public downloads.

## Deployment checklist — Axon cPanel account only
1. Back up the existing portal application and public entry-point files under the `philexcel` account.
2. Pull `amitaxonsg/PhilexcelHUB` `main` into `/home/philexcel/apps/philexcel-hub` as `philexcel` after checking for local modifications. Do not touch other accounts or Apache/NGINX configuration.
3. Run `cd /home/philexcel/apps/philexcel-hub/portal && ../.venv/bin/python -m pytest -q tests`, confirming the repository's actual venv path first.
4. Open `https://enroll.philexcel.com/enroll`; inspect desktop/mobile layout, illustration, BAT download headers, and HTTPS.
5. Run the generic BAT on a normal Windows user workstation: first-time mapping, existing correct maps, incorrect map consent, wrong NAS password, SMB error 1219, occupied local drive, NAS unreachable, per-user denied shares, rerun/repair and sign-in persistence.
6. Retire/archive old publicly linked Windows .ps1 downloads only after download integrity and UAT pass. Keep Git history and backup.
7. Roll back only the account's portal files if tests fail.

**Deployment state:** Git changes committed; Axon server pull, live browser rendering, and new Windows script UAT were not performed from this conversation. No remote shell or hosting-account deployment session was connected.
