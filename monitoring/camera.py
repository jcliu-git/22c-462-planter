import time
import sys
import asyncio
from aioconsole import ainput
import contract.contract as contract
from datetime import date
from datetime import datetime
from picamera import PiCamera
from gpiozero import MotionSensor
from gpiozero import Servo
import RPi.GPIO as GPIO
from hub.network462 import Client
from time import sleep
import json
sys.path.append("../")

# client for file transfer
client = Client("test", "127.0.0.1", 32132)
template_src_path = "source/test"
template_dest_path = "dest/test"

# devices
pir = MotionSensor(4)
camera = PiCamera()
# servos setup
servo1 = Servo(17) # 180 servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
servo2 = GPIO.PWM(27, 50) # continuous servo

def camera_capture(time, phototype, filename):
    
    # execute_query(connection, monitor_event)
    camera.start_preview()
    sleep(5)
    camera.capture(filename + ".jpg")
    camera.stop_preview()
    data = {}
    data['time'] = time
    data['type'] = phototype
    data['filename'] = filename
    monitor_event = json.dumps(data)
    return monitor_event
    #await client.sendFile(filename+ ".jpg", filename+ ".jpg")

def motion_track():
    # Defined angles of rotation for servo2(continuous servo)
    center = 7.5
    right_45 = 5
    right_90 = 2.7
    left_45 = 10
    right_90 = 12.5

async def main():
    # client for file transfer
    await client.connect()
    template_src_path = "source/test"
    template_dest_path = "dest/test"
        
    while True:
        today = date.today()
        t = time.localtime()
        cooldown = False
        current_date = time.strftime("%b-%d-%Y")
        db_time = datetime.now()
        current_time = time.strftime("%H:%M:%S", t)
        if cooldown == False:
            if pir.motion_detected():  # takes picture if detects motion
                filename = current_date + "_motion_image_" + current_time
                monitor_event = camera_capture(db_time, "motion", filename)
                await client.sendData(monitor_event)
                await client.sendFile(filename+ ".jpg", filename+ ".jpg")
                cooldown = True
            if time.strftime("%M:%S", t) == "30:00":  # takes pictures at periods
                filename = current_date + "_time_image_" + current_time
                monitor_event = camera_capture(db_time, "periodic", filename)
                await client.sendData(monitor_event)
                await client.sendFile(filename+ ".jpg", filename+ ".jpg")
                cooldown = True
        if cooldown == True:  # adds a 5 minute cooldown for pictures
            time.sleep(300)
            cooldown = False
        time.sleep(1)#race condition fix

asyncio.run(main())
