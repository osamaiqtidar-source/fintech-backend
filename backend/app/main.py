from fastapi import FastAPI
from backend.app.db import init_db
from backend.app.routers import auth, admin

app = FastAPI(title="Fintech Backend v25")

# initialize database (create tables)
try:
    init_db()
except Exception as e:
    print("init_db failed:", e)

# include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(admin.router, prefix="/admin")
@app.get("/health")
def health():
    return {"status":"ok"}
