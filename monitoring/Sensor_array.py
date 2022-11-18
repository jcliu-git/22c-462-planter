import RPi.GPIO as GPIO
import time
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# ...Setting up mcp3008...#
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi, cs)
tempChan = AnalogIn(mcp, MCP.P1)
photoChan = AnalogIn(mcp, MCP.P0)

GPIO.setmode(GPIO.BCM)

# ...Setting up depth sensor...#
PIN_TRIGGER = 16
PIN_ECHO = 26

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)


def getDepthData():

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)

    # distance in cm
    return distance


def getTemperatureData():
    volt = tempChan.value
    return volt * 0.00109375


def getLightData():
    volt = photoChan.value
    return volt
