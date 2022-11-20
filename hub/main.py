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
import threading
from flask import Flask, request
sys.path.append("../")
import hub.contract.contract as contract
from hub.network462 import ControlHub

DATABASE_URL = "postgresql://postgres:postgres@db:5432/garden" #change from localhost to db to connect to database in container
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
curr = conn.cursor()

class HubState:
    data: contract.IHubState

    def __init__(self, state: Optional[contract.IHubState] = contract.DefaultHubState):
        self.data = state

    def setMoisture(self, moisture: contract.MoistureData):
        self.data["dashboard"]["moisture"] = moisture

    def getMoisture(self) -> contract.MoistureData:
        return self.data["dashboard"]["moisture"]

    def setLight(self, light: contract.LightData):
        self.data["dashboard"]["light"] = light

    def getLight(self) -> contract.LightData:
        return self.data["dashboard"]["light"]

    def setTemperature(self, temperature: contract.TemperatureData):
        self.data["dashboard"]["temperature"] = temperature

    def getTemperature(self) -> contract.TemperatureData:
        return self.data["dashboard"]["temperature"]

    def setWaterLevel(self, waterLevel: contract.WaterLevelData):
        self.data["dashboard"]["waterLevel"] = waterLevel

    def getWaterLevel(self) -> contract.WaterLevelData:
        return self.data["dashboard"]["waterLevel"]

    def addPhoto(self, photo: contract.PhotoCapture):
        self.data["dashboard"]["photos"].append(photo)
        while len(self.data["dashboard"]["photos"]) > 10:
            self.data["dashboard"]["photos"].pop(0)

    def getPhotos(self) -> list[contract.PhotoCapture]:
        return self.data["dashboard"]["photos"]

    def setPlanterEnabled(self, enabled: bool):
        self.data["control"]["planterEnabled"] = enabled

    def getPlanterEnabled(self) -> bool:
        return self.data["control"]["planterEnabled"]

    def setHydroponicEnabled(self, enabled: bool):
        self.data["control"]["hydroponicEnabled"] = enabled

    def getHydroponicEnabled(self) -> bool:
        return self.data["control"]["hydroponicEnabled"]

    def setDryThreshold(self, threshold: float):
        self.data["control"]["dryThreshold"] = threshold

    def getDryThreshold(self) -> float:
        return self.data["control"]["dryThreshold"]

    def setFlowTime(self, flowTime: float):
        self.data["control"]["flowTime"] = flowTime

    def getFlowTime(self) -> float:
        return self.data["control"]["flowTime"]

    def setResevoirHeight(self, height: float):
        self.data["control"]["resevoirHeight"] = height

    def getResevoirHeight(self) -> float:
        return self.data["control"]["resevoirHeight"]

    def setEmptyResevoirHeight(self, height: float):
        self.data["control"]["emptyResevoirHeight"] = height

    def getEmptyResevoirHeight(self) -> float:
        return self.data["control"]["emptyResevoirHeight"]

    def setFullResevoirHeight(self, height: float):
        self.data["control"]["fullResevoirHeight"] = height

    def getFullResevoirHeight(self) -> float:
        return self.data["control"]["fullResevoirHeight"]


state = HubState()
state.data = contract.DefaultHubState

def insertDB(table: str, cols: str, data: str):
    print(f"INSERT INTO {table} ({cols}) VALUES({data})")
    curr.execute(f"INSERT INTO {table} ({cols}) VALUES({data})")


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
            if message.system == contract.System.MONITORING:
                if message.type == contract.MessageType.TEMPERATURE:
                    # insertTemperature(message)
                    state.data["dashboard"]["light"] = message.data
                    print(message)
                if message.type == contract.MessageType.LIGHT_READING:
                    # insertLight(message)
                    state.data["dashboard"]["light"] = message.data
                    print(message)
                if message.type == contract.MessageType.WATER_LEVEL:
                    # insertWaterLevel(message)
                    state.data["dashboard"]["water"] = message.data
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

app = Flask(__name__)
@app.route('/fetch', methods=['GET'])
def fetch():
    ret = json.dumps(state.data, cls=contract.ContractEncoder)
    return ret

@app.route('/update', methods=['POST'])
def update():
    message = request.form.to_dict()
    state.data = message

serverThread = threading.Thread(target=asyncio.run, args=(main(),), daemon=True)
serverThread.start()
app.run(debug=True)