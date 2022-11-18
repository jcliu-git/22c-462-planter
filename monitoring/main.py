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
                client.sendWaterLevel(contract.WaterLevelReadingMessage(getDepthData()))
                client.sendLightLevel(contract.LightLevelReadingMessage(getLightData()))
                client.sendTemperature(
                    contract.TemperatureReadingMessage(getTemperatureData())
                )
            except:
                print("something broke, continuing")

            time.sleep(3)
    finally:
        GPIO.cleanup()


asyncio.run(main())
