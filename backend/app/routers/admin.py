from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from backend.app.deps import get_current_actor
from backend.app.services.backup_service import (
    backup_database_to_s3,
    create_backup,
)
from backend.app.models import User, Company, AdminCompanyAccess

router = APIRouter(prefix="/admin", tags=["admin"])


# -----------------------------------
# Admin: List all companies
# -----------------------------------
@router.get("/companies")
def list_companies(actor=Depends(get_current_actor)):
    if actor["type"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can access this")

    from backend.app.db import session

    return session.query(Company).all()


# -----------------------------------
# Admin: Get single company
# -----------------------------------
@router.get("/companies/{company_id}")
def get_company(company_id: int, actor=Depends(get_current_actor)):
    if actor["type"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can access this")

    from backend.app.db import session

    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


# -----------------------------------
# Admin: Link admin to company
# -----------------------------------
@router.post("/companies/{company_id}/grant")
def grant_company_access(company_id: int, admin_id: int, actor=Depends(get_current_actor)):
    if actor["type"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can access this")

    from backend.app.db import session

    access = AdminCompanyAccess(admin_id=admin_id, company_id=company_id)
    session.add(access)
    session.commit()
    session.refresh(access)

    return {"ok": True, "access": access}


# -----------------------------------
# Admin: Trigger S3 Backup (kept for later use)
# -----------------------------------
@router.post("/backup-now")
def backup_now(actor=Depends(get_current_actor)):
    if actor["type"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can trigger backups")

    result = backup_database_to_s3()
    return {"ok": True, "result": result}


# ----------------------------------------------------
# ✔ NEW: Download a backup file (no AWS required)
# ----------------------------------------------------
@router.get("/backup/download", summary="Download database backup")
def download_backup(actor=Depends(get_current_actor)):
    if actor["type"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can download backups")

    backup_path = create_backup()
    if not backup_path:
        raise HTTPException(status_code=500, detail="Backup creation failed")

    return FileResponse(
        path=backup_path,
        filename=backup_path.name,
        media_type="application/octet-stream",
    )
