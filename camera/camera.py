import time
import sys
import asyncio
import pigpio
sys.path.append("../")
# from aioconsole import ainput
import contract.contract as contract
from datetime import date
from datetime import datetime
from picamera import PiCamera
import picamera.array
from gpiozero import MotionSensor
from gpiozero import Servo
import RPi.GPIO as GPIO
from plantcv import plantcv as pcv
import cv2
from hub.network462 import Client
from time import sleep
import numpy as np
import json

# client for file transfer
client = Client("test", "192.168.3.114", 32132)
template_src_path = "source/test"
template_dest_path = "dest/test"

# devices
pir = MotionSensor(4)
camera = PiCamera()
# servos setup
servo180 = 17 #180 servo
servo360 = 27 #360 servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
servo2 = GPIO.PWM(27, 50)  # continuous servo
pfile = "temp"

async def camera_capture(time, phototype, filename):

    # execute_query(connection, monitor_event)
    camera.start_preview()
    sleep(5)
    camera.capture(filename + ".jpg")
    camera.stop_preview()
    data = {}
    data["time"] = time
    data["type"] = phototype
    data["filename"] = filename

    # await client.sendFile(filename+ ".jpg", filename+ ".jpg")
    return data

async def plant_analysis(filename, pfile):
    plant1_o = cv2.imread(filename +  ".jpg" )
    plant2_o = cv2.imread(pfile + ".jpg")

    pcv.params.debug = "print"

    # Isolate plant in first image
    y_channel1 = pcv.rgb2gray_cmyk(rgb_img=plant1_o, channel='Y')
    m_channel1 = pcv.rgb2gray_cmyk(rgb_img=plant1_o, channel='M')
    plant1 = cv2.subtract(y_channel1, m_channel1)
    plant1 = pcv.closing(gray_img=plant1)
    plant1 = pcv.erode(gray_img=plant1, ksize=15, i=10)
    plant1 = pcv.closing(gray_img=plant1)
    mask1 = cv2.threshold(plant1, 35, 255, cv2.THRESH_BINARY)[1]
    mask1 = pcv.fill_holes(bin_img=mask1)
    plant1 = pcv.apply_mask(img=plant1_o, mask=mask1, mask_color='white')
    plant1 = pcv.erode(gray_img=plant1, ksize=15, i=10)

    # Isolate plant in second image
    y_channel2 = pcv.rgb2gray_cmyk(rgb_img=plant2_o, channel='Y')
    m_channel2 = pcv.rgb2gray_cmyk(rgb_img=plant2_o, channel='M')
    plant2 = cv2.subtract(y_channel2, m_channel2)
    plant2 = pcv.closing(gray_img=plant2)
    plant2 = pcv.erode(gray_img=plant2, ksize=15, i=10)
    plant2 = pcv.closing(gray_img=plant2)
    mask2 = cv2.threshold(plant2, 35, 255, cv2.THRESH_BINARY)[1]
    mask2 = pcv.fill_holes(bin_img=mask2)
    plant2 = pcv.apply_mask(img=plant2_o, mask=mask2, mask_color='white')
    plant2 = pcv.erode(gray_img=plant2, ksize=15, i=10)

    # Take difference of both plants
    plantdifference = cv2.subtract(plant1, plant2)
    plantdifference = pcv.erode(gray_img=plantdifference, ksize=10, i=10)
    return plantdifference

def motion_track():
    # Defined angles of rotation for servo2(continuous servo)
    center = 7.5
    right_45 = 5
    right_90 = 2.7
    left_45 = 10
    right_90 = 12.5

#servo definitions

async def up():
    servo180.set_mode(servo180,pigpio.OUTPUT)
    servo180.set_PWM_frequency(17, 50)
    servo180.set_servo_pulsewidth(17, 1000)
    time.sleep(3)
    servo180.set_PWM_dutycycle( 17, 0 )
    servo180.set_PWM_frequency( 17, 0 )

async def center():
    servo180.set_mode(servo180,pigpio.OUTPUT)
    servo180.set_PWM_frequency(17, 50)
    servo180.set_servo_pulsewidth(17, 1500)
    time.sleep(3)
    servo180.set_PWM_dutycycle( 17, 0 )
    servo180.set_PWM_frequency( 17, 0 )

async def down():
    servo180.set_mode(servo180,pigpio.OUTPUT)
    servo180.set_PWM_frequency(17, 50)
    servo180.set_servo_pulsewidth(17, 2000)
    time.sleep(3)
    servo180.set_PWM_dutycycle( 17, 0 )
    servo180.set_PWM_frequency( 17, 0 )

async def right90():
    servo360 = pigpio.pi()
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27,700)
    time.sleep(.16)
    servo360.set_PWM_dutycycle( 27, 0 )
    servo360.set_PWM_frequency( 27, 0 )
    time.sleep(1)
    
async def right45():
    servo360 = pigpio.pi()
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27,700)
    time.sleep(.08)
    servo360.set_PWM_dutycycle( 27, 0 )
    servo360.set_PWM_frequency( 27, 0 )
    time.sleep(1)
    
async def left45():
    servo360 = pigpio.pi()
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27,1700)
    time.sleep(.08)
    servo360.set_PWM_dutycycle( 27, 0 )
    servo360.set_PWM_frequency( 27, 0 )
    time.sleep(1)
    
async def left90():
    servo360 = pigpio.pi()
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27,1750)
    time.sleep(.16)
    servo360.set_PWM_dutycycle( 27, 0 )
    servo360.set_PWM_frequency( 27, 0 )
    time.sleep(1)

async def main():
    # client for file transfer
    await client.connect()

    while True:
        t = time.localtime()
        cooldown = False
        current_date = time.strftime("%b-%d-%Y")
        db_time = datetime.now()
        current_time = time.strftime("%H-%M-%S", t)
        if cooldown == False:
            await center()
            camera.capture("temp.jpg")
            sleep(2)
            if pir.motion_detected:  # takes picture if detects motion
                filename = current_date + "_motion_image_" + current_time
                monitor_event = await camera_capture(current_time, "motion", filename)
                # await client.sendData(monitor_event)
                await client.sendFile(filename + ".jpg", monitor_event)
                cooldown = True
            if time.strftime("%M:%S", t) == "30:00":  # takes pictures at periods
                await down()
                sleep(2)
                filename = current_date + "_time_image_" + current_time
                monitor_event = await camera_capture(current_time, "periodic", filename)
                # await client.sendData(monitor_event)
                await client.sendFile(filename + ".jpg", monitor_event)
                #checks for plant growth weekly (sunday)
                if time.strftime("%w:%H:%M:%S",t) == "0:12:30:00":
                    plantdifference = plant_analysis(filename, pfile)
                    cv2.imwrite(filename + "_growth.jpg" , plantdifference)
                    data = {}
                    data["time"] = current_time
                    data["type"] = "growth"
                    data["filename"] = filename + "_growth.jpg"
                    await client.sendFile(filename + "_growth.jpg", data)
                    pfile = filename
                cooldown = True
        if cooldown == True:  # adds a 5 minute cooldown for pictures
            time.sleep(300)
            cooldown = False
        time.sleep(1)  # race condition fix


asyncio.run(main())