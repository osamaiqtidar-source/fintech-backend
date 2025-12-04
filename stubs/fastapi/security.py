
class OAuth2PasswordBearer:
    def __init__(self, tokenUrl=None): pass

class HTTPAuthorizationCredentials:
    def __init__(self, scheme=None, credentials=None):
        self.scheme = scheme
        self.credentials = credentials

class HTTPBearer:
    def __init__(self, auto_error=True): pass
