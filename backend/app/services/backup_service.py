import os
import subprocess
import tempfile
import datetime
from pathlib import Path

# FIXED IMPORTS — your project uses backend.app.*
from backend.app.settings import settings
from backend.app.audit import log_admin_action


# ----------------------------------------------------
# NOTE:
# Render FREE tier cannot write to /var/data (requires paid disk)
# So we use /tmp/backups — this is writable and safe.
# ----------------------------------------------------

BACKUP_DIR = Path(os.getenv("BACKUP_DIR", "/tmp/backups"))
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup_database_to_s3(tag="daily"):
    """
    Create a PostgreSQL database backup and store it locally.
    S3 upload is DISABLED until AWS credentials are added.
    """

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not set")

    # --------------------------------------------
    # 1) Create a temporary pg_dump output
    # --------------------------------------------
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".sql")
    tmp.close()

    dump_cmd = f"pg_dump {db_url} -Fc -f {tmp.name}"
    res = os.system(dump_cmd)

    if res != 0:
        raise RuntimeError("pg_dump failed")

    # --------------------------------------------
    # 2) Move backup to local directory (/tmp/backups)
    # --------------------------------------------
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    local_filename = BACKUP_DIR / f"backup_{timestamp}_{tag}.dump"

    os.replace(tmp.name, local_filename)

    # --------------------------------------------
    # 3) AWS S3 upload DISABLED until you add AWS
    # --------------------------------------------
    # if settings.AWS_ACCESS_KEY and settings.BACKUP_BUCKET:
    #     import boto3
    #     s3 = boto3.client(
    #         "s3",
    #         aws_access_key_id=settings.AWS_ACCESS_KEY,
    #         aws_secret_access_key=settings.AWS_SECRET_KEY
    #     )
    #     key = f"backups/{timestamp}_{tag}.dump"
    #     s3.upload_file(str(local_filename), settings.BACKUP_BUCKET, key)
    #     return {"ok": True, "stored": str(local_filename), "s3_key": key}

    # Local-only (Render safe)
    return {"ok": True, "stored": str(local_filename)}


def create_backup():
    """
    Used by /admin/backup/download.
    Returns path to a local backup file.
    """
    result = backup_database_to_s3(tag="manual")
    return Path(result["stored"])
