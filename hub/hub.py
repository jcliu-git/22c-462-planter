import sys
from pathlib import Path
from time import sleep
import asyncio
import psycopg2
import shutil
import json
import threading
from flask import Flask, request

sys.path.append("../")
import contract.contract as contract
from network462 import ControlHub
import arduino.arduinoSystemClient as arduino

# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/garden"
# conn = psycopg2.connect(DATABASE_URL)
# conn.autocommit = True
# curr = conn.cursor()


lock = threading.Lock()


class HubState:
    data: contract.IHubState

    def __init__(self, data: contract.IHubState = contract.DefaultHubState):
        self.data = data


# pool = psycopg2.pool.ThreadedConnectionPool(1, 20, DATABASE_URL)

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
    "temperature": ["id", "temperature", "timestamp"],
    "water_level": ["id", "timestamp", "distance"],
}


def omit(obj, *keys):
    return {k: v for k, v in obj.items() if k not in keys}


def parseRows(cursor, table: str):
    result = []
    for row in cursor.fetchall():
        result.append(dict(zip(rows[table], row)))
    return [omit(row, "id") for row in result]


def fetchDashboardState():
    # get the state from the database
    try:
        curr.execute("SELECT * FROM light order by id desc limit 1")
        light = parseRows(curr, "light")

        curr.execute("SELECT * FROM moisture_level order by id desc limit 1")
        moisture = parseRows(curr, "moisture_level")

        curr.execute("SELECT * FROM temperature order by id desc limit 1")
        temperature = parseRows(curr, "temperature")

        curr.execute("SELECT * FROM water_level order by id desc limit 1")
        water = parseRows(curr, "water_level")

        curr.execute("SELECT * FROM photos order by id desc limit 10")
        photos = parseRows(curr, "photos")

        return {
            "light": light[0],
            "moisture": moisture[0],
            "temperature": temperature[0],
            "waterLevel": water[0],
            "photos": photos,
        }

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

        return False


state = HubState(
    {
        "dashboard": fetchDashboardState() or contract.DefaultHubState["dashboard"],
        "control": contract.DefaultHubState["control"],
    }
)


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
            # print(message)
            if message.system == contract.System.MONITORING:
                if message.type == contract.MessageType.TEMPERATURE:
                    # insertTemperature(message)
                    state.data["dashboard"]["temperature"] = message.data
                    # print(message)
                if message.type == contract.MessageType.LIGHT_READING:
                    # insertLight(message)
                    state.data["dashboard"]["light"] = message.data
                    # print(message)
                if message.type == contract.MessageType.WATER_LEVEL:
                    # insertWaterLevel(message)
                    state.data["dashboard"]["waterLevel"] = message.data
                    # print(message)
                if message.type == contract.MessageType.MOISTURE_READING:
                    # insertMoistureLevel(message)
                    state.data["dashboard"]["moisture"] = message.data
                    # print(message)

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

    while True:
        await asyncio.sleep(10)
        
        lock.acquire()
        moisture_readings = arduino.getSensorValues()
        print(moisture_readings)

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
        lock.release()


app = Flask(__name__)


@app.route("/fetch", methods=["GET"])
def fetch():
    ret = json.dumps(state.data, cls=contract.ContractEncoder)
    return ret


@app.route("/update", methods=["POST"])
def update():
    print(f"update request: {request.json}")
    # newState: contract.IHubState = request.get_json()
    try:
        newState: contract.IHubState = request.json

        lock.acquire()

        if (
            newState["control"]["planterEnabled"]
            != state.data["control"]["planterEnabled"]
        ):
            assert arduino.setPlanterPumps(1 if newState["control"]["planterEnabled"] else 0) == True

        if (
            newState["control"]["hydroponicEnabled"]
            != state.data["control"]["hydroponicEnabled"]
        ):
            assert arduino.setHydroPump(1 if newState["control"]["hydroponicEnabled"] else 0) == True

        if newState["control"]["dryThreshold"] != state.data["control"]["dryThreshold"]:
            assert arduino.setDryThreshold(newState["control"]["dryThreshold"]) == True

        if newState["control"]["flowTime"] != state.data["control"]["flowTime"]:
            assert arduino.setFlowTime(newState["control"]["flowTime"]) == True

        #if the water level is below 10% force pumps to be disabled
        if (
            (
                newState["control"]["emptyResevoirHeight"]
                - newState["dashboard"]["waterLevel"]["distance"]
            )
            / newState["control"]["resevoirHeight"]
        ) < 0.1:
            assert arduino.setPlanterPumps(0) == True
            newState["control"]["planterEnabled"] = False

        lock.release()

        state.data = newState

        return newState

    except Exception as e:
        print(e)
        return {"Error": True}


serverThread = threading.Thread(target=asyncio.run, args=(main(),), daemon=True)
serverThread.start()
app.run(debug=False)
