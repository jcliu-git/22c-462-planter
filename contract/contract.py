import datetime
from enum import Enum
from typing import Any, Generic, Optional, Type, TypeVar, TypedDict


class MessageType(Enum):
    ACKNOWLEDGE = "acknowledge"
    DATA = "data"
    FILE = "file"
    CONTROL = "control"


class System(Enum):
    HUB = "hub"
    CAMERA = "camera"
    SUBSURFACE = "subsurface"


# top level definitions

DataType = TypeVar("DataType")


class IMessage(TypedDict, Generic[DataType]):
    type: MessageType
    system: System
    data: DataType


class Message(Generic[DataType]):
    type: MessageType
    system: System
    data: DataType

    def __init__(self, type: MessageType, system: System, data: DataType):
        self.type = type
        self.system = system
        self.data = data

    @staticmethod
    def fromJson(message: IMessage[DataType]):
        return Message[DataType](message["type"], message["system"], message["data"])


class GenericMessage(Message[Any]):
    data: Any


class FileMessage(Message[bytes]):
    data: bytes


# subsurface definitions


class IMoistureData(TypedDict):
    moisture: float
    timestamp: Optional[datetime.datetime]


class MoistureReadingMessage(Message[IMoistureData]):
    moisture: float
    timestamp: Optional[datetime.datetime]

    def __init__(self, moisture: float, timestamp: Optional[datetime.datetime] = None):
        super().__init__(
            MessageType.DATA,
            System.SUBSURFACE,
            {"moisture": moisture, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: IMessage[IMoistureData]):
        return MoistureReadingMessage(
            message["data"]["moisture"], message["data"]["timestamp"]
        )
