import RPi.GPIO as GPIO
import time
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#...Setting up mcp3008...#
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi, cs)

tempChan = AnalogIn(mcp, MCP.P2)

photoChan = AnalogIn(mcp, MCP.P0)

GPIO.setmode(GPIO.BCM)

#...Setting up depth sensor...#
PIN_TRIGGER = 16
PIN_ECHO = 26

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)



def getDepthData():
    #print("Waiting for sensor to settle")

    time.sleep(2)

    #print("Calculating distance")

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    #print("Distance:", distance, "cm")
    
    return distance
    
def getTemperatureData():
    volt = tempChan.value
    return volt*0.00109375

def getLightData():
    volt = photoChan.value
    return volt



while True:
    print(getLightData())
    #print(getDepthData())
    time.sleep(2)


#...Testing...#
#print("Test")
#voltSum = 0
#average = 0
#temp = 0
#for i in range(50):
    #temp = getMoistureData()
    #voltSum += temp
    #print("Moisture volt:", temp)
    #time.sleep(0.1)
#average = voltSum/50


#print("Average temp:", round(average*0.109375, 2))#constant multiple to convert ot F
#print("Moisture Volt:", round(average, 2))
#getTemp()


#GPIO.cleanup()
    
    
