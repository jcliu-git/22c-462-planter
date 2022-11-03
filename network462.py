# TODO: clean up imports
import socket
import json
import threading
import os

from time import sleep

def _sendPayload(payload, socket):
    jsonpayload = json.dumps(payload)
    socket.sendall(bytes("%d\r\n" % len(jsonpayload) + jsonpayload , encoding="utf-8"))

def _preparePayload(name, type, data):
    payload = {
        "name": name,
        "type": type,
        "data": data
    }
    return payload

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
        self.acceptThread = threading.Thread(target=self._accept, daemon=True)
        self.acceptThread.start()

    # TODO: find out why this isn't being called
    def __del__(self):
        print("destructing")
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        for client in self.clients:
            print("try", client)
            self.clients[client][0].shutdown(socket.SHUT_RDWR)
            self.clients[client][0].close()
            self.clients[client][1].join()
            print("successful", client)
        print("try destruct accept")
        self.acceptThread.join()
        print("successful destruct accept")

    # listens for messages on each socket
    def _listen(self, name, conn, addr):
            while True:
                try:
                    originalMessage = conn.recv(1024)
                    message = originalMessage.splitlines()
                    lenPayloadSize = len(message[0])
                    payloadSize = int(message[0])
                    data = message[1][0:payloadSize]
                    #print("payload size: ", payloadSize)

                    largePayload = False
                    # if payload is larger than initial receive
                    if payloadSize > (1024 - lenPayloadSize):
                        remainingPayloadSize = payloadSize - (1024 - lenPayloadSize - 2)
                        message = conn.recv(remainingPayloadSize)
                        data += message
                        largePayload = True
                except Exception:
                    #print("Client disconnected")
                    conn.close()
                    del self.clients[name]
                    break

                #print(data)
                data = json.loads(data)

                if data['type'] == 'data':
                    self.queue.append(data)
                elif data['type'] == 'file':
                    #fileSize = data['data'][0]
                    filePath = data['data'][1]
                    file = open(filePath, 'wb')
                    if not largePayload:
                        file.write(originalMessage[lenPayloadSize+payloadSize+2:])
                    read = conn.recv(1024)
                    while read:
                        file.write(read)
                        read = conn.recv(1024)

                    # cleanup and send confirmation
                    file.close()
                    self.queue.append(data)
                    payload = _preparePayload('control','file', 0)
                    _sendPayload(payload, conn)
                    conn.close()
                    del self.clients[name]
                    break


    # continuously accept clients
    def _accept(self):
        try:
            while True:
                conn, addr = self.s.accept()
                # get name from client
                name = conn.recv(1024).decode('utf-8')
                thread = threading.Thread(target=self._listen, args=(name, conn, addr), daemon=True)
                thread.start()
                self.clients[name] = [conn, thread]
        except Exception:
            pass

    def sendData(self, name, data):
        conn = self.clients[name][0]
        payload = _preparePayload('control', 'data', data)
        _sendPayload(payload, conn)
    
class Client(object):
    s = None
    name = ''
    host = ''
    port = None
    queue = []
    listenThread = None

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port =  port
        self.s = socket.socket()
        self.s.connect((self.host, self.port))
        self.s.sendall(bytes(name, encoding="utf-8"))
        listenThread = threading.Thread(target=self._listen, daemon=True)
        listenThread.start()

    def __del__(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.listenThread.join()

    def _listen(self):
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

    def _sendFile(self, file, destinationPath, data):
        file.seek(0, os.SEEK_END)
        fileSize = file.tell()
        fileSock = socket.socket()
        fileSock.connect((self.host, self.port))
        fileSock.sendall(bytes(self.name + "#f", encoding="utf-8"))

        # send file info
        payload = _preparePayload(self.name, 'file', [fileSize, destinationPath, data])
        _sendPayload(payload, fileSock)

        # send file
        file.seek(0, 0)
        read = file.read(1024)
        while (read):
            fileSock.send(read)
            read = file.read(1024)

        # clean up and receive confirmation
        file.close()
        fileSock.shutdown(socket.SHUT_WR)  # signal to opposite end that sending is finished
        message = fileSock.recv(1024)
        fileSock.close()

    def sendData(self, data):
        payload = _preparePayload(self.name, 'data', data)
        _sendPayload(payload, self.s)

    def sendFile(self, sourcePath, destinationPath, data=None):  # sourcePath/destinationPath = path/to/file.png
        # try open
        file = open(sourcePath, 'rb')

        sendFileThread = threading.Thread(target=self._sendFile, args=(file, destinationPath, data), daemon=True)
        sendFileThread.start()