import socket
import json
import threading
from time import sleep

class ControlHub(object):
    s = None
    acceptThread = None
    clients = {}
    queue = []

    def __init__(self, host, port):
        self.s = socket.socket()
        self.s.bind((host,port))
        self.s.listen()

        # daemon threads are not an elegant solution to stopping threads but it will do
        self.acceptThread = threading.Thread(target=self.accept, daemon=True)
        self.acceptThread.start()

    # listens for messages on each socket
    def listen(self, conn, addr):
        try:
            while True:
                message = conn.recv(1024)
                message = message.splitlines()

                lenPayloadSize = len(message[0])
                payloadSize = int(message[0])
                data = message[1]
                #print("payload size: ", payloadSize)

                # if payload is larger than initial receive
                if payloadSize > (1024 - lenPayloadSize):
                    message = conn.recv(payloadSize - (1024 - lenPayloadSize - 2))
                    data += message

                data = json.loads(data)

                # handle different types of messages
                if data['type'] == 'data':
                    self.queue.append(data)
                elif data['type'] == 'file':
                    # TODO: implement file transfer
                    pass
        except Exception:
            # TODO: clean up from clients list
            pass

    # continuously accept clients
    def accept(self):
        try:
            while True:
                conn, addr = self.s.accept()
                # get name from client
                name = conn.recv(1024).decode('utf-8')
                thread = threading.Thread(target=self.listen, args=(conn, addr), daemon=True)
                thread.start()
                self.clients[name] = [conn, thread]
        except Exception:
            pass

    def sendData(self, name, data):
        conn = self.clients[name][0]
        payload = {
            "name": 'control',
            "type": 'data',
            "data": data
        }
        jsonpayload = json.dumps(payload)
        conn.sendall(bytes("%d\r\n" % len(jsonpayload) + jsonpayload , encoding="utf-8"))

    # TODO: find out why this isn't being called
    def __del__(self):
        print("destructing")
        self.s.shutdown(0)
        self.s.close()
        for client in self.clients:
            print("try", client)
            self.clients[client][0].shutdown(0)
            self.clients[client][0].close()
            self.clients[client][1].join()
            print("successful", client)
        print("try destruct accept")
        self.acceptThread.join()
        print("successful destruct accept")
    
class Client(object):
    s = None
    name = ''
    queue = []
    listenThread = None

    def __init__(self, name, host, port):
        self.name = name
        self.s = socket.socket()
        self.s.connect((host,port))
        self.s.sendall(bytes(name, encoding="utf-8"))
        listenThread = threading.Thread(target=self.listen, daemon=True)
        listenThread.start()

    def listen(self):
        try:
            while True:
                message = self.s.recv(1024)
                message = message.splitlines()
                lenPayloadSize = len(message[0])
                payloadSize = int(message[0])
                data = message[1]
                if payloadSize > (1024 - lenPayloadSize):
                    message = self.s.recv(payloadSize - (1024 - lenPayloadSize - 2))
                    data += message
                data = json.loads(data)
                if data['type'] == 'data':
                    self.queue.append(data)
                elif data['type'] == 'file':
                    # TODO: implement file transfer
                    pass
        except Exception:
            pass

    def sendData(self, data):
        payload = {
            "name": self.name,
            "type": 'data',
            "data": data
        }
        jsonpayload = json.dumps(payload)
        self.s.sendall(bytes("%d\r\n" % len(jsonpayload) + jsonpayload , encoding="utf-8"))
    
    def sendFile(self, path):
        # TODO: data: filesize, send payload size, open new socket for file transfer
        payload = {
            "name": self.name,
            "type": 'file',
            "data": None
        }
        jsonpayload = json.dumps(payload)
        self.s.sendall(bytes(jsonpayload, encoding="utf-8"))

    def __del__(self):
        self.s.shutdown(0)
        self.listenThread.join()