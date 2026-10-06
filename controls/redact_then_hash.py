import hashlib, json, os, re, uuid
from datetime import datetime, timezone
from pathlib import Path

REDACTIONS = [
    (re.compile(r"Bearer\s+[A-Za-z0-9._~+\-/]+=*", re.I), "Bearer [REDACTED]"),
    (re.compile(r"\b\d{7,12}\b"), "[ID_REDACTED]"),
    (re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"), "[EMAIL_REDACTED]"),
]

def redact(value: str) -> str:
    for pattern, replacement in REDACTIONS:
        value = pattern.sub(replacement, value)
    return value

def hash_payload(payload: str, salt: str | None = None) -> str:
    salt = salt or os.getenv("AUDIT_HASH_SALT", "local-lab-salt")
    return hashlib.sha256((salt + redact(payload)).encode()).hexdigest()

def write_audit(actor: str, action: str, resource: str, outcome: str, payload: str, path="logs/audit.jsonl") -> dict:
    safe_actor = redact(actor)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trace_id": str(uuid.uuid4()),
        "actor": safe_actor,
        "action": action,
        "resource": resource,
        "outcome": outcome,
        "payload_hash": hash_payload(payload),
    }
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, separators=(",", ":")) + "\n")
    return record

if __name__ == "__main__":
    line = write_audit("user@example.org", "triage.submit", "/triage", "allowed", "Bearer abc.def.ghi ID 12345678")
    assert "example.org" not in json.dumps(line)
    assert "abc.def.ghi" not in json.dumps(line)
    print(json.dumps(line))
