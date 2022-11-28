import psycopg2
import sys
from psycopg2 import pool
from dotenv import dotenv_values
from azure.storage.blob import BlobServiceClient
import os

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), ".."))
import contract.contract as contract




class Services:
    def __init__(self, hub) -> None:
        self.hub = hub
        self.config = dotenv_values(".env")

        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.config["AZURE_STORAGE_CONNECTION_STRING"]
        )
        self.container_name = "images"
        self.connection = psycopg2.connect(self.config['AZURE_PG_URI'])
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

        self.rows = {
            "light": ["id", "luminosity", "timestamp"],
            "moisture_level": [
                "id",
                "sensor1",
                "sensor2",
                "sensor3",
                "sensor4",
                "sensor5",
                "sensor6",
                "sensor7",
                "sensor8",
                "timestamp",
            ],
            "photos": ["id", "timestamp", "filepath", "width", "height", "phototype"],
            "temperature": ["id", "fahrenheit", "timestamp"],
            "water_level": ["id", "timestamp", "distance"],
        }

    def omit(self, obj, *keys):
        return {k: v for k, v in obj.items() if k not in keys}

    def parseRows(self, cursor, table: str):
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(self.rows[table], row)))
        return [self.omit(row, "id") for row in result]

    def insertDB(self, table: str, cols: str, data: str):
        self.cursor.execute(f"INSERT INTO {table} ({cols}) VALUES({data})")
        

    def insertMoistureLevel(self):
        try:
            moisture = self.hub.state["dashboard"]["moisture"]
            table = "moisture_level"
            cols = "timestamp, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8"
            values = ",".join(
                str(x)
                for x in [
                    f"timestamp '{moisture['timestamp']}'",
                    moisture["sensor1"],
                    moisture["sensor2"],
                    moisture["sensor3"],
                    moisture["sensor4"],
                    moisture["sensor5"],
                    moisture["sensor6"],
                    moisture["sensor7"],
                    moisture["sensor8"],
                ]
            )
            self.insertDB(table, cols, values)
        except Exception as e:
            print("error inserting moisture level: ", e)

    def insertLight(self):
        try:
            light = self.hub.state["dashboard"]["light"]
            table = "light"
            cols = "timestamp, luminosity"
            values = ",".join(
                str(x)
                for x in [f"timestamp '{light['timestamp']}'", light["luminosity"]]
            )
            self.insertDB(table, cols, values)
        except Exception as e:
            print("error inserting light: ", e)

    def insertWaterLevel(self):
        try:
            waterLevel = self.hub.state["dashboard"]["waterLevel"]
            table = "water_level"
            cols = "timestamp,distance"
            values = ",".join(
                str(x)
                for x in [
                    f"timestamp '{waterLevel['timestamp']}'",
                    waterLevel["distance"],
                ]
            )
            self.insertDB(table, cols, values)
        except Exception as e:
            print("error inserting water level: ", e)

    def insertTemperature(self):
        try:
            temperature = self.hub.state["dashboard"]["temperature"]
            table = "temperature"
            cols = "timestamp, fahrenheit"
            values = ",".join(
                str(x)
                for x in [
                    f"timestamp '{temperature['timestamp']}'",
                    temperature["fahrenheit"],
                ]
            )
            self.insertDB(table, cols, values)
        except Exception as e:
            print("error inserting temperature: ", e)

    def uploadImage(self, message: contract.PhotoCaptureMessage):
        filename = message.data["filename"]
        type = message.data["phototype"]
        print("processing file: " + filename)

        upload_file_path = f"temp/{filename}"
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, blob=filename
        )
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

        self.insertDB(
            "photos",
            "timestamp, filepath, width, height, phototype",
            f"timestamp '{message.data['timestamp']}', '{blob_client.url}', {message.data['width']}, {message.data['height']}, '{type}'",
        )

        os.remove(upload_file_path)
