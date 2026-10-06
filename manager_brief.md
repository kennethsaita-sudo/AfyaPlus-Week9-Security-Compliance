# Manager Security Brief

## Risks
The triage service handles health-related messages, so unauthorised access or excessive retention could harm users. A stolen token could be used to call the API. A poorly scoped MCP stock tool could reveal information for clinics that the caller should not see. Prompt-override text could try to bypass normal controls. Logs could also create a second privacy risk if they stored raw tokens or identity numbers.

## Mitigations
`controls/transit_policy.py` refuses cleartext connections to non-localhost partners. `controls/resolve_secrets.py` stops the service from booting when `JWT_SECRET` is absent, while `.gitignore`, `controls/check_gitignore.py`, and `docker-compose.yml` keep secret values out of source control. `controls/rbac.py` limits each role, and `mcp_server/clinics_allowlist.json` limits the clinics accepted by `mcp_server/server.py`. `controls/injection_guard.py` blocks override-style input before a model or tool call. `controls/redact_then_hash.py` creates structured audit records without retaining the raw payload, token, email address, or identity number.

## Kenya DPA alignment
`compliance/data_inventory.json` lists the processing purposes, data categories, owners, teaching lawful-basis labels, and retention periods. `compliance/retention.json` and `compliance/retention_sweeper.py` implement storage limits while preserving `compliance/deletion_records.jsonl`. `compliance/rights_lookup.py` demonstrates how an authorised privacy owner could locate records for an access or erasure request. These are coursework alignment artefacts, not a regulator approval or legal opinion. Legal review is pending.

## What we will not claim
We will not claim that the system is perfectly secure, regulator-approved, or a replacement for clinical judgement. For any future finance use, the AI may recommend information for human review but must not independently decide whether a person receives credit, a transfer, or another financial outcome. Final decisions remain with authorised staff under documented policy.
