"""
Library for CSCE 462 Final Project
"""
# TODO: clean up imports
import asyncio
import datetime
import socket
import json
import sys
import threading
import os

from typing import AsyncGenerator, Generator

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import contract.contract as contract


#from time import sleep

def _send_payload(payload, payload_socket):
    jsonpayload = json.dumps(payload)
    payload_socket.sendall(bytes(f"{len(jsonpayload)}\r\n" + jsonpayload, encoding="utf-8"))

def _prepare_payload(name, message_type, data):
    payload = {
        "name": name,
        "type": message_type,
        "data": data
    }
    return payload




class ControlHub(object):
    """
    Control hub class
    =================
    Attributes:
        queue       queue for received messages and files
    
    Methods:
        sendData(name, data)
            Args:
                name (string): name of receiving pi
                data (any): any json serializable data
    """
    _s = None
    _accept_thread = None
    _clients = {}
    queue = []

    def __init__(self, host, port):
        """_summary_

        Args:
            host (_type_): _description_
            port (_type_): _description_
        """
        self._s = socket.socket()
        self._s.bind((host,port))
        self._s.listen()

        # daemon threads are not an elegant solution to stopping threads but it will do
        self._accept_thread = threading.Thread(target=self._accept, daemon=True)
        self._accept_thread.start()

    # TODO: find out why this isn't being called
    # is called on raspi but not on windows
    def __del__(self):
        #print("destructing")
        self._s.shutdown(socket.SHUT_RDWR)
        self._s.close()
        for client in self._clients.items():
            #print("try", client)
            client[0].shutdown(socket.SHUT_RDWR)
            client[0].close()
            client[1].join()
            #print("successful", client)
        #print("try destruct accept")
        self._accept_thread.join()
        #print("successful destruct accept")

    # listens for messages on each socket
    def _listen(self, name, conn, addr, residual):
        while True:
            try:
                original_message = conn.recv(1024)

                # edge case handling
                if residual:
                    original_message = residual + original_message
                    residual = None

                message = original_message.splitlines()
                length_payload_size = len(message[0])
                payload_size = int(message[0])
                data = message[1][0:payload_size]
                #print("payload size: ", payloadSize)

                large_payload = False
                # if payload is larger than initial receive
                if payload_size > (1024 - length_payload_size):
                    remaining_payload_size = payload_size - (1024 - length_payload_size - 2)
                    message = conn.recv(remaining_payload_size)
                    data += message
                    large_payload = True
            except Exception as error:
                print(name, "disconnected:", error)
                conn.close()
                del self._clients[name]
                break

            #print(data)
            data = json.loads(data)

            if data['type'] == 'data':
                self.queue.append(data)
            elif data['type'] == 'file':
                #fileSize = data['data'][0]
                file_path = data['data'][1]
                file = open(file_path, 'wb')

                if not large_payload:
                    file.write(original_message[length_payload_size+payload_size+2:])

                read = conn.recv(1024)

                while read:
                    file.write(read)
                    read = conn.recv(1024)

                # cleanup and send confirmation
                file.close()
                self.queue.append(data)
                payload = _prepare_payload('control','file', 0)
                _send_payload(payload, conn)
                conn.close()
                del self._clients[name]
                break


    # continuously accept clients
    def _accept(self):
        try:
            while True:
                conn, addr = self._s.accept()
                # get name from client
                original_message = conn.recv(64)
                message = original_message.splitlines()
                name = message[0].decode('utf-8')

                # edge case: payload received at the same time as name
                if len(message) > 1:
                    residual = original_message[len(message[0])+2:]
                else:
                    residual = None

                thread = threading.Thread(target=self._listen, args=(name, conn, addr, residual), daemon=True)
                thread.start()
                self._clients[name] = [conn, thread]

        except Exception as error:
            print("accepting", name,"failed:", error)
            conn.close()

    def sendData(self, name, data):
        conn = self._clients[name][0]
        payload = _prepare_payload('control', 'data', data)
        _send_payload(payload, conn)
    
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
    _s = None
    _name = ''
    _host = ''
    _port = None
    _listen_thread = None
    _file_counter = 0

    queue = []

    def __init__(self, name, host, port):
        self._name = name
        self._host = host
        self._port =  port
        self._s = socket.socket()
        self._s.connect((self._host, self._port))
        self._s.sendall(bytes(name + "\r\n", encoding="utf-8"))
        listen_thread = threading.Thread(target=self._listen, daemon=True)
        listen_thread.start()

    def __del__(self):
        if self._s:
            self._s.shutdown(socket.SHUT_RDWR)
            self._s.close()
        if self._listen_thread:
            self._listen_thread.join()

    def _listen(self):
        try:
            while True:
                message = self._s.recv(1024)
                message = message.splitlines()
                length_payload_size = len(message[0])
                payload_size = int(message[0])
                data = message[1]
                if payload_size > (1024 - length_payload_size):
                    message = self._s.recv(payload_size - (1024 - length_payload_size - 2))
                    data += message
                data = json.loads(data)
                if data['type'] == 'data':
                    self.queue.append(data)
                elif data['type'] == 'file':
                    # TODO: implement file transfer
                    pass
        except Exception as error:
            print("Error:", error)

    def _send_file(self, file, destination_path, data):
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file_sock = socket.socket()
        file_sock.connect((self._host, self._port))
        name_append = self._name + f"_f{self._file_counter}"
        self._file_counter += 1
        file_sock.sendall(bytes(name_append + "\r\n", encoding="utf-8"))

        # send file info
        payload = _prepare_payload(self._name, 'file', [file_size, destination_path, data])
        _send_payload(payload, file_sock)

        # send file
        file.seek(0, 0)
        read = file.read(1024)
        while read:
            file_sock.send(read)
            read = file.read(1024)

        # clean up and receive confirmation
        file.close()
        file_sock.shutdown(socket.SHUT_WR)  # signal to opposite end that sending is finished
        message = file_sock.recv(1024)
        file_sock.close()

    def disconnect(self):
        """
        Disconnect from server
        """
        self._s.close()
        self._s = None


    def sendData(self, data):
        """
        Send data to server

        Args:
            data (any): any json serializable data
        """
        payload = _prepare_payload(self._name, 'data', data)
        _send_payload(payload, self._s)

    # sourcePath/destinationPath = path/to/file.png
    def sendFile(self, source_path, destination_path, data=None):
        """
        Send file to server

        Args:
            source_path (string): Path of source file
            destination_path (string): Path of where the file is going to be placed on server
            data (any, optional): Any additional data that would help the server figure out
                what to do with the file. Defaults to None.
        """
        # try open
        file = open(source_path, 'rb')

        send_file_thread = threading.Thread(target=self._send_file,args=(file, destination_path, data), daemon=True)
        send_file_thread.start()



class StreamingClient(Client):
    _message_size = 1024
    _system = "client"

    _wsock = None
    _rsock = None

    def __init__(self, name: str, host: str, port: int):
        self._rsock, self._wsock = socket.socketpair()
        self._rsock.bind((host, port))
        self._wsock.bind((host, port))


    async def stream(self) -> AsyncGenerator[contract.Message, contract.Message]:
        reader, writer = await asyncio.open_connection(sock=self._rsock)


        while True:
            data = (await reader.read(100)).decode()

            try:
                message = json.loads(data)
                yield contract.Message(message['type'], message['type'], message['data'])

            except Exception as e:
                print(e)

    def sendData(self, data):
        if(self._wsock):
            self._wsock.sendall(bytes(json.dumps(data), encoding="utf-8"))

        


# on the sending side we want a clear interface to interact with
class SuburfaceClient(StreamingClient):
    def __init__(self, name: str = "subsurface", host: str = "127.0.0.1", port: int = 3000):
        super().__init__(name, host, port)

    def logMoistureData(self, data: contract.MoistureReadingMessage):
        """
            Send moisture data to hub
            if the timestamp is not specified it will be added for you
        """
        if data.timestamp is None:
            data.timestamp = datetime.datetime.now()

        
        self.sendData(data)

    # def logTemperatureData(self, data: contract.TemperatureData):
        # submodule has added this method indicating that they need to send this type of dat
        # is is up to the network module to decide how to send it
        # we want the client interface to widen only, which means we allow them
        # more freedom in how they give us the information and we accomodate their needs
        # we try not to impose new restrictions on them
        # raise NotImplementedError()
