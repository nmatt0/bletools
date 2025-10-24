#!/usr/bin/env python3
from bleak import BleakClient, BleakScanner
import asyncio
import sys
import binascii
import time

d1 = bytearray.fromhex("a522010900170181a000781c0e63f0")
d2 = bytearray.fromhex("a522020500a901e2a40001")
d3 = bytearray.fromhex("a522090400a601e0a400")
d4 = bytearray.fromhex("a5220a05009201f1a40001")

def notify_callback(sender: int, data: bytearray):
    print(f"{sender}: {data}")

async def write(address,uuid,data):
    ret = True
    try:
        async with BleakClient(address) as client:
            await client.start_notify("0000fff1-0000-1000-8000-00805f9b34fb",notify_callback)
            await client.write_gatt_char(uuid,d1)
            await asyncio.sleep(1.0)
            await client.write_gatt_char(uuid,d2)
            await asyncio.sleep(1.0)
            await client.write_gatt_char(uuid,d3)
            await asyncio.sleep(1.0)
            await client.write_gatt_char(uuid,d4)
            await asyncio.sleep(10.0)
            await client.stop_notify("0000fff1-0000-1000-8000-00805f9b34fb")
    except Exception as e:
        print(e)
        ret = False
    return ret

if len(sys.argv) < 4:
    print("usage: "+sys.argv[0]+" <device MAC> <characteristic UUID> <DATA>")
    print("device MAC: MAC address of the BLE server")
    print("UUID: UUID of the BLE characteristic to write")
    print("DATA: data as hex string")
    sys.exit(1)

address = sys.argv[1]
uuid = sys.argv[2]
data = sys.argv[3]
data = bytearray.fromhex(data)

ret = asyncio.run(write(address,uuid,data))

if not ret:
    print("write error")
else:
    print("HEX: " + ''.join(format(x, '02x') for x in data))
    s = ""
    for b in data:
        if b >= 32 and b <= 127:
            s += chr(b)
        else:
            s += "."
    print("STRING: " + s)



