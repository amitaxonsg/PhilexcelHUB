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

## October 22 installer selection correction

Amit explicitly selected the previously tested `Philexcel-NAS-Setup-Repair-UAT-v5.6-AXON.bat`, uploaded through cPanel File Manager to `/home/philexcel/`. The application `/enroll/installer` endpoint now serves **that exact server-local file** rather than the alternate generic Git batch file. There is no fallback; missing/empty file returns 503. Historical generic Git batch remains as a rollback/development artifact, not the live download.

**Security caution:** v5.6 UAT may embed a readable staff/NAS username directory. Public browser access to the batch can expose that directory; NAS password/ACL validation within the script does not protect text inside downloaded script. Perform explicit privacy approval or remove embedded staff register before general distribution. A public site cannot reliably attest same-LAN presence.

After deploying the new Git revision, validate file existence, ownership, response attachment filename, byte count and checksum against the approved upload before announcing release. New endpoint code and landing page changes do not take effect until pulled to the server; no server-side pull is claimed in this Git update.



## Enrollment network advisory patch

The green enrollment introduction now has a prominent, accessible `NAS connection not verified` notice immediately underneath it. It explains that employees should join the approved office LAN/Wi-Fi or contact support, while keeping download and manual instructions visible. The notice deliberately does **not** claim a successful or failed live LAN probe. NAS reachability is checked by the Windows batch file after download, not by the remote Singapore-hosted web browser.

This is a presentation-only change to `portal/templates/enroll.html` and `portal/static/style.css`, plus an enrollment test assertion. The approved v5.6 account-local batch download route, batch file, NAS permissions, and other portals are unchanged. Apply by fast-forward pulling main as account user `philexcel`, running the existing test suite, and checking `https://enroll.philexcel.com/enroll`. Do not modify other hosting accounts, server settings or DNS.


## Follow-up correction: connectivity status (22 October 2026)

Removed the permanent `NAS connection not verified` warning from the public enrollment page. This warning was not based on a live test and incorrectly suggested users on the office LAN were out of range. Replaced it with neutral `Office NAS connectivity check` guidance below the green header. The employee's **local AXON v5.6 batch installer** remains responsible for checking `PHILEXCEL-HUB` reachability and stopping safely if unavailable.

No browser-side ping or NAS probing was implemented: the public cPanel-hosted site cannot execute a reliable ping from the visitor's Windows machine. The existing two-column instructions, manual mapping paths, and approved account-local v5.6 download route remain unchanged. After account-scoped Git pull, run the test suite and inspect the enrollment page. The new test checks that the static warning is absent.
