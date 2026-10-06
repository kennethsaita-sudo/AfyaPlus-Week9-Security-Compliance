import json
from pathlib import Path
from controls.rbac import require_permission

_ALLOWLIST = {c["clinic_id"]: c for c in json.loads(Path(__file__).with_name("clinics_allowlist.json").read_text())["clinics"]}
_STOCK = {"CLINIC-NAI-001": {"ORS": 42, "GLOVES": 120}, "CLINIC-MSA-001": {"ORS": 30, "GLOVES": 85}}

def check_stock(clinic_id: str, item: str, role: str) -> dict:
    require_permission(role, "stock:read_allowed_clinic")
    if clinic_id not in _ALLOWLIST:
        raise PermissionError("clinic is not allowlisted")
    item_key = item.strip().upper()
    quantity = _STOCK.get(clinic_id, {}).get(item_key)
    return {"clinic_id": clinic_id, "item": item_key, "available": quantity is not None and quantity > 0, "quantity": quantity}

if __name__ == "__main__":
    print(json.dumps(check_stock("CLINIC-NAI-001", "ORS", "partner")))
