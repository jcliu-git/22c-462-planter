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

"""def insertDB():
    while True:
        if control.queue:
            payload = control.queue.pop(0)
            name = payload['name']
            type = payload['type']
            data = payload['data']
            if name == 'monitor_event' and type =='file': #for now, only monitor_event sends file type
                filesize = data[0]
                path = data[1]
                timestamp = data[2][0]
                pictype = data[2][1]
                filename = data[2][2]
                query = 'INSERT INTO monitor_event VALUES(%s,%s,%s,%s,%s)'
                curr.execute(query, (timestamp,pictype,filename,filesize,path))
            else: #data type 
                print('Inserting data...')
                print(data)
                query = 'INSERT INTO ' + name + ' VALUES(%s,%s);'
                curr.execute(query, (datetime.now(), data))
                print('done')
        sleep(1)
"""








