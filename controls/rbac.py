ROLE_PERMISSIONS = {
    "partner": {"triage:submit", "stock:read_allowed_clinic"},
    "operations": {"triage:submit", "stock:read_allowed_clinic", "audit:read"},
}

def is_allowed(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())

def require_permission(role: str, permission: str) -> None:
    if not is_allowed(role, permission):
        raise PermissionError(f"role={role!r} denied permission={permission!r}")

if __name__ == "__main__":
    assert is_allowed("partner", "triage:submit")
    assert not is_allowed("partner", "audit:read")
    assert not is_allowed("unknown", "triage:submit")
    print("PASS: role matrix denies unknown and over-scoped access")
