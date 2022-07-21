#!/usr/bin/env python3
from bleak import BleakScanner
import asyncio
import sys

async def scan(timeout):
    return await BleakScanner.discover(timeout=timeout)

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" <scan time>")
    sys.exit(1)
timeout=int(sys.argv[1])

# list of BLEDevice (https://bleak.readthedocs.io/en/latest/api.html#bleak.backends.device.BLEDevice)
devices = asyncio.run(scan(timeout))
for d in devices:
    print(d.address)
    print("\tName: "+d.name)
    print("\tRSSI: "+str(d.rssi))

