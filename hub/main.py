import sys
import os
from pathlib import Path
from time import sleep
import asyncio
import psycopg2
import random
import time
import shutil

sys.path.append("../")
import contract.contract as contract
from hub.network462 import ControlHub

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/garden"
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
curr = conn.cursor()


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
    cols = "timestamp, value"
    message.data["timestamp"] = f"timestamp '{message.data['timestamp']}'"
    values = ",".join(
        str(x) for x in [message.data["timestamp"], message.data["value"]]
    )
    insertDB(table, cols, values)


def insertWaterLevel(message: contract.WaterLevelData):
    table = "water_level"
    cols = "timestamp,value"
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
    cols = "timestamp, value"
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
                    insertTemperature(message)
                if message.type == contract.MessageType.LIGHT_READING:
                    insertLight(message)
                if message.type == contract.MessageType.WATER_LEVEL:
                    insertWaterLevel(message)
                if message.type == "data":
                    print("inserting sensor data", message.data)
                    insertMoistureLevel(
                        contract.MoistureReadingMessage(
                            message.data["moisture"],
                            message.data["moisture"],
                            message.data["moisture"],
                            message.data["moisture"],
                            message.data["moisture"],
                            message.data["moisture"],
                            message.data["moisture"],
                            message.data["moisture"],
                        )
                    )
                    insertLight(contract.LightReadingMessage(message.data["light"]))
                    insertWaterLevel(
                        contract.WaterLevelReadingMessage(message.data["depth"])
                    )
                    insertTemperature(
                        contract.TemperatureDataReadingMessage(
                            message.data["temperature"]
                        )
                    )

            if message.system == contract.System.CAMERA:
                if message.type == contract.MessageType.FILE_MESSAGE:
                    """
                    message.data["data"]:
                    {
                        "time": YYYY-MM-DD hh:mm:ss,
                        "phototype": periodic/motion,
                        "filename": str
                    }
                    """
                    filename = message.data["data"]["filename"]
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
        except:
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
