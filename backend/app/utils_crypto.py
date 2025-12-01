
import os
from cryptography.fernet import Fernet

FERNET_KEY = os.getenv("EINVOICE_CRYPTO_KEY") or Fernet.generate_key().decode()
fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY,str) else FERNET_KEY)

def encrypt(b: bytes) -> str:
    return fernet.encrypt(b).decode()

def decrypt(s: str) -> bytes:
    return fernet.decrypt(s.encode())
