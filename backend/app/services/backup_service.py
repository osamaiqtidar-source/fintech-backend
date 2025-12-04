import os, subprocess, tempfile, boto3, datetime
from app.settings import settings
from app.audit import log_admin_action
def backup_database_to_s3(tag='daily'):
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise RuntimeError('DATABASE_URL not set')
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.sql')
    tmp.close()
    dump_cmd = f"pg_dump {db_url} -Fc -f {tmp.name}"
    res = os.system(dump_cmd)
    if res != 0:
        raise RuntimeError('pg_dump failed')
    # upload to s3 if configured
    if settings.settings.AWS_ACCESS_KEY and settings.settings.BACKUP_BUCKET:
        s3 = boto3.client('s3', aws_access_key_id=settings.settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.settings.AWS_SECRET_KEY)
        key = f"backups/{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{tag}.dump"
        s3.upload_file(tmp.name, settings.settings.BACKUP_BUCKET, key)
        os.unlink(tmp.name)
        return {'ok': True, 's3_key': key}
    else:
        return {'ok': True, 'file': tmp.name}
