import time
from datetime import date
from datetime import datetime
from picamera import PiCamera
from gpiozero import MotionSensor
from gpiozero import Servo
import RPi.GPIO as GPIO
from network462 import Client
from time import sleep
import json

# client for file transfer
client = Client("test", "127.0.0.1", 32132)
# devices
pir = MotionSensor(4)
camera = PiCamera()
# servos setup
servo1 = Servo(17) # 180 servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
servo2 = GPIO.PWM(27, 50) # contnous servo


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
    client.sendData(monitor_event)
    client.sendFile(filename+ ".jpg", filename+ ".jpg")

def motion_track():
    # Defined angles of rotation for servo2(contnous servo)
    center = 7.5
    right_45 = 5
    right_90 = 2.7
    left_45 = 10
    right_90 = 12.5
    

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
            camera_capture(db_time, "motion", filename)
            cooldown = True
        if time.strftime("%M:%S", t) == "30:00":  # takes pictures at periods
            filename = current_date + "_time_image_" + current_time
            camera_capture(db_time, "time", filename)
            cooldown = True
    if cooldown == True:  # adds a 5 minute cooldown for pictures
        time.sleep(300)
        cooldown = False
    time.sleep(1)#race condition fix