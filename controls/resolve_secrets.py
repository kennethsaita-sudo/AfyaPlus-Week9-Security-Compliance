import os

def resolve_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"FATAL: required secret {name} is missing")
    return value

def load_secrets() -> dict[str, str]:
    return {"JWT_SECRET": resolve_required("JWT_SECRET")}

if __name__ == "__main__":
    load_secrets()
    print("PASS: required secrets resolved without printing values")
