import asyncio
import websockets


async def handler(websocket):
    while True:
        try:
            async for message in websocket:
                print(message)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")


async def main():
    async with websockets.serve(handler, "", 5000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
