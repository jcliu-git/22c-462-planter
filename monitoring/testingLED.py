import RPi.GPIO as GPIO
#import time
#$import os
#import time
#import busio
#import digitalio
import board
#import adafruit_mcp3xxx.mcp3008 as MCP
#from adafruit_mcp3xxx.analog_in import AnalogIn
#from rpi_ws281x import PixelStrip, Color
import neopixel 

#...Setting up mcp3008...#
#spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
#cs = digitalio.DigitalInOut(board.D22)

#GPIO.setmode(GPIO.BCM)

#...Setting up depth sensor...#

LED = 18
PIN_ECHO = 26

pixels = neopixel.NeoPixel(board.D18, 2)

pixels[0] = (255, 0, 0)
pixels.fill((255, 0, 0))

'''
strip = PixelStrip(1, 18) # , 800000, 10, False, 255, 0

strip.begin()
strip.setBrightness(200)
strip.setPixelColor(0, Color(255,0,0))
strip.show()
print(strip.numPixels())
print(strip.getPixelColor(0))
print(strip.getPixelColorRGB(0))
'''

'''

try:
    while True:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255,0,0))
            print("red")
            strip.show()
            time.sleep(50/1000)
except KeyboardInterrupt:
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(10/1000)
'''