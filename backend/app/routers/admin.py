from fastapi import APIRouter, Depends
from backend.app.deps import require_admin, require_super_admin
router = APIRouter()

@router.get('/companies')
def list_companies(current=Depends(require_admin)):
    return {'companies': []}

@router.post('/create-admin')
def create_admin(current=Depends(require_super_admin)):
    return {'message': 'create admin allowed only for super admin'}
