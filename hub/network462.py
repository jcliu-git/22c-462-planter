"""
Library for CSCE 462 Final Project
"""
import asyncio
import json
import os
import sys
from threading import Thread
from typing import Any, AsyncGenerator, Generator
sys.path.append("../")
import contract.contract as contract

# TODO: implement contracts
def _prepare_payload(system, message_type, data):
    payload = {"system": str(system), "type": str(message_type), "data": data}
    return payload

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
        self.queue = asyncio.Queue()

    async def startServer(self):
        self._server = await asyncio.start_server(self._listen, self._host, self._port)
        asyncio.create_task(self._server.serve_forever())

    async def _listen(self, reader, writer):
        data = await reader.readline()
        system_name = data.decode("utf-8")[:-1]
        print("client:", system_name)
        self._clients[system_name] = [reader, writer]
        while True:
            #print("waiting for data")
            data = await reader.readline()
            if not data:
                print("Client", system_name, "has disconnected.")
                break
            #print(data)
            try:
                payload = json.loads(data)
                if payload["type"] == "data":
                    await self.queue.put(payload)
                if payload["type"] == "file":
                    # TODO: create directory if doesn't exist

                    # write to file
                    filepath = payload["data"]["path"] + payload["data"]["filename"]
                    with open(filepath, "wb+") as file:
                        data = await reader.readexactly(payload["data"]["filesize"])
                        file.write(data)

                        # append queue and clean up
                        await self.queue.put(payload)
                        writer.write(b"\n")  # acknowledgement
                        await writer.drain()
                        writer.close()
                        print("deleting")
                        del self._clients[system_name]
                        break
            except Exception as err:
                print(err)
                break

    async def sendData(self, system, data):
        writer = self._clients[str(system)][1]
        payload = _prepare_payload(system, contract.MessageType.DATA, data)
        jsonpayload = json.dumps(payload) + "\n"
        encoded = bytes(jsonpayload, encoding="utf-8")
        writer.write(encoded)
        await writer.drain()
        
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

        sendFile(sour)
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
            #print("connecting")
            self._reader, self._writer = await asyncio.open_connection(self._host, self._port)
            #print("connection established")

            # send system name to server
            encoded = str(self._system) + "\n"
            self._writer.write(encoded.encode("utf-8"))
            await self._writer.drain()

            asyncio.create_task(self._receive_messages())
        except Exception as err:
            print("Disconnected:", err)

    async def _receive_messages(self):
        try:
            while True:
                data = await self._reader.readline()
                payload = json.loads(data)
                if payload["type"] == "data":
                    await self.queue.put(payload)
        except Exception as err:
            print(err)

    async def sendData(self, data):
        if self._writer is not None:
            payload = _prepare_payload(
                self._system,
                contract.MessageType.DATA,
                data
                )
            jsonpayload = json.dumps(payload) + "\n"
            encoded = bytes(jsonpayload, encoding="utf-8")
            self._writer.write(encoded)
            await self._writer.drain()
        else:
            print("Sending data failed")

    async def _send_file(self, source_path, destination_path, data):
        # try open
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

            # send file info
            filename = destination_path.split('/')[-1]
            path = destination_path[:len(destination_path)-len(filename)]
            # TODO: implement contracts
            #payload = contract.FileMessage(self._system, filename, path, file_size)
            payload = {
                "system": str(self._system),
                "type": "file",
                "data": {
                    "filename": filename,
                    "path": path,
                    "filesize": file_size,
                    "data": data
                }
            }
            jsonpayload = json.dumps(payload) + "\n"
            writer.write(bytes(jsonpayload, encoding="utf-8"))
            await writer.drain()

            # send file
            file.seek(0,0)
            await asyncio.sleep(1)
            read = file.read()
            writer.write(read)

            # cleanup
            await writer.drain()
            file.close()
            acknowledgement = await reader.readline()
            writer.close()

    async def sendFile(self, source_path, destination_path, data=None):
        """
        Send file to server

        Args:
            source_path (string): Path of source file
            destination_path (string): Path of where the file is going to be placed on server
            data (any, optional): Any additional data that would help the server figure out
                what to do with the file. Defaults to None.
        """
        # sending files is slow, better to do it on a different thread in a separate event loop
        thread = Thread(target=asyncio.run, args=(self._send_file(source_path, destination_path, data),), daemon = True)
        thread.start()