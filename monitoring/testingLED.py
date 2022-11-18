import RPi.GPIO as GPIO
import time
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from rpi_ws281x import PixelStrip, Color

#...Setting up mcp3008...#
#spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
#cs = digitalio.DigitalInOut(board.D22)

#GPIO.setmode(GPIO.BCM)

#...Setting up depth sensor...#
LED = 18
PIN_ECHO = 26

strip = PixelStrip(1, 18, 800000, 10, False, 255, 0)

strip.begin()

try:
    while True:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255,0,0))
            print("red")
            strip.show()
            time.sleep(500/1000)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,255))
            print("blue")
            strip.show()
            time.sleep(500/1000)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,255,0))
            print("green")
            strip.show()
            time.sleep(500/1000)
except KeyboardInterrupt:
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(10/1000)