import sys

sys.path.append("../")
import asyncio
import contract.contract as contract
from hub.network462 import MonitoringClient
import random
import time
import datetime


def getDepthData():
    return random.randint(0, 100)


def getLightData():
    return random.randint(0, 100)


def getTemperatureData():
    return random.randint(0, 100)


def randomTimePastSevenDays():
    # returns a random time in the past 7 days
    return (
        datetime.datetime.now()
        - datetime.timedelta(
            days=random.randint(0, 6), seconds=random.randint(0, 86400)
        )
    ).strftime("%Y-%m-%d %H:%M:%S")


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
                contract.WaterLevelReadingMessage(
                    getDepthData(), randomTimePastSevenDays()
                )
            )

            if count <= 0:
                await client.sendLightLevel(
                    contract.LightLevelReadingMessage(
                        getLightData(), randomTimePastSevenDays()
                    )
                )
                await client.sendTemperature(
                    contract.TemperatureReadingMessage(
                        getTemperatureData(), randomTimePastSevenDays()
                    )
                )
                count = 5
            else:
                count -= 1
        except Exception as e:
            await client.connect()

        await asyncio.sleep(1)


asyncio.run(main())
