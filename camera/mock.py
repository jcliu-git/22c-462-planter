import sys
import os
import asyncio
import time

sys.path.append("../")
import contract.contract as contract
from hub.network462 import CameraClient

import requests


async def main():
    if not os.path.isdir("temp"):
        os.mkdir("temp")

    client = CameraClient(host="127.0.0.1")
    await client.connect()

    print("connected")

    while True:
        try:
            i = int(time.time())
            res = requests.get(f"https://picsum.photos/720/480")
            with open(f"./temp/{i}.jpg", "wb") as f:
                f.write(res.content)

            await client.sendImage(
                f"./temp/{i}.jpg",
                contract.PhotoCaptureMessage(f"{i}.jpg", contract.PhotoType.PERIODIC),
            )

            await asyncio.sleep(1)

            i = int(time.time())
            res = requests.get(f"https://picsum.photos/720/480")
            with open(f"./temp/{i}.jpg", "wb") as f:
                f.write(res.content)

            await client.sendImage(
                f"./temp/{i}.jpg",
                contract.PhotoCaptureMessage(f"{i}.jpg", contract.PhotoType.MOTION),
            )

        except Exception as e:
            print(e)

        finally:
            await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
