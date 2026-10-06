import hashlib, json
from pathlib import Path

FIXTURE = {"subject-001": {"triage_messages": ["msg-101"], "mcp_queries": ["query-201"]}}

def lookup(subject_id: str) -> dict:
    return {"subject_id_hash": hashlib.sha256(subject_id.encode()).hexdigest(), "records": FIXTURE.get(subject_id, {}), "owner": "AfyaPlus Privacy Owner", "legal_review": "pending"}

if __name__ == "__main__":
    result = lookup("subject-001")
    assert result["records"]
    print(json.dumps(result))
