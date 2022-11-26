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

    client = CameraClient()
    await client.connect()

    print("connected")

    while True:
        try:
            i = int(time.time())
            res = requests.get(f"https://source.unsplash.com/random/720x480?sig=${i}")
            with open(f"./temp/{i}.jpg", "wb") as f:
                f.write(res.content)

            await client.sendImage(
                f"./temp/{i}.jpg",
                contract.PhotoCaptureMessage(f"{i}.jpg", contract.PhotoType.PERIODIC),
            )

            await asyncio.sleep(1)

            await client.sendImage(
                f"./temp/{i}.jpg",
                contract.PhotoCaptureMessage(f"{i}.jpg", contract.PhotoType.MOTION),
            )

            os.remove(f"./temp/{i}.jpg")
        except Exception as e:
            print(e)

        finally:
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
