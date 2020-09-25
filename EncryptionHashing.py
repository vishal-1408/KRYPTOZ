import hashlib

def hash_str(credential):
    hashed_string=hashlib.sha256(str.encode(credential))
    hashed_string_hex = hashed_string.digest()
    return hashed_string_hex