import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import contract.contract as contract
from hub.network462 import SuburfaceClient


async def handle_messages(client: SuburfaceClient):
    stream = client.stream()

    async for message in stream:
        match message.system:
            case contract.System.HUB:
                print(f"Received message from HUB: {message.data}")


def main():
    client = SuburfaceClient()

    data = contract.MoistureReadingMessage(0.5)

    client.sendData(data)


if __name__ == "__main__":
    main()
