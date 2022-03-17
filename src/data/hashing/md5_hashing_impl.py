from hashlib import md5

from infrastructure.ioc_container import service
from .md5_hashing import Md5Hashing


@service
class Md5HashingImpl(Md5Hashing):
    def hash(self, value: bytes) -> int:
        hash_object = md5(value)
        hash_bytes = hash_object.digest()
        return int.from_bytes(hash_bytes, 'big')
 
