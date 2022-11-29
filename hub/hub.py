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
import RPi.GPIO as GPIO
from services import Services
from scheduler import startScheduler
from pathlib import Path

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), ".."))

import contract.contract as contract
from network462 import ControlHubServer

# import arduino.arduinoSystemClient as arduino
from enum import Enum


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


class PumpState(str, Enum):
    ON = "ON"
    OFF = "OFF"
    SUSPENDED = "SUSPENDED"


class PumpController:
    state: PumpState
    enabled: bool
    pin: int
    debounce: int

    def __init__(self, pin=21, debounce=30) -> None:
        self.state = PumpState.OFF
        self.enabled = False
        self.pin = pin
        self.debounce = debounce

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def off(self):
        self.state = PumpState.OFF
        GPIO.output(self.pin, GPIO.LOW)

    def suspend(self):
        if self.debounce < 0:
            self.off()
            return

        self.state = PumpState.SUSPENDED
        GPIO.output(self.pin, GPIO.LOW)
        asyncio.get_event_loop().call_later(self.debounce, self.off)

    def on(self, duration: int):
        # pass zero to turn on indefinitely
        if (
            not self.enabled
            or self.state == PumpState.ON
            or self.state == PumpState.SUSPENDED
        ):
            return

        self.state = PumpState.ON
        GPIO.output(self.pin, GPIO.HIGH)
        if duration > 0:
            asyncio.get_event_loop().call_later(duration, self.suspend)


class Hub:
    state: contract.IHubState
    randomMoisture: bool = False

    def __init__(self, state: contract.IHubState = contract.default_hub_state()):
        self.state = state
        self.hub = ControlHubServer("0.0.0.0", 32132)
        self.services = Services(self)
        self.planterPump = PumpController(pin=21, debounce=30)
        self.hydroponicPump = PumpController(pin=20, debounce=-1)

    def reset(self):
        self.state = contract.default_hub_state()

    def shouldPump(self):
        return (
            sum(
                [self.state["dashboard"]["moisture"][f"sensor{x}"] for x in range(1, 9)]
            )
            / 4
            > self.dryThresholdFromPercent(self.state["control"]["dryThreshold"] / 100)
            and self.state["control"]["planterEnabled"]
            and not self.state["control"]["calibrating"]
        )

    async def handle_messages(self):
        hub = self.hub
        stream = hub.stream()

        async for message in stream:
            # print(message)
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

                    if message.type == contract.MessageType.MOISTURE_READING:
                        self.state["dashboard"]["moisture"] = message.data
                        websockets.broadcast(
                            hub.websockets.values(), json.dumps(self.state)
                        )
                        if self.shouldPump():
                            self.planterPump.on(self.state["control"]["flowTime"])
                        else:
                            self.planterPump.off()

                if message.system == contract.System.CAMERA:
                    if message.type == contract.MessageType.PHOTO_CAPTURED:
                        self.services.uploadImage(message)

                if message.system == contract.System.UI:
                    if message.type == contract.MessageType.HUB_STATE:
                        try:
                            newState: contract.IHubState = message.data

                            self.planterPump.enabled = newState["control"][
                                "planterEnabled"
                            ]
                            self.hydroponicPump.enabled = newState["control"][
                                "hydroponicEnabled"
                            ]

                            self.state = newState

                            if self.state["control"]["hydroponicEnabled"]:
                                self.hydroponicPump.on(0)
                            else:
                                self.hydroponicPump.off()

                            # if the water level is below 10% force pumps to be disabled
                            if (
                                (
                                    newState["control"]["emptyResevoirHeight"]
                                    - newState["dashboard"]["waterLevel"]["distance"]
                                )
                                / newState["control"]["resevoirHeight"]
                            ) < 0.1:
                                newState["control"]["planterEnabled"] = False
                                continue

                            if self.shouldPump():
                                self.planterPump.on(self.state["control"]["flowTime"])
                            else:
                                self.planterPump.off()

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

        while True:
            await asyncio.sleep(5)

    def dryThresholdFromPercent(self, percent: float):
        DRY_MAX = 495
        WET_MAX = 190
        if (percent < 0) or (percent > 1):
            print("you passed a dry threshold outside of 0 - 1")
            return DRY_MAX

        return percent * (DRY_MAX - WET_MAX) + WET_MAX


if __name__ == "__main__":
    hub = Hub()
    asyncio.run(hub.start())
