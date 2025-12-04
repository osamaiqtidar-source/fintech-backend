
class Session:
    def __init__(self): pass
    def execute(self, *a, **k): pass
    def commit(self): pass
    def close(self): pass

def sessionmaker(**kwargs):
    def _session():
        return Session()
    return _session
