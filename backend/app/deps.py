
import os
from fastapi import Header, HTTPException

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin-secret-token")

def get_current_admin(x_admin_token: str = Header(None)):
    if x_admin_token is None:
        raise HTTPException(status_code=401, detail="Admin token required")
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return {"admin": True}
