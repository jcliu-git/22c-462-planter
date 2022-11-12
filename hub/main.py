import sys
from time import sleep
import asyncio
sys.path.append("../")
import contract.contract as contract
from hub.network462 import ControlHub

async def handle_messages(controlHub):
    # asynchronous generator
    stream = controlHub.stream()
    async for message in stream:
        # do something based on what message you get
        print(message)
        if message.system == contract.System.SUBSURFACE:
            # testing for now
            if message.type == contract.MessageType.DATA:
                print("data received, sending response")
                await controlHub.sendData(message.system, message.data)
            if message.type == contract.MessageType.FILE_MESSAGE:
                print("file received, sending response")
                await controlHub.sendData(message.system, message.data)
        if message.system == contract.System.HYDROPONICS:
            if message.type == contract.MessageType.DATA:
                """
                message.data:
                {
                    "depth": int,
                    "temperature": int,
                    "moisture": int,
                    "light": int
                }
                """
                pass
        if message.system == contract.System.CAMERA:
            if message.type == contract.FILE_MESSAGE:
                """
                    message.data.data:
                    {
                        "time":,
                        "type": periodic/motion,
                        "filename" str
                    }
                """
                pass

async def main():
    controlHub = ControlHub("0.0.0.0", 32132)
    await controlHub.startServer()

    # create non-blocking concurrent task
    asyncio.create_task(handle_messages(controlHub))

    # control hub monitoring, can be crated as another task
    while True:
        await asyncio.sleep(2)

asyncio.run(main())