import datetime
from enum import Enum
from typing import Any, AsyncGenerator, Generic, Optional, Type, TypeVar, TypedDict


class System(Enum):
    HUB = "hub"
    MONITORING = "monitor"
    SUBSURFACE = "subsurface"


class MessageType(Enum):
    # subsurface
    MOISTURE_READING = "moisture_reading"
    # monitoring
    MOTION_DETECTED = "motion_detected"


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


class PackageDirection(Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


# subsurface definitions


class IMoistureData(TypedDict):
    moisture: float
    timestamp: Optional[datetime.datetime]


class MoistureReadingMessage(Message[IMoistureData]):
    moisture: float
    timestamp: Optional[datetime.datetime]

    def __init__(self, moisture: float, timestamp: Optional[datetime.datetime] = None):
        super().__init__(
            MessageType.MOISTURE_READING,
            System.SUBSURFACE,
            {"moisture": moisture, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: IMessage[IMoistureData]):
        return MoistureReadingMessage(
            message["data"]["moisture"], message["data"]["timestamp"]
        )


# monitoring definitions


class IMotionDetected(TypedDict):
    human: bool
    timestamp: Optional[datetime.datetime]


class MotionDetected(Message[IMotionDetected]):
    human: bool
    timestamp: Optional[datetime.datetime]

    def __init__(self, human: bool, timestamp: Optional[datetime.datetime] = None):
        super().__init__(
            MessageType.MOTION_DETECTED,
            System.MONITORING,
            {"human": human, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: IMessage[IMotionDetected]):
        return MotionDetected(message["data"]["human"], message["data"]["timestamp"])
