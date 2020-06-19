from hashlib import sha256


def hash_somehow(target: str) -> int:
    hash_obj = sha256()
    hash_obj.update(bytearray(target.encode('utf-8')))
    return int.from_bytes(hash_obj.digest(), 'big')
