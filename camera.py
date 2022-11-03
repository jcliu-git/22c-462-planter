import time
import psycopg2
from datetime import date
from picamera import PiCamera
from gpiozero import MotionSensor
from network462 import Client
from time import sleep
import json

#client for file transfer
client = Client('test','127.0.0.1', 32132)
#devices
pir = MotionSensor(4)
camera = PiCamera()
#database
hostname = 'ec2-44-209-57-4.compute-1.amazonaws.com'
database = 'da41gg09sivbgs'
username = 'wzgfnyeewdbzlx'
pwd = '68b169eefd466125c85c00c9bf7a28c2a4137ea409591093a62b680eb20af23e'
port_id = 5432

conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)

def camera_capture(time,id,filename):
    cur = conn.cursor()
    sql = '''
    INSERT INTO monitor_event (time, id, file_name) 
    VALUES (%s, %s, %s)
    ''' % (time,id,filename)
    #execute_query(connection, monitor_event)
    camera.start_preview()
    sleep(5)
    camera.capture(filename + ".jpg")
    camera.stop_preview()
    #client.sendData(64\r\n{"name": ... "data": ... })
    #if client.queue:
    #    data = client.queue.pop(0)
    #    data = json.dumps(data, indent = 4) # pretty print data
    #    print(data)
    conn.close()

while True:
    today = date.today()
    t = time.localtime()
    cooldown = False
    current_date = time.strftime("%b-%d-%Y")
    current_time = time.strftime("%H:%M:%S", t)
    if cooldown == False:
        if (pir.motion_detected()): #takes picture if detects motion
            filename = current_date + "_motion_image_" + current_time
            camera_capture(current_time, "motion" , filename)
            cooldown = True
        if (time.strftime("%M:%S", t) == "30:00"): #takes pictures at periods
            filename = current_date + "_time_image_" + current_time
            camera_capture(current_time, "time", filename)
            cooldown = True
    if cooldown == True: #adds a 5 minute cooldown for pictures
        time.sleep(300)
        cooldown = False