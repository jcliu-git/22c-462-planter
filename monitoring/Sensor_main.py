import sys
sys.path.append("../")
import asyncio
import contract.contract as contract
from hub.network462 import Client
from Sensor_array import *

async def main():
    client = Client("monitor", "192.168.3.143", 32132)
    await client.connect()
    while True:
        data = {
                "type": "sensors",
                "temperature": getTemperatureData(),
                "light": getLightData(),
                "moisture": getMoistureData()
            }
        print(data)
        await client.sendData(data)
        time.sleep(3)
#print(getDepth())
asyncio.run(main())
GPIO.cleanup()
