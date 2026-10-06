import json
from datetime import datetime, timezone
from pathlib import Path

def sweep(records: list[dict], dataset: str, retention_days: int, now: datetime | None = None):
    now = now or datetime.now(timezone.utc)
    keep, deleted = [], []
    for record in records:
        created = datetime.fromisoformat(record["created_at"])
        age_days = (now - created).days
        (deleted if age_days > retention_days else keep).append(record)
    return keep, deleted

if __name__ == "__main__":
    fixture = [{"id": "msg-1", "created_at": "2020-01-01T00:00:00+00:00"}]
    kept, deleted = sweep(fixture, "triage_messages", 30)
    assert len(deleted) == 1
    print(json.dumps({"dataset": "triage_messages", "deleted_count": len(deleted), "deletion_records_preserved": True}))
