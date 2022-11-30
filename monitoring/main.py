import sys

sys.path.append("../")
import asyncio
import contract.contract as contract
from hub.network462 import MonitoringClient
from Sensor_array import *
import serial

def setColorByTemp(temp):
    temp = round(temp)
    r = (temp - 60) * 6 # set red (r)
    if r > 255: #bounding r to not go out of range for rgb
        r = 255
    elif r < 0:
        r = 0

    g = 0 #green unused for gradient

    b = 255 - (temp - 20) * 6 # set blue (b)
    if b > 255: #bounding b to not go out of range for rgb
        b = 255
    elif b < 0:
        b = 0
    rgb = f'{r},{g},{b}\n'
    return rgb

async def main():
    client = MonitoringClient(
        contract.System.MONITORING, contract.NETWORK_HOST, contract.NETWORK_PORT
    )
    await client.connect()
    sensors = SensorArray()
    ser = serial.Serial('/dev/ttyACM0',9600,timeout=1, write_timeout=0)
    ser.reset_input_buffer()
    ser.write('0,0,0'.encode('utf-8'))
    time.sleep(1)
    line = ser.readline().decode('utf-8').rstrip()
    #print("arduino:", line)
    print("connected")
    """
    water level / moisture are the most important, send those every second
    send the others every 5 seconds
    """
    count = 5
    try:
        while True:
            try:
                await client.sendWaterLevel(
                    contract.WaterLevelReadingMessage(sensors.getDepth())
                )

                await client.sendSoilMoisture(
                    contract.MoistureReadingMessage(
                        *[*sensors.getMoisture(), 0, 0, 0, 0]
                    )
                )

                if count <= 0:
                    await client.sendLightLevel(
                        contract.LightLevelReadingMessage(sensors.getLight())
                    )
                    await client.sendTemperature(
                        contract.TemperatureReadingMessage(sensors.getTemperature())
                    )
                    count = 5
                else:
                    count -= 1
                temperature = sensors.getTemperature()
                #print("temp:", temperature)
                rgb = setColorByTemp(temperature)
                #print(rgb)
                ser.write(str(rgb).encode('utf-8'))
                time.sleep(1)
                line = ser.readline().decode('utf-8').rstrip()
                #print("arduino:", line)
            except Exception as e:
                print(e)
                ser.write('0,0,0'.encode('utf-8'))
                time.sleep(0.5)
                line = ser.readline().decode('utf-8').rstrip()
                print("arduino:", line)
            await asyncio.sleep(1)
    finally:
        GPIO.cleanup()
        ser.write('0,0,0'.encode('utf-8'))
        time.sleep(0.5)
        line = ser.readline().decode('utf-8').rstrip()
        print("arduino:", line)


asyncio.run(main())
