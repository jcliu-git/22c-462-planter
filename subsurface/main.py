import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import contract.message as message
from hub.network462 import Client

if __name__ == "__main__":

    client = Client("subsurface", "127.0.0.1", 3000)

    data: message.MoistureReading = {
        "name": "moisture",
        "type": message.MessageType.DATA,
        "system": message.System.SUBSURFACE,
        "data": {"moisture": 2.1, "timestamp": 123456789},
    }

    client.sendData(data)
