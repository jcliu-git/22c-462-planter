"""
Library for CSCE 462 Final Project
"""
import asyncio
import json
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from threading import Thread
from types import AsyncGeneratorType
from typing import Any, AsyncGenerator, Generator
import websockets

sys.path.append("../")
import contract.contract as contract

Path("logs").mkdir(parents=True, exist_ok=True)
logname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_network.log"
logpath = f"logs/{logname}"
logging.basicConfig(filename=logpath, encoding="utf-8")


class ControlHub(object):
    """
    Control hub class
    =================
    Attributes:
        queue       asyncio queue for received messages and files

    Methods:
        sendData(system, data)
            Args:
                system (string/System): name of receiving pi
                data (any): any json serializable data
    """

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._server = None
        self._clients = {}
        self.websocket = None
        self.queue = asyncio.Queue()
        self.web_socket_server = None
        self.websockets = {}

    async def _webSocketListener(self, socket):
        self.websockets[socket.id] = socket
        try:
            async for message in socket:
                try:
                    # print(message)
                    await self.queue.put(json.loads(message))
                except Exception as err:
                    logging.error("Websocket message processing failed: %s", err)
        finally:
            del self.websockets[socket.id]

    async def _startWebSocketServer(self):
        async with websockets.serve(self._webSocketListener, "0.0.0.0", 5000) as server:
            self.web_socket_server = server
            await asyncio.Future()

    async def startServer(self):
        self._server = await asyncio.start_server(self._listen, self._host, self._port)
        asyncio.create_task(self._server.serve_forever())
        asyncio.create_task(self._startWebSocketServer())
        print("Server has started.")

    async def _listen(self, reader, writer):
        data = await reader.readline()
        system_name = data.decode("utf-8")[:-1]
        print(f"Client {system_name} has connected.")
        self._clients[system_name] = [reader, writer]
        while True:
            # print("waiting for data")
            data = await reader.readline()
            if not data:
                debugmsg = "Client " + system_name + " has disconnected."
                print(debugmsg)
                logging.warning(debugmsg)
                break
            # print(data)
            try:
                payload = json.loads(data)
                if payload["identifier"] == contract.MessageIdentifier.FILE:
                    filepath = "temp/" + payload["data"]["filename"]
                    # logging.info("File: %s", filepath)

                    # create directory if doesn't exist
                    Path("temp/").mkdir(parents=True, exist_ok=True)

                    # write to file
                    with open(filepath, "wb+") as file:
                        data = await reader.readexactly(payload["data"]["filesize"])
                        file.write(data)

                        # append queue and clean up
                        await self.queue.put(payload)
                        writer.write(b"\n")  # acknowledgement
                        await writer.drain()
                        writer.close()
                        # print("File transfer done. Removing", system_name)
                        del self._clients[system_name]
                        break
                else:
                    await self.queue.put(payload)
            except Exception as err:
                logging.error("Initial message processing failed: %s", err)

    async def sendData(self, system, data):
        writer = self._clients[str(system)][1]
        payload = contract.DataMessage(system, data)
        jsonpayload = json.dumps(payload, cls=contract.ContractEncoder) + "\n"
        encoded = bytes(jsonpayload, encoding="utf-8")
        try:
            writer.write(encoded)
            await writer.drain()
        except Exception as err:
            logging.error("Writing failed: %s", err)

    async def _sendContract(self, system, payload):
        writer = self._clients[str(system)][1]
        jsonpayload = json.dumps(payload, cls=contract.ContractEncoder) + "\n"
        encoded = bytes(jsonpayload, encoding="utf-8")
        try:
            writer.write(encoded)
            await writer.drain()
        except Exception as err:
            logging.error("Writing failed: %s", err)

    async def stream(self) -> AsyncGenerator[contract.Message, None]:
        while True:
            queueItem: contract.Message = await self.queue.get()
            # print(queueItem)
            try:
                yield contract.Message.fromJson(queueItem)
            except Exception as err:
                print("Error in stream: ", err)
                logging.error(err)
                continue


class Client(object):
    """
    Client class
    =================
    Attributes:
        queue       queue for received messages and files

    Methods:
        sendData(name, data)
            Args:
                name (string): name of receiving pi
                data (any): any json serializable data

        sendFile(source_path, destination_path, data)
            Args:
                source_path (string): Path of source file
                destination_path (string): Path of where the file is going to be placed on server
                data (any, optional): Any additional data that would help the server figure out
                    what to do with the file. Defaults to None.
    """

    def __init__(self, system, host, port):
        self._system = system
        self._host = host
        self._port = port
        self._reader = None
        self._writer = None
        self._file_counter = 0
        self.queue = asyncio.Queue()

    async def connect(self):
        """
        Connect to the server
        """
        try:
            # print("connecting")
            self._reader, self._writer = await asyncio.open_connection(
                self._host, self._port
            )
            # print("connection established")

            # send system name to server
            encoded = str(self._system) + "\n"
            self._writer.write(encoded.encode("utf-8"))
            await self._writer.drain()

            asyncio.create_task(self._receive_messages())
        except Exception as err:
            logging.error("Disconnected: %s", err)

    async def _receive_messages(self):
        while True:
            data = await self._reader.readline()
            if not data:
                logging.error("Server has disconnected.")
                break
            try:
                payload = json.loads(data)
                if payload["type"] == "data":
                    await self.queue.put(payload)
            except Exception as err:
                logging.error("Processing received message failed: %s", err)

    async def _sendData(self, data):
        """Generic data function, shouldn't be used with contracts

        Args:
            data (any): any json serializable datatype
        """
        if self._writer is not None:
            payload = contract.DataMessage(self._system, data)
            jsonpayload = json.dumps(payload, cls=contract.ContractEncoder) + "\n"
            encoded = bytes(jsonpayload, encoding="utf-8")
            self._writer.write(encoded)
            await self._writer.drain()
        else:
            logging.error("Socket has been closed or does not exist.")

    async def _sendContract(self, payload):
        if self._writer is not None:
            jsonpayload = json.dumps(payload, cls=contract.ContractEncoder) + "\n"
            encoded = bytes(jsonpayload, encoding="utf-8")
            self._writer.write(encoded)
            await self._writer.drain()
        else:
            logging.error("Socket has been closed or does not exist.")

    async def _send_file(self, source_path, data):
        # try open
        try:
            with open(source_path, "rb") as file:
                # file size
                file.seek(0, os.SEEK_END)
                file_size = file.tell()

                # connect to server
                reader, writer = await asyncio.open_connection(self._host, self._port)
                encoded = str(self._system) + f"_f{self._file_counter}\n"
                self._file_counter += 1
                if self._file_counter > 512:
                    self._file_counter = 0
                writer.write(encoded.encode("utf-8"))
                await writer.drain()
                filename = source_path.split("/")[-1]
                # send file info
                payload = contract.FileMessage(self._system, filename, file_size, data)
                # print(payload)
                jsonpayload = json.dumps(payload, cls=contract.ContractEncoder) + "\n"
                # print(jsonpayload)
                writer.write(bytes(jsonpayload, encoding="utf-8"))
                await writer.drain()

                # send file
                file.seek(0, 0)
                await asyncio.sleep(1)
                read = file.read()
                writer.write(read)

                # cleanup
                await writer.drain()
                file.close()
                acknowledgement = await reader.readline()
                writer.close()
        except Exception as err:
            logging.error("Error: %s", err)

    async def _send_file_contract(self, source_path, payload):
        # try open
        try:
            with open(source_path, "rb") as file:
                # file size
                file.seek(0, os.SEEK_END)
                file_size = file.tell()

                # connect to server
                reader, writer = await asyncio.open_connection(self._host, self._port)
                encoded = str(self._system) + f"_f{self._file_counter}\n"
                self._file_counter += 1
                if self._file_counter > 512:
                    self._file_counter = 0
                writer.write(encoded.encode("utf-8"))
                await writer.drain()
                filename = source_path.split("/")[-1]
                payload.data["filesize"] = file_size
                payload.data["filename"] = filename
                # send file info
                # print(payload)
                jsonpayload = json.dumps(payload, cls=contract.ContractEncoder) + "\n"
                # print(jsonpayload)
                writer.write(bytes(jsonpayload, encoding="utf-8"))
                await writer.drain()

                # send file
                file.seek(0, 0)
                await asyncio.sleep(1)
                read = file.read()
                writer.write(read)

                # cleanup
                await writer.drain()
                file.close()
                acknowledgement = await reader.readline()
                writer.close()
        except Exception as err:
            logging.error("Error: %s", err)

    async def _sendFile(self, source_path, data=None):
        """
        Send file to server

        Args:
            source_path (string): Path of source file
            destination_path (string): Path of where the file is going to be placed on server
            data (any, optional): Any additional data that would help the server figure out
                what to do with the file. Defaults to None.
        """
        # sending files is slow, better to do it on a different thread in a separate event loop
        thread = Thread(
            target=asyncio.run, args=(self._send_file(source_path, data),), daemon=True
        )
        thread.start()

    async def _sendFileContract(self, source_path, contract):
        thread = Thread(
            target=asyncio.run,
            args=(self._send_file_contract(source_path, contract),),
            daemon=True,
        )
        thread.start()

    async def stream(self) -> AsyncGeneratorType[contract.IMessage, None]:
        while True:
            queueItem = await self.queue.get()
            yield contract.Message.fromJson(queueItem)


"""
HUB = "hub"
MONITORING = "monitor"
SUBSURFACE = "subsurface"
CAMERA = "camera"
IRRIGATION = "irrigation"
"""


class MonitoringClient(Client):
    def __init__(
        self,
        system: contract.System = contract.System.MONITORING,
        host: str = contract.NETWORK_HOST,
        port: int = contract.NETWORK_PORT,
    ):
        super().__init__(system, host, port)

    async def sendWaterLevel(self, message: contract.WaterLevelReadingMessage):
        await self._sendContract(message)

    async def sendTemperature(self, message: contract.TemperatureReadingMessage):
        await self._sendContract(message)

    async def sendLightLevel(self, message: contract.LightLevelReadingMessage):
        await self._sendContract(message)


class CameraClient(Client):
    def __init__(
        self,
        system: contract.System = contract.System.CAMERA,
        host: str = contract.NETWORK_HOST,
        port: int = contract.NETWORK_PORT,
    ):
        super().__init__(system, host, port)

    async def sendImage(self, source_path: str, data: contract.PhotoCaptureMessage):
        await self._sendFileContract(source_path, data)
