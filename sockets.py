import asyncio
import time

import websockets

import smbus
bus = smbus.SMBus(1)
channel = 1
address = 0xa

async def hello(websocket, path):
    prev = time.time()
    while True:
        # print("awaiting")
        coords = await websocket.recv()
        # print("got")
        now = time.time()
        diff = now - prev
        # 100ms min time between calls to arduino
        if diff > 0.1:
            x = coords.split(":")[0]
            y = coords.split(":")[1]
            print(f"time diff was {diff}, x {x} and y {y}")
            prev = time.time()
            ESCset = 45 * y + 90
            turnSet = 90 * x + 90
            data = [int(turnSet), int(ESCset)]
            bus.write_i2c_block_data(address, 1, data)
        else:
            pass


start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
