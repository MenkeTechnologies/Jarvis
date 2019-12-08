import asyncio
import sys
import threading
import time

import smbus
import websockets

import util

ARDUINO_WAIT = 0.050
bus = smbus.SMBus(1)
channel = 1
address = 0xa


def run():
    while True:
        # print("writing to i2c")
        time.sleep(1)
        bus.write_byte(address, 2)


async def hello(websocket, path):
    prev = time.time()
    print("connected")
    thread = threading.Thread(target=run, args=())
    thread.daemon = True
    thread.start()
    while True:
        msg = await websocket.recv()
        now = time.time()
        diff = now - prev
        if diff > ARDUINO_WAIT:
            cmdType = msg.split(util.CMD_DELIM)[0]
            cmd = msg.split(util.CMD_DELIM)[1]
            if cmdType == "joystick":
                x = cmd.split(":")[0]
                y = cmd.split(":")[1]
                print(f"cmd type {cmdType}, cmd:{cmd}, time diff was {diff}, x {x} and y {y}")
                prev = time.time()
                ESCset = 45 * float(y) + 90
                turnSet = 90 * float(x) + 90
                data = [int(turnSet), int(ESCset)]
                try:
                    pass
                    bus.write_i2c_block_data(address, 1, data)
                except:
                    print("could not write to i2c", file=sys.stderr)
        else:
            pass


start_server = websockets.serve(hello, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
