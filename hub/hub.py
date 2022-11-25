import sys
from pathlib import Path
from time import sleep
import websockets
import asyncio

import psycopg2
from psycopg2 import pool
import shutil
import json
import threading
import logging
from datetime import datetime
from dotenv import dotenv_values


sys.path.append("../")
import contract.contract as contract
from network462 import ControlHub
import arduino.arduinoSystemClient as arduino

Path("logs").mkdir(parents=True, exist_ok=True)
logname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_hub.log"
logpath = f"logs/{logname}"
logging.basicConfig(filename=logpath, encoding="utf-8")


config = dotenv_values(".env")
db = psycopg2.pool.ThreadedConnectionPool(
    1,
    20,
    config["DATABASE_URL"],
)


# lock to prevent simultaneous writes to arduino
lock = threading.Lock()


class HubState:
    data: contract.IHubState

    def __init__(self, data: contract.IHubState = contract.DefaultHubState):
        self.data = data


rows = {
    "light": ["id", "luminosity", "timestamp"],
    "moisture_level": [
        "id",
        "sensor1",
        "sensor2",
        "sensor3",
        "sensor4",
        "sensor5",
        "sensor6",
        "sensor7",
        "sensor8",
        "timestamp",
    ],
    "photos": ["id", "timestamp", "filepath", "width", "height"],
    "temperature": ["id", "fahrenheit", "timestamp"],
    "water_level": ["id", "timestamp", "distance"],
}


def omit(obj, *keys):
    return {k: v for k, v in obj.items() if k not in keys}


def parseRows(cursor, table: str):
    result = []
    for row in cursor.fetchall():
        result.append(dict(zip(rows[table], row)))
    return [omit(row, "id") for row in result]


state = HubState(
    {
        "dashboard": contract.DefaultHubState["dashboard"],
        "control": contract.DefaultHubState["control"],
    }
)


def insertDB(table: str, cols: str, data: str):
    conn = db.getconn()
    curr = conn.cursor()
    curr.execute(f"INSERT INTO {table} ({cols}) VALUES({data})")

    db.putconn(conn)


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


def insertTemperature(message: contract.TemperatureData):
    table = "temperature"
    cols = "timestamp, temperature"
    message.data["timestamp"] = f"timestamp '{message.data['timestamp']}'"
    values = ",".join(
        str(x) for x in [message.data["timestamp"], message.data["value"]]
    )
    insertDB(table, cols, values)


async def handle_messages(hub):
    stream = hub.stream()
    temperature = 10
    light = 10
    water_level = 3

    async for message in stream:
        # do something based on the message you get
        try:

            if message.system == contract.System.MONITORING:
                if message.type == contract.MessageType.TEMPERATURE:
                    state.data["dashboard"]["temperature"] = message.data
                    websockets.broadcast(
                        hub.websockets.values(), json.dumps(state.data)
                    )

                    if temperature <= 0:
                        insertTemperature(message)
                        temperature = 10
                    else:
                        temperature -= 1

                if message.type == contract.MessageType.LIGHT_READING:
                    state.data["dashboard"]["light"] = message.data
                    websockets.broadcast(
                        hub.websockets.values(), json.dumps(state.data)
                    )

                    if light <= 0:
                        insertLight(message)
                        light = 10
                    else:
                        light -= 1

                if message.type == contract.MessageType.WATER_LEVEL:
                    state.data["dashboard"]["waterLevel"] = message.data
                    websockets.broadcast(
                        hub.websockets.values(), json.dumps(state.data)
                    )

                    if water_level <= 0:
                        insertWaterLevel(message)
                        water_level = 3
                    else:
                        water_level -= 1

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
                    type = message.data["phototype"]
                    print("processing file: " + filename)
                    path = f"../ui/public/camera/{type}/"

                    Path(path).mkdir(parents=True, exist_ok=True)

                    print("placing file here: " + path + filename)
                    shutil.move("temp/" + filename, path + filename)

            if message.system == contract.System.UI:
                if message.type == contract.MessageType.HUB_STATE:
                    try:
                        newState: contract.IHubState = message.data

                        try:

                            if (
                                newState["control"]["planterEnabled"]
                                != state.data["control"]["planterEnabled"]
                            ):
                                arduino.setPlanterPumps(
                                    1 if newState["control"]["planterEnabled"] else 0
                                )

                            if (
                                newState["control"]["hydroponicEnabled"]
                                != state.data["control"]["hydroponicEnabled"]
                            ):
                                arduino.setHydroPump(
                                    1 if newState["control"]["hydroponicEnabled"] else 0
                                )

                            if (
                                newState["control"]["dryThreshold"]
                                != state.data["control"]["dryThreshold"]
                            ):
                                arduino.setDryThreshold(
                                    newState["control"]["dryThreshold"]
                                )

                            if (
                                newState["control"]["flowTime"]
                                != state.data["control"]["flowTime"]
                            ):
                                arduino.setFlowTime(newState["control"]["flowTime"])

                            # if the water level is below 10% force pumps to be disabled
                            if (
                                (
                                    newState["control"]["emptyResevoirHeight"]
                                    - newState["dashboard"]["waterLevel"]["distance"]
                                )
                                / newState["control"]["resevoirHeight"]
                            ) < 0.1:
                                arduino.setPlanterPumps(0)
                                newState["control"]["planterEnabled"] = False

                        except Exception as e:
                            arduino.errorSendingValues()
                            arduino.setHydroPump(0)
                            arduino.setPlanterPumps(0)

                        state.data = newState

                    except Exception as err:
                        print(err)

        except Exception as err:
            print(err)
            logging.error(err)


async def main():
    controlHub = ControlHub("0.0.0.0", 32132)
    await controlHub.startServer()

    asyncio.create_task(handle_messages(controlHub))

    fiveMinutes = 60 * 5

    # handle synchronous reads from the arduino
    while True:
        try:
            await asyncio.sleep(5)

            fiveMinutes -= 5

            lock.acquire()
            moisture_readings = arduino.getSensorValues()
            lock.release()

            if fiveMinutes <= 0:
                insertMoistureLevel(
                    contract.MoistureReadingMessage(
                        moisture_readings[0],
                        moisture_readings[1],
                        moisture_readings[2],
                        moisture_readings[3],
                        moisture_readings[4],
                        moisture_readings[5],
                        moisture_readings[6],
                        moisture_readings[7],
                        moisture_readings[8],
                    )
                )
                fiveMinutes = 60 * 5

            if moisture_readings:
                state.data["dashboard"]["moisture"] = {
                    "sensor1": moisture_readings[0],
                    "sensor2": moisture_readings[1],
                    "sensor3": moisture_readings[2],
                    "sensor4": moisture_readings[3],
                    "sensor5": moisture_readings[4],
                    "sensor6": moisture_readings[5],
                    "sensor7": moisture_readings[6],
                    "sensor8": moisture_readings[7],
                }

        except Exception as e:
            print(e)
            logging.error(e)
            continue
        finally:
            lock.release()


if __name__ == "__main__":
    asyncio.run(main())
