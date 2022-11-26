import sys

sys.path.append("../")
import asyncio
import contract.contract as contract
from hub.network462 import MonitoringClient
import random


def getDepthData():
    return random.randint(0, 100)


def getLightData():
    return random.randint(0, 100)


def getTemperatureData():
    return random.randint(0, 100)


async def main():
    client = MonitoringClient(
        contract.System.MONITORING, "127.0.0.1", contract.NETWORK_PORT
    )
    await client.connect()
    print("connected")
    count = 5
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


asyncio.run(main())
