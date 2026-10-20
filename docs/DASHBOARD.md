# Dashboard requirements

## Axon IT
DSM version/disk health, Cloud Sync status, backup and restore state, secure Tailscale status, NAS user and permission administration, full audit. All privileged actions previewed, allowlisted, verified and logged.

## Philexcel Admin
Employees: create/disable, never auto-delete. Departments: assign users to approved groups. Access: RO/RW/none with before-after preview; actual NAS ACL checks including unexpected direct grants. View storage, cloud sync and audit. No DSM root or SSH access.

## Department chatbot (AI ONLY)
Each person uses individual username/password and sees a chatbot scoped to approved departments. Show answer, source document link, and optional suggestions. No NAS management. If assigned to multiple departments, the backend checks actual authorized scope each request. Gemini is called only after authorization-filtered SharePoint retrieval. No shared broad-access hub@ credential exposed to users. Explicitly respect SharePoint permissions; NAS ACLs don't propagate to SharePoint. Initially read-only; no AI write/edit actions.

Security: secure password hashes, TLS, MFA for admins, session expiry, rate limits, CSRF protection, access logs, prompt-injection resistance, auditing and tests for cross-department leakage. Do not run web server as unrestricted root. Gemini API tokens remain server-side.

Dashboard hosting depends on DSM package availability and DS223 performance; keep DSM UI unmodified.
