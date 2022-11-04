from enum import Enum
from typing import Any, TypedDict


class MessageType(Enum):
    ACKNOWLEDGE = "acknowledge"
    DATA = "data"
    FILE = "file"
    CONTROL = "control"


class System(Enum):
    HUB = "hub"
    CAMERA = "camera"
    SUBSURFACE = "subsurface"


class Message(TypedDict):
    name: str
    type: MessageType
    system: System


class GenericMessage(Message):
    data: Any


class FileMessage(Message):
    data: bytes


# subsurface


class MoistureData(TypedDict):
    moisture: float
    timestamp: int


class MoistureReading(Message):
    data: MoistureData


# monitoring


class MonitorEvent(Enum):
    VISITOR_DETECTED = "visitor_detected"


class MonitorEventMessage(Message):
    event: MonitorEvent
