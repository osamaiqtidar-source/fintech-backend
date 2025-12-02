import os
from pathlib import Path
from .crypto import encrypt_bytes,decrypt_bytes
BLOB_DIR=os.getenv('CERT_BLOB_DIR','/tmp/fintech_certs')
Path(BLOB_DIR).mkdir(parents=True,exist_ok=True)
def store_blob(content:bytes,filename:str)->str:
    blob_id=filename
    p=Path(BLOB_DIR)/blob_id
    p.write_text(encrypt_bytes(content))
    return blob_id
def load_blob(blob_id:str)->bytes:
    p=Path(BLOB_DIR)/blob_id
    if not p.exists():
        raise FileNotFoundError()
    return decrypt_bytes(p.read_text())
