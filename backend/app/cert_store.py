
import os
from pathlib import Path
from .utils_crypto import encrypt, decrypt
BLOB_DIR = os.getenv("CERT_BLOB_DIR", "/tmp/fintech_certs")
Path(BLOB_DIR).mkdir(parents=True, exist_ok=True)

def store_blob(content: bytes, filename: str) -> str:
    blob_id = filename
    p = Path(BLOB_DIR) / blob_id
    p.write_text(encrypt(content))
    return blob_id

def load_blob(blob_id: str) -> bytes:
    p = Path(BLOB_DIR) / blob_id
    if not p.exists():
        raise FileNotFoundError()
    return decrypt(p.read_text())
