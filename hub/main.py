import sys
import os
from pathlib import Path
from time import sleep
import asyncio
from typing import Optional
import psycopg2
import random
import time
import shutil

import json

sys.path.append("../")
import contract.contract as contract
from hub.network462 import ControlHub

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/garden"
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
curr = conn.cursor()


class HubState:
    state: contract.IHubState

    def __init__(self, state: Optional[contract.IHubState] = contract.DefaultHubState):
        self.state = state

    def setMoisture(self, moisture: contract.MoistureData):
        self.state["dashboard"]["moisture"] = moisture

    def getMoisture(self) -> contract.MoistureData:
        return self.state["dashboard"]["moisture"]

    def setLight(self, light: contract.LightData):
        self.state["dashboard"]["light"] = light

    def getLight(self) -> contract.LightData:
        return self.state["dashboard"]["light"]

    def setTemperature(self, temperature: contract.TemperatureData):
        self.state["dashboard"]["temperature"] = temperature

    def getTemperature(self) -> contract.TemperatureData:
        return self.state["dashboard"]["temperature"]

    def setWaterLevel(self, waterLevel: contract.WaterLevelData):
        self.state["dashboard"]["waterLevel"] = waterLevel

    def getWaterLevel(self) -> contract.WaterLevelData:
        return self.state["dashboard"]["waterLevel"]

    def addPhoto(self, photo: contract.PhotoCapture):
        self.state["dashboard"]["photos"].append(photo)
        while len(self.state["dashboard"]["photos"]) > 10:
            self.state["dashboard"]["photos"].pop(0)

    def getPhotos(self) -> list[contract.PhotoCapture]:
        return self.state["dashboard"]["photos"]

    def setPlanterEnabled(self, enabled: bool):
        self.state["control"]["planterEnabled"] = enabled

    def getPlanterEnabled(self) -> bool:
        return self.state["control"]["planterEnabled"]

    def setHydroponicEnabled(self, enabled: bool):
        self.state["control"]["hydroponicEnabled"] = enabled

    def getHydroponicEnabled(self) -> bool:
        return self.state["control"]["hydroponicEnabled"]

    def setDryThreshold(self, threshold: float):
        self.state["control"]["dryThreshold"] = threshold

    def getDryThreshold(self) -> float:
        return self.state["control"]["dryThreshold"]

    def setFlowTime(self, flowTime: float):
        self.state["control"]["flowTime"] = flowTime

    def getFlowTime(self) -> float:
        return self.state["control"]["flowTime"]

    def setResevoirHeight(self, height: float):
        self.state["control"]["resevoirHeight"] = height

    def getResevoirHeight(self) -> float:
        return self.state["control"]["resevoirHeight"]

    def setEmptyResevoirHeight(self, height: float):
        self.state["control"]["emptyResevoirHeight"] = height

    def getEmptyResevoirHeight(self) -> float:
        return self.state["control"]["emptyResevoirHeight"]

    def setFullResevoirHeight(self, height: float):
        self.state["control"]["fullResevoirHeight"] = height

    def getFullResevoirHeight(self) -> float:
        return self.state["control"]["fullResevoirHeight"]


state: contract.IHubState = HubState()


def insertDB(table: str, cols: str, data: str):
    print(f"INSERT INTO {table} ({cols}) VALUES({data})")
    curr.execute(f"INSERT INTO {table} ({cols}) VALUES({data})")
    conn.commit()


def insertMoistureLevel(message: contract.MoistureReadingMessage):
    table = "moisture_level"
    cols = "timestamp, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8"
    message.data["timestamp"] = f"timestamp '{message.data['timestamp']}'"
    values = ",".join(
        str(x)
        for x in [
            message.data["timestamp"],
            message.data["sensor1"],
            message.data["sensor2"],
            message.data["sensor3"],
            message.data["sensor4"],
            message.data["sensor5"],
            message.data["sensor6"],
            message.data["sensor7"],
            message.data["sensor8"],
        ]
    )
    insertDB(table, cols, values)


def insertLight(message: contract.LightData):
    table = "light"
    cols = "timestamp, luminosity"
    message.data["timestamp"] = f"timestamp '{message.data['timestamp']}'"
    values = ",".join(
        str(x) for x in [message.data["timestamp"], message.data["value"]]
    )
    insertDB(table, cols, values)


def insertWaterLevel(message: contract.WaterLevelData):
    table = "water_level"
    cols = "timestamp,distance"
    message.data["timestamp"] = f"timestamp '{message.data['timestamp']}'"
    values = ",".join(
        str(x) for x in [message.data["timestamp"], message.data["value"]]
    )
    insertDB(table, cols, values)


def insertPhoto(message: contract.PhotoCaptureMessage):
    table = "photos"
    cols = "timestamp, filepath, width, height"
    message.data["timestamp"] = f"timestamp '{message.data['timestamp']}'"
    message.data["filepath"] = f"'{message.data['filepath']}'"
    values = ",".join(
        str(x)
        for x in [
            message.data["timestamp"],
            message.data["filepath"],
            message.data["width"],
            message.data["height"],
        ]
    )
    insertDB(table, cols, values)


def insertTemperature(message: contract.TemperatureData):
    table = "temperature"
    cols = "timestamp, temperature"
    message.data["timestamp"] = f"timestamp '{message.data['timestamp']}'"
    values = ",".join(
        str(x) for x in [message.data["timestamp"], message.data["value"]]
    )
    insertDB(table, cols, values)


async def handle_messages(controlHub: ControlHub):
    # asynchronous generator
    stream = controlHub.stream()
    async for message in stream:
        # do something based on what message you get
        try:
            # TODO: remove print statements below when everything's tested
            print(message)
            if message.system == contract.System.SUBSURFACE:
                # testing for now
                if message.type == contract.MessageType.DATA:
                    if message.data["type"] == contract.SubsurfaceDataType.MOISTURE:
                        insertMoistureLevel(message)

                    # await controlHub.sendData(message.system, message.data)
                # if message.type == contract.MessageType.FILE_MESSAGE:
                #     await controlHub.sendData(message.system, message.data)
            # if message.system == contract.System.HYDROPONICS:
            #     if message.type == contract.MessageType.DATA:
            #         """
            #         message.data:
            #         {
            #             "depth": int,
            #             "temperature": int,
            #             "moisture": int,
            #             "light": int
            #         }
            #         """

            #         pass
            if message.system == contract.System.MONITORING:
                if message.type == contract.MessageType.TEMPERATURE:
                    # insertTemperature(message)
                    print(message)
                if message.type == contract.MessageType.LIGHT_READING:
                    # insertLight(message)
                    print(message)
                if message.type == contract.MessageType.WATER_LEVEL:
                    # insertWaterLevel(message)
                    print(message)

            if message.system == contract.System.CAMERA:
                if message.type == contract.MessageType.PHOTO_CAPTURED:
                    """
                    message.data["data"]:
                    {
                        "time": YYYY-MM-DD hh:mm:ss,
                        "phototype": periodic/motion,
                        "filename": str
                    }
                    """
                    filename = message.data["filename"]
                    print("processing file: " + filename)
                    path = "../ui/public/"
                    # if message.data["data"]["phototype"] == contract.PhotoType.PERIODIC:
                    #     path += "periodic/"
                    # elif message.data["data"]["phototype"] == contract.PhotoType.MOTION:
                    #     path += "motion/"
                    Path(path).mkdir(parents=True, exist_ok=True)
                    print("placing file here: " + path + filename)
                    shutil.move("temp/" + filename, path + filename)
                    photocaptureMessage = contract.PhotoCaptureMessage.fromJson(message)
                    insertPhoto(photocaptureMessage)
        except Exception as err:
            print(err)
            print("something broke")


async def main():
    controlHub = ControlHub("0.0.0.0", 32132)
    await controlHub.startServer()

    # create non-blocking concurrent task
    asyncio.create_task(handle_messages(controlHub))

    # control hub monitoring, can be crated as another task
    while True:
        await asyncio.sleep(2)


asyncio.run(main())
