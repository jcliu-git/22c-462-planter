import RPi.GPIO as GPIO
import time

try:
    GPIO.setmode(GPIO.BOARD)

    trigger = 7
    echo = 11

    GPIO.setup(trigger, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    GPIO.output(trigger, GPIO.LOW)

    print("Waiting for sensor to settle")

    time.sleep(2)

    print("Calculating distance")

    GPIO.output(trigger, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(trigger, GPIO.LOW)

    while GPIO.input(echo)==0:
        pulse_start_time = time.time()
    while GPIO.input(echo)==1:
        pulse_end_time = time.time()
    
    pulse_duration = pulse_end_time - pulse_start_time

    distance = round(pulse_duration * 17150, 2)#17150 is some constant multiple to convert input to cm

    print("Distance:", distance, "cm")

finally:
    GPIO.cleanup()
