import os
import subprocess
import tempfile
import datetime
from pathlib import Path

# FIXED IMPORTS
from backend.app.settings import settings
from backend.app.audit import log_admin_action


# NEW: Render persistent backup folder
BACKUP_DIR = Path(os.getenv("BACKUP_DIR", "/var/data/backups"))
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup_database_to_s3(tag='daily'):
    """Creates a local database backup. S3 disabled until AWS is configured."""
    
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise RuntimeError('DATABASE_URL not set')

    # Create a temporary dump
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.sql')
    tmp.close()

    dump_cmd = f"pg_dump {db_url} -Fc -f {tmp.name}"
    res = os.system(dump_cmd)
    if res != 0:
        raise RuntimeError("pg_dump failed")

    # Save to Render backup directory
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    local_filename = BACKUP_DIR / f"backup_{timestamp}_{tag}.dump"
    os.replace(tmp.name, local_filename)

    # S3 upload removed because AWS is not configured yet
    return {"ok": True, "stored": str(local_filename)}


def create_backup():
    """Used by /admin/backup/download endpoint."""
    result = backup_database_to_s3(tag="manual")
    return Path(result["stored"])
