import os
import psycopg2
from time import sleep
from datetime import datetime
import sys
from time import sleep
import asyncio
sys.path.append("../")
import contract.contract as contract
from hub.network462 import ControlHub

#Connect to database
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn.autocommit=True
curr = conn.cursor()

async def main():
    controlHub = ControlHub("0.0.0.0", 32132)
    await controlHub.startServer()
    while True:
        message = await controlHub.queue.get()
        match message.system:
            case contract.System.SUBSURFACE:
                match message.type:
                    case contract.MessageType.MOISTURE_READING:
                        data = contract.MoistureReadingMessage.fromJson(message)
        await controlHub.sendData(data["system"], data["data"])

asyncio.run(main())

def insertDB(table: str, cols: str, data: str):
    curr.execute(f"INSERT INTO {table} {cols} VALUES{data}")
    conn.commit()

def insertMoistureLevel(data):
    table = "moisture_level"
    cols = "(sensor_1, sensor_2, sensor_3, sensor_4, sensor_5, sensor_6, sensor_7, sensor_8)"
    values = "("
    for i in range(1, 7):
        values += str(data[i-1])
        values += ", "
    values += str(data[7]) + ")"
    insertDB(table, cols, values)






