
def Depends(x=None): return x
def Header(default=None): return default

class HTTPException(Exception):
    def __init__(self, status_code=None, detail=None):
        self.status_code = status_code
        self.detail = detail

class FastAPI:
    def __init__(self, *a, **kw): pass
    def add_middleware(self, *a, **kw): pass
    def include_router(self, *a, **kw): pass

class APIRouter:
    def __init__(self, *a, **kw): pass
    def get(self, *args, **kw):
        def deco(fn): return fn
        return deco
    def post(self, *args, **kw):
        def deco(fn): return fn
        return deco
    def patch(self, *args, **kw):
        def deco(fn): return fn
        return deco
    def put(self, *args, **kw):
        def deco(fn): return fn
        return deco
    def delete(self, *args, **kw):
        def deco(fn): return fn
        return deco
    def include_router(self, *a, **kw): pass

def Query(default=None, **kw): return default
class BackgroundTasks:
    def __init__(self): pass
# expose submodules
from . import responses as responses
from . import middleware as middleware
from . import status as status
from . import security as security
