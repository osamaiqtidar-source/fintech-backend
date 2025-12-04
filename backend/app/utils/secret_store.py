from app.cert_store import store_blob, load_blob
import json
def save_provider_credentials(provider_id:int, credentials:dict) -> str:
    blob = json.dumps(credentials).encode('utf-8')
    blob_name = f"einvoice_provider_{provider_id}.enc"
    try:
        store_blob(blob, blob_name)
    except Exception:
        # fallback: store raw as file (less secure) - for dev only
        with open('/tmp/' + blob_name, 'wb') as f:
            f.write(blob)
    return blob_name
def load_provider_credentials(ref:str) -> dict:
    try:
        raw = load_blob(ref)
        return json.loads(raw.decode('utf-8'))
    except Exception:
        # fallback: try /tmp
        with open('/tmp/' + ref, 'rb') as f:
            return json.loads(f.read().decode('utf-8'))
