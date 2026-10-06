# Week 9: AI Security and Compliance

## Overview
This repository secures the AfyaPlus triage API and logistics MCP path built in Weeks 6 to 8. It adds TLS policy checks, fail-closed secret loading, JWT authentication, role-based authorisation, MCP clinic allowlisting, prompt-injection blocking, privacy-safe audit logging, retention and rights-request stubs, and Kenya Data Protection Act alignment artefacts. The non-technical summary is in `manager_brief.md`.

## Repository map
- `app/`: protected FastAPI triage endpoint
- `mcp_server/`: allowlisted, minimum-response `check_stock` tool
- `controls/`: encryption, secrets, RBAC, injection and audit controls
- `compliance/`: inventory, retention, deletion and rights artefacts
- `tests/`: runnable security assertions
- `evidence/`: save screenshots or transcripts here

## Encryption
- TLS evidence: `controls/transit_policy.py`
- Git-ignore proof: `.gitignore` and `controls/check_gitignore.py`
- Fail-closed boot: `controls/resolve_secrets.py` and `app/main.py`
- Secret references: `controls/secret_refs.yaml`
- At-rest fallback design: `controls/kms_twin.json` and encrypted-provider volume notes in `docker-compose.yml`
- Localhost HTTP is a documented lab exception only.

## Access control (including MCP)
- Role matrix: `controls/rbac.py`
- Authentication remains required: JWT validation in `app/main.py`
- Injection guard: `controls/injection_guard.py`, returning HTTP 400 before model/tool use
- Clinic allowlist: `mcp_server/clinics_allowlist.json`
- Minimum MCP response: `mcp_server/server.py`

## Logging
- JSONL path: `logs/audit.jsonl` (generated locally and ignored by git)
- Redaction and hashing: `controls/redact_then_hash.py`
- Required fields: actor, action, resource, outcome and trace ID

## Kenya DPA
- Inventory: `compliance/data_inventory.json`
- Retention: `compliance/retention.json` and `compliance/retention_sweeper.py`
- Preserved deletion record: `compliance/deletion_records.jsonl`
- Rights path and owner: `compliance/rights_lookup.py`; owner is the AfyaPlus Privacy Owner
- `lawful_basis` entries are teaching labels. Legal review pending.

## Manager brief
See `manager_brief.md`. It contains: Risks, Mitigations, Kenya DPA alignment, and What we will not claim. It deliberately avoids absolute security claims and includes the finance recommend-rather-than-decide line.

## Fallbacks declared
- [x] No live Azure Key Vault: local environment injection plus `secret_refs.yaml` and `kms_twin.json`
- [x] No live AWS account: AWS KMS architecture is still represented in `kms_twin.json`
- [x] Local MCP stub: `mcp_server/server.py`
- [x] Legal review pending on `lawful_basis`
- [x] No paid model call is required

## Run in VS Code PowerShell
```powershell
cd C:\path\to\AfyaPlus-Week9-Security-Capstone
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = "."
$env:JWT_SECRET = "change-this-lab-secret-to-a-long-random-value"
pytest -q
python controls\transit_policy.py
python controls\check_gitignore.py
python controls\rbac.py
python controls\injection_guard.py
python controls\redact_then_hash.py
python mcp_server\server.py
python compliance\retention_sweeper.py
python compliance\rights_lookup.py
python -m uvicorn app.main:app --reload
```

## Capture evidence
Take terminal screenshots showing:
1. `pytest -q` passing.
2. `python controls/transit_policy.py` passing, plus a denied cleartext production URL from the tests.
3. `$env:JWT_SECRET=""; python -m uvicorn app.main:app` failing closed.
4. `python controls/check_gitignore.py` passing.
5. `python controls/redact_then_hash.py` producing a line with a hash and no raw token/ID.
6. `python mcp_server/server.py` returning only clinic ID, item, availability and quantity.
7. `python compliance/retention_sweeper.py` and `rights_lookup.py` passing.

## Optional authenticated API test
Generate a short-lived HS256 token containing `sub`, `role` (`partner`), and `exp`, then call `/triage`. The endpoint must return 401 without a token, 403 for an unauthorised role, 400 for override-style input, and 200 for an authorised normal request.

## Checklist
- [x] Secrets not in git
- [x] MCP cannot dump the environment or every clinic
- [x] Unknown roles denied
- [x] JWT remains required on `/triage`
- [x] Audit payloads are redacted then hashed
- [x] Inventory, retention, deletion record and rights path included
- [x] Manager brief is readable by a non-engineer
- [x] Weeks 6 to 8 services locked down
