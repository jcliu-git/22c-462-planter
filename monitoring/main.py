import sys

sys.path.append("../")
import asyncio
import contract.contract as contract
from hub.network462 import MonitoringClient
from Sensor_array import *


async def main():
    client = MonitoringClient(
        contract.System.MONITORING, '192.168.3.143', contract.NETWORK_PORT
    )
    await client.connect()
    print('connected')
    try:
        while True:
            try:
                await client.sendWaterLevel(contract.WaterLevelReadingMessage(getDepthData()))
                await client.sendLightLevel(contract.LightLevelReadingMessage(getLightData()))
                await client.sendTemperature(
                    contract.TemperatureReadingMessage(getTemperatureData())
                )
            except Exception as e:
                print(e)

            await asyncio.sleep(3)
    finally:
        GPIO.cleanup()


asyncio.run(main())



