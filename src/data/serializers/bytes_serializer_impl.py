import pickle

from infrastructure.ioc_container import service
from .bytes_serializer import BytesSerializer


@service
class BytesSerializerImpl(BytesSerializer):
    def serialize(self, value: object) -> bytes:
        return pickle.dumps(value)
