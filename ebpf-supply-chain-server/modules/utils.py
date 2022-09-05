import hashlib

def get_md5(data: str) -> str:
    m = hashlib.md5(data.encode("UTF-8"))
    return m.hexdigest()
