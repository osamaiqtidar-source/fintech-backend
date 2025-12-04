import os
import subprocess
import tempfile
import datetime
from pathlib import Path
from app.settings import settings
from app.audit import log_admin_action

# NOTE:
# boto3 removed because AWS is not used yet.
# When you enable AWS, uncomment boto3 import and S3 upload section.


# NEW: Render persistent backup folder
BACKUP_DIR = Path(os.getenv("BACKUP_DIR", "/var/data/backups"))
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup_database_to_s3(tag='daily'):
    """
    Creates a database backup and stores it locally.
    S3 upload disabled until AWS is configured.
    """

    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise RuntimeError('DATABASE_URL not set')

    # Create local temporary dump
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.sql')
    tmp.close()

    dump_cmd = f"pg_dump {db_url} -Fc -f {tmp.name}"
    res = os.system(dump_cmd)
    if res != 0:
        raise RuntimeError("pg_dump failed")

    # Save a permanent copy to Render Disk
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    local_filename = BACKUP_DIR / f"backup_{timestamp}_{tag}.dump"

    os.replace(tmp.name, local_filename)

    # S3 DISABLED (NO boto3, NO AWS)
    # Future use:
    # if settings.settings.AWS_ACCESS_KEY and settings.settings.BACKUP_BUCKET:
    #     s3 = boto3.client(
    #         's3',
    #         aws_access_key_id=settings.settings.AWS_ACCESS_KEY,
    #         aws_secret_access_key=settings.settings.AWS_SECRET_KEY
    #     )
    #     key = f"backups/{timestamp}_{tag}.dump"
    #     s3.upload_file(str(local_filename), settings.settings.BACKUP_BUCKET, key)
    #     return {'ok': True, 'stored': str(local_filename), 's3_key': key}

    # LOCAL ONLY (free, works on Render with no AWS)
    return {'ok': True, 'stored': str(local_filename)}


# ADD THIS: Function needed by download endpoint
def create_backup():
    """
    Helper for /admin/backup/download to create a backup
    and return its local file path.
    """
    result = backup_database_to_s3(tag="manual")
    return Path(result["stored"])
