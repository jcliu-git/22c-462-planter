import random
import sys
from pathlib import Path
import websockets
import asyncio
import os
import json
import threading
import logging
import datetime
from services import Services
from scheduler import startScheduler


sys.path.append("../")
import contract.contract as contract
from network462 import ControlHubServer
import arduino.arduinoSystemClient as arduino

Path("logs").mkdir(parents=True, exist_ok=True)
logname = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "_hub.log"
logpath = f"logs/{logname}"
logging.basicConfig(filename=logpath, encoding="utf-8")


def randomTimePastSevenDays():
    # returns a random time in the past 7 days
    return (
        datetime.datetime.now()
        - datetime.timedelta(
            days=random.randint(0, 6), seconds=random.randint(0, 86400)
        )
    ).strftime("%Y-%m-%d %H:%M:%S")


class Hub:
    state: contract.IHubState
    randomMoisture: bool = False

    def __init__(self, state: contract.IHubState = contract.DefaultHubState):
        self.lock = threading.Lock()
        self.state = state
        self.hub = ControlHubServer("0.0.0.0", 32132)
        self.services = Services(self)
        if len(sys.argv) > 1:
            self.randomMoisture = sys.argv[1] == "test"

    def reset(self):
        self.state = contract.DefaultHubState

    async def handle_messages(self):
        hub = self.hub
        stream = hub.stream()

        async for message in stream:
            try:
                if message.system == contract.System.MONITORING:
                    if message.type == contract.MessageType.TEMPERATURE:
                        self.state["dashboard"]["temperature"] = message.data
                        websockets.broadcast(
                            hub.websockets.values(), json.dumps(self.state)
                        )

                    if message.type == contract.MessageType.LIGHT_READING:
                        self.state["dashboard"]["light"] = message.data
                        websockets.broadcast(
                            hub.websockets.values(), json.dumps(self.state)
                        )

                    if message.type == contract.MessageType.WATER_LEVEL:
                        self.state["dashboard"]["waterLevel"] = message.data
                        websockets.broadcast(
                            hub.websockets.values(), json.dumps(self.state)
                        )

                if message.system == contract.System.CAMERA:
                    if message.type == contract.MessageType.PHOTO_CAPTURED:
                        self.services.uploadImage(message)

                if message.system == contract.System.UI:
                    if message.type == contract.MessageType.HUB_STATE:
                        try:
                            newState: contract.IHubState = message.data
                            
                            try:
                                self.lock.acquire()
                                if (
                                    newState["control"]["planterEnabled"]
                                    != self.state["control"]["planterEnabled"]
                                ):
                                    arduino.setPlanterPumps(
                                        1
                                        if newState["control"]["planterEnabled"]
                                        else 0
                                    )

                                if (
                                    newState["control"]["hydroponicEnabled"]
                                    != self.state["control"]["hydroponicEnabled"]
                                ):
                                    arduino.setHydroPump(
                                        1
                                        if newState["control"]["hydroponicEnabled"]
                                        else 0
                                    )

                                if (
                                    newState["control"]["dryThreshold"]
                                    != self.state["control"]["dryThreshold"]
                                ):
                                    arduino.setDryThreshold(
                                        newState["control"]["dryThreshold"]
                                    )

                                if (
                                    newState["control"]["flowTime"]
                                    != self.state["control"]["flowTime"]
                                ):
                                    arduino.setFlowTime(newState["control"]["flowTime"])

                                # if the water level is below 10% force pumps to be disabled
                                if (
                                    (
                                        newState["control"]["emptyResevoirHeight"]
                                        - newState["dashboard"]["waterLevel"][
                                            "distance"
                                        ]
                                    )
                                    / newState["control"]["resevoirHeight"]
                                ) < 0.1:
                                    arduino.setPlanterPumps(0)
                                    newState["control"]["planterEnabled"] = False

                            except Exception as e:
                                logging.error(f"Error setting arduino state: {e}")
                                arduino.errorSendingValues()
                                arduino.setHydroPump(0)
                                arduino.setPlanterPumps(0)

                            finally:
                                if self.lock.locked():
                                    self.lock.release()

                            self.state = newState

                        except Exception as err:
                            logging.error(f"Error setting hub state: {err}")
                            print(err)

            except Exception as err:
                print("handle_messages error: ", err)
                logging.error("handle_messages error: " + err)

    async def start(self):

        await self.hub.startServer()
        asyncio.create_task(self.handle_messages())
        asyncio.create_task(startScheduler(self.services))

        # handle synchronous reads from the arduino
        while True:
            try:
                await asyncio.sleep(5)
                self.lock.acquire()
                #moisture_readings = []
                #if self.randomMoisture:
                #    for _ in range(8):
                #        moisture_readings.append(random.randint(120, 1024))
                #else:
                #    moisture_readings = arduino.getSensorValues()

                moisture_readings = arduino.getSensorValues()
                print(moisture_readings)
                if moisture_readings == False:
                    if self.lock.locked():
                        self.lock.release()
                    continue

                if moisture_readings:
                    self.state["dashboard"]["moisture"] = {
                        "sensor1": moisture_readings[0],
                        "sensor2": moisture_readings[1],
                        "sensor3": moisture_readings[2],
                        "sensor4": moisture_readings[3],
                        "sensor5": moisture_readings[4],
                        "sensor6": moisture_readings[5],
                        "sensor7": moisture_readings[6],
                        "sensor8": moisture_readings[7],
                        "timestamp": (
                            randomTimePastSevenDays()
                            if self.randomMoisture
                            else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ),
                    }

            except Exception as e:
                print(e)
                logging.error(e)
            finally:
                if self.lock.locked():
                    self.lock.release()
                continue


if __name__ == "__main__":
    hub = Hub()
    asyncio.run(hub.start())
