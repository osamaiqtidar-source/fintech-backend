from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Correct router imports
from backend.app.routers import auth, admin, company_auth, invoices, einvoice, connector, export

app = FastAPI(title="Fintech Backend API", version="1.0.0")

# ----------------------------------------------------
# CORS (allow your frontend etc.)
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # update this later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Include all routers
# ----------------------------------------------------
app.include_router(auth.router)
app.include_router(company_auth.router)
app.include_router(invoices.router)
app.include_router(einvoice.router)
app.include_router(connector.router)
app.include_router(export.router)

# IMPORTANT: include admin router (for backup endpoints)
app.include_router(admin.router)


# ----------------------------------------------------
# Health Check Endpoint
# ----------------------------------------------------
@app.get("/")
def root():
    return {"message": "Fintech Backend API is running"}
