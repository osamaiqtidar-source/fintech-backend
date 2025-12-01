
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session, select
from ..deps import get_current_admin
from ..db import SessionLocal
from .. import models_extra, models
from ..cert_store import store_blob

router = APIRouter()

@router.post("/einvoice/provider/add")
def add_provider(country: str, provider_name: str, type: str = "B", endpoint_url: str = None, creds: str = None):
    db: Session = SessionLocal()
    p = models_extra.EInvoiceProvider(country=country.upper(), provider_name=provider_name, type=type, endpoint_url=endpoint_url)
    db.add(p); db.commit(); db.refresh(p)
    return {"ok": True, "provider_id": p.id}

@router.post("/companies/{company_id}/einvoice/generate-csr")
def generate_csr(company_id: int, admin = Depends(get_current_admin)):
    # generate CSR and private key, store private key as blob, return CSR PEM text
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.x509 import NameOID
    import cryptography.x509 as x509
    import datetime
    from ..cert_store import store_blob
    db = SessionLocal()
    c = db.get(models.Company, company_id)
    if not c:
        raise HTTPException(404, "Company not found")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    key_pem = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, c.name),
    ])).sign(key, hashes.SHA256())
    csr_pem = csr.public_bytes(serialization.Encoding.PEM)
    blob_id = store_blob(key_pem, f"company_{company_id}_priv.pem")
    # store CompanyZatcaConfig row
    cz = models_extra.CompanyZatcaConfig(company_id=company_id, private_key_blob_id=blob_id, status="csr_generated")
    db.add(cz); db.commit(); db.refresh(cz)
    return {"csr": csr_pem.decode(), "blob_id": blob_id}

@router.post("/companies/{company_id}/einvoice/upload-certificate")
async def upload_certificate(company_id: int, file: UploadFile = File(...), csid: str = None, admin = Depends(get_current_admin)):
    db: Session = SessionLocal()
    c = db.get(models.Company, company_id)
    if not c:
        raise HTTPException(404, "Company not found")
    content = await file.read()
    blob_id = store_blob(content, f"company_{company_id}_cert.pem")
    cz = db.exec(select(models_extra.CompanyZatcaConfig).where(models_extra.CompanyZatcaConfig.company_id==company_id)).first()
    if not cz:
        cz = models_extra.CompanyZatcaConfig(company_id=company_id, certificate_blob_id=blob_id, csid=csid, status="cert_uploaded")
    else:
        cz.certificate_blob_id = blob_id
        cz.csid = csid
        cz.status = "cert_uploaded"
    db.add(cz); db.commit(); db.refresh(cz)
    return {"ok": True, "blob_id": blob_id}
