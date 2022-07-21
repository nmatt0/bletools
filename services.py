#!/usr/bin/env python3
from bleak import BleakClient, BleakScanner
import asyncio
import sys
import binascii

async def services(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        return services
    return False


if len(sys.argv) < 2:
    print("usage: "+sys.argv[0]+" <device MAC>")
    print("device MAC: MAC address of the BLE server")
    sys.exit(1)

address = sys.argv[1]

services = asyncio.run(services(address))

if not services:
    print("not found")
else:
    for service in services:
        print(service)
        for char in service.characteristics:
            print(char)
            print(char.properties)
            #if "read" in char.properties:
