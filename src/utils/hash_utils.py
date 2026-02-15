import hashlib

def generate_hashes(file_bytes):
    return {
        "md5": hashlib.md5(file_bytes).hexdigest(),
        "sha256": hashlib.sha256(file_bytes).hexdigest()
    }
