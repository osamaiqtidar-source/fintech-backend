
# Expanded sqlmodel stub
class _Meta:
    def create_all(self, engine=None):
        pass

class SQLModel:
    metadata = _Meta()
    def __init_subclass__(cls, *args, **kwargs):
        return super().__init_subclass__()

def create_engine(*args, **kwargs):
    return object()

def declarative_base():
    class Base:
        metadata = _Meta()
    return Base

def Field(*args, **kwargs):
    return None

def Column(*args, **kwargs):
    return None

# SQL query helpers
def select(*args, **kwargs):
    class _Sel:
        def where(self, *a, **k): return self
        def join(self, *a, **k): return self
    return _Sel()

def and_(*args, **kwargs): return True
def or_(*args, **kwargs): return True

__all__ = [
    "SQLModel", "create_engine", "declarative_base",
    "Field", "Column", "select", "and_", "or_"
]
