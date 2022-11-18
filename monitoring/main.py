import sys

sys.path.append("../")
import asyncio
import contract.contract as contract
from hub.network462 import MonitoringClient
from Sensor_array import *


async def main():
    client = MonitoringClient(
        contract.System.MONITORING, contract.NETWORK_HOST, contract.NETWORK_PORT
    )
    await client.connect()
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

            time.sleep(3)
    finally:
        GPIO.cleanup()


asyncio.run(main())
