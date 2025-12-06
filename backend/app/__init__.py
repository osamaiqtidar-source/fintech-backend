# Export commonly used models so "from backend.app import User" works

from .models.user import User
from .models.company import Company, AdminCompanyAccess

# Re-export optional modules
try:
    from . import models_extra
except Exception:
    models_extra = None

try:
    from . import models_einvoice
except Exception:
    models_einvoice = None

try:
    from . import cert_store
except Exception:
    cert_store = None

__all__ = [
    "User",
    "Company",
    "AdminCompanyAccess",
    "models_extra",
    "models_einvoice",
    "cert_store",
]
