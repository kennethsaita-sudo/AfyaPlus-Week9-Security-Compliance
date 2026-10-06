import os
import jwt
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from controls.injection_guard import guard
from controls.rbac import require_permission
from controls.resolve_secrets import load_secrets
from controls.redact_then_hash import write_audit

SECRETS = load_secrets()  # fail closed at boot
app = FastAPI(title="AfyaPlus Week 9 Secure Triage")

class TriageRequest(BaseModel):
    message: str = Field(min_length=3, max_length=2000)


def authenticate(authorization: str | None) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Bearer token required")
    try:
        return jwt.decode(authorization[7:], SECRETS["JWT_SECRET"], algorithms=["HS256"], options={"require": ["exp", "sub", "role"]})
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid or expired token")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/triage")
def triage(body: TriageRequest, authorization: str | None = Header(default=None)):
    claims = authenticate(authorization)
    try:
        require_permission(str(claims.get("role", "")), "triage:submit")
        guard(body.message)
    except PermissionError as exc:
        raise HTTPException(403, str(exc))
    except ValueError as exc:
        write_audit(str(claims["sub"]), "triage.submit", "/triage", "blocked", body.message)
        raise HTTPException(400, str(exc))
    write_audit(str(claims["sub"]), "triage.submit", "/triage", "allowed", body.message)
    return {"status": "accepted", "advisory_only": True}
