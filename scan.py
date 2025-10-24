#!/usr/bin/env python3
from bleak import BleakScanner
import asyncio
import sys

async def scan(timeout):
    return await BleakScanner.discover(timeout=timeout, return_adv=True)

if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" <scan time>")
    sys.exit(1)
timeout=int(sys.argv[1])

# dict of {address: (BLEDevice, AdvertisementData)} (https://bleak.readthedocs.io/en/latest/api.html#bleak.backends.device.BLEDevice)
devices_and_adv = asyncio.run(scan(timeout))
devices_sorted = sorted(devices_and_adv.items(), key=lambda x: x[1][1].rssi, reverse=True)

for address, (device, adv_data) in devices_sorted:
    print(device.address)
    print("\tName: " + (device.name or "Unknown"))
    print("\tRSSI: " + str(adv_data.rssi))

