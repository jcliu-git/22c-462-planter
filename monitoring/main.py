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
    sensors = SensorArray()
    print("connected")
    """
    water level / moisture are the most important, send those every second
    send the others every 5 seconds
    """
    count = 5
    try:
        while True:
            try:
                await client.sendWaterLevel(
                    contract.WaterLevelReadingMessage(sensors.getDepth())
                )

                await client.sendSoilMoisture(
                    contract.MoistureReadingMessage(
                        *[*sensors.getMoisture(), 0, 0, 0, 0]
                    )
                )

                if count <= 0:
                    await client.sendLightLevel(
                        contract.LightLevelReadingMessage(sensors.getLight())
                    )
                    await client.sendTemperature(
                        contract.TemperatureReadingMessage(sensors.getTemperature())
                    )
                    count = 5
                else:
                    count -= 1

            except Exception as e:
                print(e)

            await asyncio.sleep(1)
    finally:
        GPIO.cleanup()


asyncio.run(main())
