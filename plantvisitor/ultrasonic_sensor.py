import RPi.GPIO as GPIO
import time
import webbrowser
import sys
import OS
GPIO.setmode(GPIO.BCM)

TRIG = 16
ECHO = 18
print "Distance Measurement in Progress"

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        GPIO.output(TRIG, False)
        print "Waiting ..."
        time.sleep(2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if(distance <= 100 and windowopen==False):
            print "Distance: ", distance, "cm"
            webbrowser.open('file://' + os.path.realpath('hello.html'))
            windowopen = True
            time.sleep(2)
            os.system("Kill $(pidof dillo)")
            time.sleep(2)
            webbrowser.open("file://" + os.path.realpath("index.html"))
        if(distance > 100 and distance < 3000 and windowopen == True):
            print "Distance: ", distance, "cm"
            os.system("Kill $(pidof dillo)")
            time.sleep(2)
            webbrowser.open('file://' + os.path.realpath('goodbye.html'))
            os.system("Kill $(pidof dillo)")
            windowopen = False
except KeyboardInterrupt:
    print("Cleaning up!")
    GPIO.cleanup()
