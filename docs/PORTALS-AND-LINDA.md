# Philexcel portals and Linda implementation plan

Approved by Amit in the current commissioning session. This is an implementation specification, not evidence of live deployment.

## Addresses
| Host | Purpose | Current evidence |
| --- | --- | --- |
| enroll.philexcel.com | Microsoft 365 staff sign-in and signed Windows mapping download | Planned |
| ai.philexcel.com | Department workspace and Linda chat | Planned; linda-preview.html is a public design preview only |
| axon.philexcel.com | Restricted Axon IT support tasks, diagnostics, sync/backup status and audit | Planned |
| admin.philexcel.com | Delegated Philexcel staff/access administration | Planned |
| data.philexcel.com | Redirect to Philexcel HUB SharePoint | User reports working |
| hub.philexcel.com | NAS shortcut | Prior DNS/TLS issue; current verification pending |

These are three dashboard roles (Axon IT, Philexcel Admin, Department); enrollment and file shortcuts are supporting entry points.

## Linda, your Philexcel AI Assistant
Amit requests a basic department chat interface backed by Gemini and indexed documents. This supersedes a landing-page-only UI design. Amit subsequently authorized building and activating Linda now, bringing the former Phase 2 work into the current implementation scope. Live AI remains unimplemented and must not be presented as operational until connected and tested. Use the company Hub-managed Google Cloud/Gemini project identity; a mailbox alone is not an API credential. Select the Gemini model at deployment after checking available models and pricing. Keep API credentials on the server.

### Request path
1. Authenticate Microsoft 365 identities through Entra authorization-code flow, validate issuer, audience, tenant and session.
2. Resolve approved identity-to-department mapping on the server. A browser department choice never grants access.
3. Check current SharePoint document authorization for the requesting person. NAS credentials and SharePoint identities remain separate.
4. Retrieve chunks only from permitted department libraries and Company-Shared. Exclude Executive & Board at ingestion AND retrieval.
5. Recheck authorization before sending source excerpts to Gemini and before returning source links. Reject the request if identity or permissions cannot be checked.
6. Treat retrieved documents as untrusted content, never as commands or instructions that override assistant rules.
7. Return a grounded answer with document title and source link; if evidence is missing, say so rather than fabricate.
8. No file writes, NAS commands or access administration through Linda initially.

### Index lifecycle
Use seven separately scoped indexes/namespaces or equally enforced metadata partitions. Record library, item ID, version, source URL and ACL provenance. Process additions, changes, deletion and permission changes. Purge deleted documents, vectors and caches. Permission-filter retrieval before generation; never retrieve across all departments and ask Gemini to hide unauthorized content. Cache by identity/permission scope and invalidate on access changes. Avoid logging document contents or tokens. Confirm client data handling, project region, retention and API billing configuration before production indexing.

### UI
Department cards open Linda's basic chatbox. Live UI exposes authorized departments only, displays the current scope and provides cited source links. Company Shared supplements each department scope. Public preview uses no company files or credentials and has disabled submission. Do not add Gemini keys to HTML or Git.

## Enrollment and Z: cutover
Use a signed, versioned PowerShell download; browser sign-in cannot silently execute local code. Validate Microsoft 365 session server side and resolve the approved NAS username. Request personal NAS credentials securely on the PC; never embed them or send them to the website. Verify network access and SMB permissions before mapping. Offsite use SharePoint unless a separately approved private NAS route exists.

Map department letters X/H/F/M/R/E and Company Shared Z. If Z is already mapped elsewhere, preserve it and report cutover pending. Only an explicit cutover mode may record the old mapping, replace it and verify the result, with rollback instructions. Never include a shared administrator secret or store passwords in scripts, Git or ordinary logs. Reconnect per-user drives at sign-in. Existing script must be reviewed against these requirements before staff deployment.

## Commissioning checkpoint
- SharePoint HUB created; seven libraries exist with versioning and unique permissions.
- Readback: corresponding group Contribute; HUB Owners and commissioning administrator Full Control. Groups remain empty pending staff identity confirmation.
- Seven Cloud Sync connections reported completed by Amit, bidirectional. Company Shared NAS-to-cloud small-file test confirmed by user. Reverse-direction, department mapping, conflict, deletion and recovery UAT remain pending.
- Cloud Sync file-size filter set to zero by user; SharePoint service limits still apply. Recycle folder excluded by Cloud Sync rules, not replicated as an ordinary library folder.
- No real company migration/cutover, independent backup acceptance or production readiness implied.
- Provisioning app uses delegated SharePoint AllSites.FullControl; review/revoke commissioning access after setup. The Linda runtime must have its own narrowly scoped identity, not reuse the provisioning app.

## Next implementation gates
Inspect hosting/runtime and approved deployment credentials; confirm Entra app, HTTPS callback URLs and Google project/API availability. Complete mapping script review and one-PC UAT. Implement authenticated portal backend, authorization and index lifecycle before enabling chat. Never publish privileged actions as a static client-side dashboard.


## AI dashboard trial — approved
- One company-wide 30-day trial for Linda and the AI dashboard. It is not a new trial per employee, browser or login.
- Start only on the first deliberate production activation, after the live backend is configured. No start date is assigned by writing this specification or opening a design preview.
- Persist trial_started_at and trial_expires_at server side in UTC; expiry is exactly 30 days (720 hours) after activation. Display local date/time and remaining days in the dashboard.
- Before each chat, retrieval or AI API request, enforce current time < trial_expires_at. At expiry return HTTP 403 with code TRIAL_EXPIRED; do not retrieve documents or call Gemini.
- UI during trial: “30-day AI trial” with remaining days and expiry date. At expiry: “Trial Expired” and “Your 30-day trial of Linda, your Philexcel AI Assistant, has ended. Contact Axon 1Pro Solutions to continue.” Disable question submission and provide a support link.
- Reloads, local clock changes, account changes, reinstalling or clearing browser storage must not restart or extend the trial. Only an authorized Axon administrator can activate, extend or renew it, with an audit event.
- NAS SMB, enrollment, SharePoint files, data shortcut, existing Cloud Sync and non-AI administrative/support functions remain available according to their normal permissions. No automatic charge or renewal is configured.
- Required tests: one instant before expiry, exact expiry, after expiry, a second staff account, browser storage reset, and file access after AI expiry.
- Trial enforcement is specified but not live; secure backend and persistent store still need implementation.
