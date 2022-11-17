import os
import sys
from typing import Any

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import contract.contract as contract
from hub.network462 import SuburfaceClient


async def handle_messages(client: SuburfaceClient):
    stream: Any = client.stream()

    async for message in stream:
        match message.system:
            case contract.System.SUBSURFACE:
                match message.type:
                    case contract.MessageType.MOISTURE_READING:
                        data = contract.MoistureReadingMessage.fromJson(message)


def main():
    client = SuburfaceClient()

    data = contract.MoistureReadingMessage(0.5)

    client.sendData(data)


if __name__ == "__main__":
    main()
