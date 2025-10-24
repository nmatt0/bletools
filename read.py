#!/usr/bin/env python3
from bleak import BleakClient, BleakScanner
import asyncio
import sys
import binascii

async def read(address,uuid):
    data = False
    try:
        async with BleakClient(address) as client:
            print(client.mtu_size)
            #client.mtu_size = 512
            data = await client.read_gatt_char(uuid)
    except Exception as e:
        print(e)
    return data

if len(sys.argv) < 3:
    print("usage: "+sys.argv[0]+" <device MAC> <characteristic UUID>")
    print("device MAC: MAC address of the BLE server")
    print("UUID: UUID of the BLE characteristic to read")
    sys.exit(1)

address = sys.argv[1]
uuid = sys.argv[2]

data = asyncio.run(read(address,uuid))

if not data:
    print("not found")
else:
    print("HEX: " + ''.join(format(x, '02x') for x in data))
    s = ""
    for b in data:
        if b >= 32 and b <= 127:
            s += chr(b)
        else:
            s += "."
    print("STRING: " + s)



