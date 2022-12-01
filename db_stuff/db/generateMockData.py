import psycopg2
from datetime import datetime, timedelta
import random

DATABASE_URL = "postgresql://vanle:password@localhost:5432/garden" #change from localhost to db to connect to database in container
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
curr = conn.cursor()

def insertDB(table: str, cols: str, data: str):
    print(f"INSERT INTO {table} ({cols}) VALUES({data})")
    curr.execute(f"INSERT INTO {table} ({cols}) VALUES({data})")


def insertMoistureLevel(timestamp,sensor_list):
    table = "moisture_level"
    cols = "timestamp, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8"
    values = timestamp + ','
    values += ",".join(str(val) for val in sensor_list)
    insertDB(table, cols, values)

def insertLight(timestamp, val):
    table = "light"
    cols = "timestamp, luminosity"
    values = timestamp + ',' + str(val)
    insertDB(table, cols, values)


def insertWaterLevel(timestamp,val):
    table = "water_level"
    cols = "timestamp,distance"
    values = timestamp + ',' + str(val)
    insertDB(table, cols, values)


def insertTemperature(timestamp,val):
    table = "temperature"
    cols = "timestamp, temperature"
    values = timestamp + ',' + str(val)
    insertDB(table, cols, values)

#Populate using 100 mock data every hour 
start_day = datetime(2022,11,26,7)
for i in range(1,101):
    timestamp = (start_day + timedelta(hours=1*i)).strftime('%Y-%m-%d %H:%M')
    timestamp ='\''+timestamp+'\''
    #Moisture Level
    sensor_val = [int(random.uniform(41000,44000)) for i in range(8)]
    insertMoistureLevel(timestamp,sensor_val)
    #Light
    insertLight(timestamp, int(random.uniform(5000,9999)))
    #Water Level
    insertWaterLevel(timestamp, round(random.uniform(10,50),2))
    #Temperature