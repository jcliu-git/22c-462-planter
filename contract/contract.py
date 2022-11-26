import datetime
from enum import Enum
from json import dumps, JSONEncoder
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
    TypedDict,
    Dict,
)
import time


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


NETWORK_PORT = 32132
NETWORK_HOST = "172.29.80.1"


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
    UI = "ui"

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


# helps the receiving function identify whether this some data or a file
class MessageIdentifier(str, Enum):
    DATA = "data"
    FILE = "file"

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
    PHOTO_CAPTURED = "photo_captured"
    # camera
    WATER_LEVEL = "water_level"
    LIGHT_READING = "light_reading"
    # irrigation

    # hydroponics
    HYDROPONICS = "hydroponic_data"

    # temperature
    TEMPERATURE = "temperature"

    HUB_STATE = "hub_state"

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


class Message(Generic[DataType]):
    type: MessageType
    system: System
    data: DataType
    identifier: MessageIdentifier

    def __init__(
        self,
        type: MessageType,
        system: System,
        data: DataType,
        identifier: MessageIdentifier = MessageIdentifier.DATA,
    ):
        self.type = type
        self.system = system
        self.data = data
        self.identifier = identifier

    def __repr__(self):
        return dumps(self.__dict__)

    @staticmethod
    def fromJson(message):
        return Message(
            message["type"], message["system"], message["data"], message["identifier"]
        )


class GenericMessage(Message[Any]):
    data: Any


class DataMessage(GenericMessage):
    def __init__(self, system, data):
        super().__init__(MessageType.DATA, system, data)


# file
class FileMessage(Message[DataType]):
    def __init__(
        self,
        system: System,
        filename: str = None,
        filesize: int = None,
        data=None,
        type: MessageType = MessageType.FILE_MESSAGE,
        combine: Dict = {},
    ):
        # data is obsolete but is still there just in case
        # should use combine instead, which combines the python dictionary with
        # the other important things like filename and filesize in the data dictionary
        # tl;dr no need to do message["data"]["data"] or message.data["data"] anymore
        data_dict = {"filename": filename, "filesize": filesize, "data": data}
        combined_dict = data_dict | combine
        super().__init__(type, system, combined_dict, MessageIdentifier.FILE)


class MoistureData(TypedDict):
    sensor1: float
    sensor2: float
    sensor3: float
    sensor4: float
    sensor5: float
    sensor6: float
    sensor7: float
    sensor8: float
    timestamp: Optional[datetime.datetime]


class MoistureReadingMessage(Message[MoistureData]):
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
            timestamp = now()
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
    def fromJson(message: IMessage[MoistureData]):
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


class LightData(TypedDict):
    luminosity: float
    timestamp: Optional[datetime.datetime]


class LightLevelReadingMessage(Message[LightData]):
    def __init__(
        self, luminosity: float, timestamp: Optional[datetime.datetime] = None
    ):
        if timestamp is None:
            timestamp = now()
        super().__init__(
            MessageType.LIGHT_READING,
            System.MONITORING,
            {"luminosity": luminosity, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: LightData):
        return LightLevelReadingMessage(
            message["data"]["luminosity"], message["data"]["timestamp"]
        )


# Water Level definitions


class WaterLevelData(TypedDict):
    distance: float
    timestamp: Optional[datetime.datetime]


class WaterLevelReadingMessage(Message[WaterLevelData]):
    def __init__(self, distance: float, timestamp: Optional[datetime.datetime] = None):
        if timestamp is None:
            timestamp = now()
        super().__init__(
            MessageType.WATER_LEVEL,
            System.MONITORING,
            {"distance": distance, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: WaterLevelData):
        return WaterLevelReadingMessage(
            message["data"]["distance"], message["data"]["timestamp"]
        )


class TemperatureData(TypedDict):
    fahrenheit: float
    timestamp: Optional[datetime.datetime]


class TemperatureReadingMessage(Message[TemperatureData]):
    fahrenheit: float
    timestamp: Optional[datetime.datetime]

    def __init__(
        self, fahrenheit: float, timestamp: Optional[datetime.datetime] = None
    ):
        if timestamp is None:
            timestamp = now()
        super().__init__(
            MessageType.TEMPERATURE,
            System.MONITORING,
            {"fahrenheit": fahrenheit, "timestamp": timestamp},
        )

    @staticmethod
    def fromJson(message: TemperatureData):
        return TemperatureReadingMessage(
            message["data"]["fahrenheit"], message["data"]["timestamp"]
        )


# monitoring definitions


class PhotoCapture(TypedDict):
    filepath: str
    phototype: PhotoType
    timestamp: Optional[datetime.datetime]
    width: int
    height: int


class PhotoCaptureMessage(FileMessage):
    def __init__(
        self,
        filename: str,
        phototype: PhotoType,
        timestamp: Optional[datetime.datetime] = None,
        width: int = 720,
        height: int = 480,
    ):
        if timestamp is None:
            timestamp = now()
        super().__init__(
            System.CAMERA,
            filename,
            type=MessageType.PHOTO_CAPTURED,
            combine={
                "phototype": phototype,
                "timestamp": timestamp,
                "width": width,
                "height": height,
            },
        )

    def __repr__(self):
        return dumps(self.__dict__)

    @staticmethod
    def fromJson(message: FileMessage):
        filepath = "/"
        if message.data["phototype"] == "motion":
            filepath += "motion/"
        elif message.data["phototype"] == "periodic":
            filepath += "periodic/"
        elif message.data["phototype"] == "growth":
            filepath += "growth/"
        filepath += message.data["filename"]
        return PhotoCaptureMessage(
            filepath,
            message.data["phototype"],
            message.data["timestamp"],
        )


class IDashboardState(TypedDict):
    light: LightData
    temperature: TemperatureData
    photos: list[PhotoCapture]
    waterLevel: WaterLevelData
    moisture: MoistureData


class IControlState(TypedDict):
    planterEnabled: bool
    hydroponicEnabled: bool
    dryThreshold: float
    flowTime: float
    resevoirHeight: float
    emptyResevoirHeight: float
    fullResevoirHeight: float
    calibrating: bool


class IHubState(TypedDict):
    dashboard: IDashboardState
    control: IControlState


DefaultHubState: IHubState = {
    "dashboard": {
        "moisture": {
            "sensor1": 20,
            "sensor2": 101,
            "sensor3": 229,
            "sensor4": 488,
            "sensor5": 2928,
            "sensor6": 72,
            "sensor7": 289,
            "sensor8": 209,
            "timestamp": now(),
        },
        "light": {"luminosity": 54016, "timestamp": now()},
        "waterLevel": {"distance": 20.3, "timestamp": now()},
        "temperature": {"fahrenheit": 65.0005, "timestamp": now()},
        "photos": [],
    },
    "control": {
        "planterEnabled": True,
        "hydroponicEnabled": True,
        "dryThreshold": 500,
        "flowTime": 3.0,
        "resevoirHeight": 245,
        "emptyResevoirHeight": 250,
        "fullResevoirHeight": 5,
        "calibrating": False,
    },
    "analytics": {"waterConsumptionByDay": {}, "systemPulse": []},
    "websocketConnected": False,
}
