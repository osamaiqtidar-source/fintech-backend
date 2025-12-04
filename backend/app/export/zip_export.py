import io, zipfile
def create_zip_stream(files: dict):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, content in files.items():
            if isinstance(content, str):
                content = content.encode("utf-8")
            elif hasattr(content, "getvalue"):
                content = content.getvalue()
            z.writestr(name, content)
    buf.seek(0)
    return buf
