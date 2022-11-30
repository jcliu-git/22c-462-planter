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
from gpiozero import MotionSensor
import RPi.GPIO as GPIO
from plantcv import plantcv as pcv
import cv2
from hub.network462 import CameraClient
from time import sleep
import numpy as np

# client = Client("test", "192.168.3.114", 32132)
client = CameraClient(host="192.168.3.128")

# devices
pir = MotionSensor(4)
camera = PiCamera()
camera.rotation = 90
# servos setup
servo180 = pigpio.pi()  # 180 servo
servo360 = pigpio.pi()  # 360 servo
pfile = "temp"


async def camera_capture(time, phototype, filename):

    # execute_query(connection, monitor_event)
    
    camera.start_preview()
    sleep(5)
    camera.capture(filename + ".jpg")
    camera.stop_preview()

    data = contract.PhotoCaptureMessage(filename, phototype)
    """
    data = {}
    data["time"] = time
    data["type"] = phototype
    data["filename"] = filename
    """

    # await client.sendFile(filename+ ".jpg", filename+ ".jpg")
    return data


async def plant_analysis(filename, pfile):
    plant1_o = cv2.imread(filename + ".jpg")
    plant2_o = cv2.imread(pfile + ".jpg")

    pcv.params.debug = "print"

    # Isolate plant in first image
    y_channel1 = pcv.rgb2gray_cmyk(rgb_img=plant1_o, channel="Y")
    m_channel1 = pcv.rgb2gray_cmyk(rgb_img=plant1_o, channel="M")
    plant1 = cv2.subtract(y_channel1, m_channel1)
    plant1 = pcv.closing(gray_img=plant1)
    plant1 = pcv.erode(gray_img=plant1, ksize=3, i=10)
    plant1 = pcv.closing(gray_img=plant1)
    mask1 = cv2.threshold(plant1, 35, 255, cv2.THRESH_BINARY)[1]
    mask1 = pcv.fill_holes(bin_img=mask1)
    plant1 = pcv.apply_mask(img=plant1_o, mask=mask1, mask_color="white")
    plant1 = pcv.erode(gray_img=plant1, ksize=3, i=10)

    # Isolate plant in second image
    y_channel2 = pcv.rgb2gray_cmyk(rgb_img=plant2_o, channel="Y")
    m_channel2 = pcv.rgb2gray_cmyk(rgb_img=plant2_o, channel="M")
    plant2 = cv2.subtract(y_channel2, m_channel2)
    plant2 = pcv.closing(gray_img=plant2)
    plant2 = pcv.erode(gray_img=plant2, ksize=15, i=10)
    plant2 = pcv.closing(gray_img=plant2)
    mask2 = cv2.threshold(plant2, 35, 255, cv2.THRESH_BINARY)[1]
    mask2 = pcv.fill_holes(bin_img=mask2)
    plant2 = pcv.apply_mask(img=plant2_o, mask=mask2, mask_color="white")
    plant2 = pcv.erode(gray_img=plant2, ksize=3, i=10)

    # Take difference of both plants
    plantdifference = cv2.subtract(plant1, plant2)
    plantdifference = pcv.erode(gray_img=plantdifference, ksize=3, i=10)

    # Remove white background noise from difference image
    th = 200 # defines the value below which a pixel is considered "white"
    #white_pixels = np.where(
     #   (plantdifference[:, :, 0] > th) & 
      #  (plantdifference[:, :, 1] > th) & 
       # (plantdifference[:, :, 2] > th)
       # )
    # set those pixels to black
    #plantdifference[white_pixels] = [0, 0, 0]
    cv2.imwrite(filename + "_growth.jpg", plantdifference)
    return plantdifference


def motion_detect():
    #uses before and after to see if there is motion
    before = cv2.imread("temp.jpg")
    after = cv2.imread("temp2.jpg")
    diff = 255 - cv2.absdiff(before, after)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200)
    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contours, key = cv2.contourArea, reverse = True)
    if len(sorted_contours) != 0:
        largest_item = sorted_contours[0]
        cv2.drawContours(diff, largest_item, -1 (255,0,0),10)
        cont_area = cv2.contourArea(largest_item)
    else:
        cont_area = 0
    return cont_area  


# servo definitions


async def up():
    servo180.set_mode(servo180, pigpio.OUTPUT)
    servo180.set_PWM_frequency(17, 50)
    servo180.set_servo_pulsewidth(17, 1200)
    time.sleep(3)
    servo180.set_PWM_dutycycle(17, 0)
    servo180.set_PWM_frequency(17, 0)


async def center():
    servo180.set_mode(servo180, pigpio.OUTPUT)
    servo180.set_PWM_frequency(17, 50)
    servo180.set_servo_pulsewidth(17, 1500)
    time.sleep(3)
    servo180.set_PWM_dutycycle(17, 0)
    servo180.set_PWM_frequency(17, 0)


async def down():
    servo180.set_mode(servo180, pigpio.OUTPUT)
    servo180.set_PWM_frequency(17, 50)
    servo180.set_servo_pulsewidth(17, 1850)
    time.sleep(3)
    servo180.set_PWM_dutycycle(17, 0)
    servo180.set_PWM_frequency(17, 0)


async def right90():
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27, 700)
    time.sleep(0.16)
    servo360.set_PWM_dutycycle(27, 0)
    servo360.set_PWM_frequency(27, 0)
    time.sleep(1)


async def right45():
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27, 1100)
    time.sleep(0.08)
    servo360.set_PWM_dutycycle(27, 0)
    servo360.set_PWM_frequency(27, 0)
    time.sleep(1)


async def left45():
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27, 1900)
    time.sleep(0.08)
    servo360.set_PWM_dutycycle(27, 0)
    servo360.set_PWM_frequency(27, 0)
    time.sleep(1)


async def left90():
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27, 2000)
    time.sleep(0.16)
    servo360.set_PWM_dutycycle(27, 0)
    servo360.set_PWM_frequency(27, 0)
    time.sleep(1)

async def center2():
    servo360.set_mode(27, pigpio.OUTPUT)
    servo360.set_PWM_frequency(27, 50)
    servo360.set_servo_pulsewidth(27, 1500)
    time.sleep(0.16)
    servo360.set_PWM_dutycycle(27, 0)
    servo360.set_PWM_frequency(27, 0)
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
            print("running")
            await center()
            await center2()
            camera.start_preview()
            time.sleep(5)
            camera.capture("temp.jpg")
            camera.stop_preview()
            time.sleep(2)
            if pir.motion_detected:  # takes picture if detects motion
                camera.start_preview()
                time.sleep(5)
                camera.capture("temp2.jpg")
                camera.stop_preview()
                #checks to see if there is a new entity
                threshold = await motion_detect()
                if threshold > 200:
                    print("Motion Detected")
                    filename = current_date + "_motion_image_" + current_time
                    monitor_event = await camera_capture(current_time, "motion", filename)
                    await client.sendImage(filename + ".jpg", monitor_event)
                    time.sleep(30)
            if time.strftime("%M", t) == "30":  # takes pictures at periods
                await down()
                time.sleep(2)
                await center2()
                time.sleep(2)
                filename = current_date + "_time_image_" + current_time
                monitor_event = await camera_capture(current_time, "periodic", filename)
                await client.sendImage(filename + ".jpg", monitor_event)
                # checks for plant growth weekly (sunday)
                if time.strftime("%w:%H:%M", t) == "0:12:30":
                    global pfile
                    if (pfile != "temp"):
                        await plant_analysis(filename, pfile)
                        data = contract.PhotoCaptureMessage(filename + "_growth.jpg", contract.PhotoType.GROWTH)
                        await client.sendImage(filename + "_growth.jpg", data)
                    pfile = filename
                time.sleep(30)
        time.sleep(1)  # race condition fix


asyncio.run(main())
