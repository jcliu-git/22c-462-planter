import datetime
from enum import Enum
from json import dumps, JSONEncoder
from typing import Any, AsyncGenerator, Generic, Optional, Type, TypeVar, TypedDict

class ContractEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Message):
            return o.__dict__

class System(str, Enum):
    HUB = "hub"
    MONITORING = "monitor"
    SUBSURFACE = "subsurface"
    CAMERA = "camera"
    IRRIGATION = "irrigation"

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)
    


class MessageType(str, Enum):
    # generics
    DATA = "data"
    FILE_MESSAGE = "file"

    # subsurface
    MOISTURE_READING = "moisture_reading"
    # monitoring
    MOTION_DETECTED = "motion_detected"
    # camera
    # irrigation

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

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

    def __repr__(self):
        return dumps(self.__dict__)

    @staticmethod
    def fromJson(message: IMessage[DataType]):
        return Message[DataType](message["type"], message["system"], message["data"])


class GenericMessage(Message[Any]):
    data: Any

class PackageDirection(Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class DataMessage(GenericMessage):
    def __init__(self, system, data):
        super().__init__(
            MessageType.DATA,
            system,
            data
        )

# file

class FileMetadata(TypedDict):
    filename: str
    path: str
    filesize: int
    data: Any

class FileMessage(Message[FileMetadata]):
    filename: str
    path: str
    filesize: int

    def __init__(self, system: System, destination_path: str, filesize: int, data = None):
        filename = destination_path.split("/")[-1]
        path = destination_path[:len(destination_path)-len(filename)]
        super().__init__(
            MessageType.FILE_MESSAGE,
            system,
            {
                "filename": filename,
                "path": path,
                "filesize": filesize,
                "data": data
            }
        )
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


class PhotoCapture(TypedDict):
    filename: str
    phototype: str
    timestamp: Optional[datetime.datetime]


class PhotoCaptureMessage(Message[PhotoCapture]):
    filename: str
    phototype: str
    timestamp: Optional[datetime.datetime]

    def __init__(
        self,
        filename: str,
        phototype: str,
        timestamp: Optional[datetime.datetime] = None,
    ):
        super().__init__(
            MessageType.DATA,
            System.CAMERA,
            {"filename": filename, "phototype": phototype, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: IMessage[PhotoCapture]):
        return PhotoCaptureMessage(
            message["data"]["filename"],
            message["data"]["phototype"],
            message["data"]["timestamp"],
        )
