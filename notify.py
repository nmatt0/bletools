#!/usr/bin/env python3
from bleak import BleakClient, BleakScanner
import asyncio
import sys
import binascii
import time


u1 = "eb2eb8fd-ce11-44ac-babb-000000000001"
u2 = "eb2eb8fd-ce11-44ac-babb-000000000002"

def printstring(data):
    s = ""
    for b in data:
        if b >= 32 and b <= 127:
            s += chr(b)
        else:
            s += "."
    print("HEX: " + ''.join(format(x, '02x') for x in data))
    print("STRING: " + s)


def notify_callback(sender: int, data: bytearray):
    print(data.decode('utf-8'))
    #print(f"{sender}: {data}")

async def write(address):
    ret = True
    try:
        async with BleakClient(address) as client:
            print("connected!")
            await client.start_notify(u1,notify_callback)
            #await client.start_notify(u2,notify_callback)
            await asyncio.sleep(1.0)
            while True:
                data = await client.read_gatt_char(u1)
                printstring(data)
                await asyncio.sleep(1.0)
            #await client.stop_notify(u1)
            #await client.stop_notify(u2)
    except Exception as e:
        print("PRINTING ERROR:")
        print(e)
        ret = False
    return ret

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" <device MAC> <characteristic UUID> <DATA>")
    print("device MAC: MAC address of the BLE server")
    sys.exit(1)

address = sys.argv[1]

ret = asyncio.run(write(address))

if not ret:
    print("error")
