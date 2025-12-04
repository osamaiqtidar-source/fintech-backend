
# Full FastAPI responses stub
class Response:
    def __init__(self, content=None, status_code=200, media_type=None):
        self.content = content

class JSONResponse(Response):
    def __init__(self, content=None, status_code=200):
        super().__init__(content, status_code)

class FileResponse(Response):
    def __init__(self, path, media_type=None, filename=None):
        super().__init__(path)

class StreamingResponse(Response):
    def __init__(self, content, media_type=None):
        super().__init__(content)

# Export them clearly for "from fastapi.responses import X"
__all__ = ["Response", "JSONResponse", "FileResponse", "StreamingResponse"]
