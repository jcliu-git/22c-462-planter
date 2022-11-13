import datetime
from enum import Enum
from json import dumps, JSONEncoder
from typing import Any, AsyncGenerator, Generic, Optional, Type, TypeVar, TypedDict


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ContractEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Message):
            return o.__dict__


class PhotoType(str, Enum):
    MOTION = "motion"
    PERIODIC = "periodic"

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class System(str, Enum):
    HUB = "hub"
    MONITORING = "monitor"
    SUBSURFACE = "subsurface"
    CAMERA = "camera"
    IRRIGATION = "irrigation"
    HYDROPONICS = "hydroponics"

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
    WATER_LEVEL = "water_level"
    LIGHT_READING = "light_reading"
    # irrigation

    # hydroponics
    HYDROPONICS = "hydroponic_data"

    # temperature
    TEMPERATURE = "temperature"

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


# top level definitions

DataType = TypeVar("DataType")


class IMessage(TypedDict):
    type: MessageType
    system: System
    data: DataType

    # def __repr__(self):
    #     return self.__dict__


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
    def fromJson(message):
        return Message(message["type"], message["system"], message["data"])


class GenericMessage(Message[Any]):
    data: Any


class PackageDirection(Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class DataMessage(GenericMessage):
    def __init__(self, system, data):
        super().__init__(MessageType.DATA, system, data)


# file


class FileMetadata(TypedDict):
    filename: str
    path: str
    filesize: int
    # data: Any


class FileMessage(Message[FileMetadata]):
    def __init__(self, system: System, filename: str, filesize: int, data=None):
        super().__init__(
            MessageType.FILE_MESSAGE,
            system,
            {"filename": filename, "filesize": filesize, "data": data},
        )


# subsurface definitions
class HydroponicData(TypedDict):
    light: int
    temperature: int
    depth: int
    moisture: int


class IMoistureData(TypedDict):
    sensor1: float
    sensor2: float
    sensor3: float
    sensor4: float
    sensor5: float
    sensor6: float
    sensor7: float
    sensor8: float
    timestamp: Optional[datetime.datetime]


class MoistureReadingMessage(Message[IMoistureData]):
    def __init__(
        self,
        sensor1: float,
        sensor2: float,
        sensor3: float,
        sensor4: float,
        sensor5: float,
        sensor6: float,
        sensor7: float,
        sensor8: float,
        timestamp: Optional[datetime.datetime] = None,
    ):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        super().__init__(
            MessageType.MOISTURE_READING,
            System.SUBSURFACE,
            {
                "sensor1": sensor1,
                "sensor2": sensor2,
                "sensor3": sensor3,
                "sensor4": sensor4,
                "sensor5": sensor5,
                "sensor6": sensor6,
                "sensor7": sensor7,
                "sensor8": sensor8,
                "timestamp": timestamp,
            },
        )

    @staticmethod
    def fromJson(message: IMessage[IMoistureData]):
        return MoistureReadingMessage(
            message["data"]["sensor1"],
            message["data"]["sensor2"],
            message["data"]["sensor3"],
            message["data"]["sensor4"],
            message["data"]["sensor5"],
            message["data"]["sensor6"],
            message["data"]["sensor7"],
            message["data"]["sensor8"],
            message["data"]["timestamp"],
        )


class HydroponicMessage(Message[HydroponicData]):
    def __init__(
        self,
        depth: float,
        temperature: float,
        moisture: float,
        light: int,
        timestamp: Optional[datetime.datetime] = None,
    ):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        super().__init__(
            MessageType.HYDROPONICS,
            System.HYDROPONICS,
            {
                "depth": depth,
                "temperature": temperature,
                "moisture": moisture,
                "light": light,
                "timestamp": timestamp,
            },
        )


class LightData(TypedDict):
    value: float
    timestamp: Optional[datetime.datetime]


class LightReadingMessage(Message[LightData]):
    def __init__(self, value: float, timestamp: Optional[datetime.datetime] = None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        super().__init__(
            MessageType.LIGHT_READING,
            System.MONITORING,
            {"value": value, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: HydroponicMessage):
        return LightReadingMessage(
            message["data"]["light"], message["data"]["timestamp"]
        )


# Water Level definitions


class WaterLevelData(TypedDict):
    value: float
    timestamp: Optional[datetime.datetime]


class WaterLevelReadingMessage(Message[LightData]):
    def __init__(self, value: float, timestamp: Optional[datetime.datetime] = None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        super().__init__(
            MessageType.WATER_LEVEL,
            System.MONITORING,
            {"value": value, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: HydroponicMessage):
        return WaterLevelReadingMessage(
            message["data"]["depth"], message["data"]["timestamp"]
        )


class TemperatureData(TypedDict):
    value: float
    timestamp: Optional[datetime.datetime]


class TemperatureDataReadingMessage(Message[TemperatureData]):
    value: float
    timestamp: Optional[datetime.datetime]

    def __init__(self, value: float, timestamp: Optional[datetime.datetime] = None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        super().__init__(
            MessageType.TEMPERATURE,
            System.MONITORING,
            {"value": value, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: HydroponicMessage):
        return TemperatureDataReadingMessage(
            message["data"]["temperature"], message["data"]["timestamp"]
        )


# monitoring definitions


class PhotoCapture(TypedDict):
    filepath: str
    phototype: PhotoType
    timestamp: Optional[datetime.datetime]


class PhotoCaptureMessage(Message[PhotoCapture]):
    def __init__(
        self,
        filepath: str,
        phototype: PhotoType,
        timestamp: Optional[datetime.datetime] = None,
        width: int = 720,
        height: int = 480,
    ):
        if timestamp is None:
            timestamp = now()
        super().__init__(
            MessageType.FILE_MESSAGE,
            System.CAMERA,
            {
                "filepath": filepath,
                "phototype": phototype,
                "timestamp": timestamp,
                "width": width,
                "height": height,
            },
        )

    @staticmethod
    def fromJson(message: FileMessage):
        filepath = "/"
        if message.data["data"]["phototype"] == "motion":
            filepath += "motion/"
        elif message.data["data"]["phototype"] == "periodic":
            filepath += "periodic/"
        filepath += message.data["data"]["filename"]
        return PhotoCaptureMessage(
            filepath,
            message.data["data"]["phototype"],
            message.data["data"]["timestamp"],
        )
