import sys

sys.path.append("../")
import asyncio
import contract.contract as contract
from hub.network462 import MonitoringClient
from Sensor_array import *


async def main():
    client = MonitoringClient(
        contract.System.MONITORING, "192.168.3.143", contract.NETWORK_PORT
    )
    await client.connect()
    print("connected")
    """
    water level is the most important, send that every second
    send the others every 5 seconds
    """
    count = 5
    try:
        while True:
            try:
                await client.sendWaterLevel(
                    contract.WaterLevelReadingMessage(getDepthData())
                )

                if count <= 0:
                    await client.sendLightLevel(
                        contract.LightLevelReadingMessage(getLightData())
                    )
                    await client.sendTemperature(
                        contract.TemperatureReadingMessage(getTemperatureData())
                    )
                    count = 5
                else:
                    count -= 1

            except Exception as e:
                print(e)
                await client.connect()
                print("reconnected")

            await asyncio.sleep(1)
    finally:
        GPIO.cleanup()


asyncio.run(main())
