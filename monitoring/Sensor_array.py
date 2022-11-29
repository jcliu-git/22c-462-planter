import RPi.GPIO as GPIO
import time
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class SensorArray:
    # ...Setting up mcp3008...#
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D22)
    mcp = MCP.MCP3008(spi, cs)
    photo_chan = AnalogIn(mcp, MCP.P0)
    temp_chan = AnalogIn(mcp, MCP.P1)
    moisture_channels = [
        AnalogIn(mcp, MCP.P2),
        AnalogIn(mcp, MCP.P3),
        AnalogIn(mcp, MCP.P4),
        AnalogIn(mcp, MCP.P5),
    ]

    # ...Setting up depth sensor...#
    PIN_TRIGGER = 16
    PIN_ECHO = 26

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

    def __del__(self):
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
        GPIO.output(self.PIN_ECHO, GPIO.LOW)
        GPIO.output(self.PIN_PUMP, GPIO.LOW)
        GPIO.cleanup()

    def cleanup(self):
        self.__del__()

    def pumpOn(self):
        GPIO.output(self.PIN_PUMP, GPIO.HIGH)

    def pumpOff(self):
        GPIO.output(self.PIN_PUMP, GPIO.LOW)

    def getDepth(self):

        GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(self.PIN_ECHO) == 0:
            pulse_start_time = time.time()
        while GPIO.input(self.IN_ECHO) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)

        # distance in cm
        return distance

    def getTemperature(self):
        volt = self.temp_chan.value
        return volt * 0.00109375

    def getLight(self):
        volt = self.photo_chan.value
        return volt

    def getMoisture(self):
        return [chan.value / 100 for chan in self.moisture_channels]
