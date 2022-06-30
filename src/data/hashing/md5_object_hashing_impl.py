from infrastructure.ioc_container import service
from data.serializers import BytesSerializer
from data.hashing import Md5Hashing
from .md5_object_hashing import Md5ObjectHashing


@service
class Md5ObjectHashingImpl(Md5ObjectHashing):
    def __init__(self, bytes_serializer: BytesSerializer, md5_hashing: Md5Hashing) -> None:
        self.__bytes_serializer = bytes_serializer
        self.__md5_hashing = md5_hashing

    def hash(self, value: object) -> int:
        value_bytes = self.__bytes_serializer.serialize(value)
        return self.__md5_hashing.hash(value_bytes)
