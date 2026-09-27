#!/usr/bin/env python3
import argparse
from bleak import BleakScanner
import asyncio
import json, collections
from ble_decoders import decode_ble_advertisment

parser = argparse.ArgumentParser()
parser.add_argument("timeout", help="Scan time", type=int)
parser.add_argument("--decode", help="Try to decode advertisement data", action="store_true")
parser.add_argument("--json", help="JSON output", action="store_true")
parser.add_argument("--filter", help="Filter MAC addresses starting with FILTER", default="")
args = parser.parse_args()

async def scan(timeout):
    return await BleakScanner.discover(timeout=timeout, return_adv=True)


# dict of {address: (BLEDevice, AdvertisementData)} (https://bleak.readthedocs.io/en/latest/api.html#bleak.backends.device.BLEDevice)
devices_and_adv = asyncio.run(scan(args.timeout))
devices_sorted = sorted(devices_and_adv.items(), key=lambda x: x[1][1].rssi, reverse=True)

ret = collections.OrderedDict()

for address, (device, adv_data) in devices_sorted:
    if args.filter and not device.address.lower().startswith(args.filter.lower()):
        continue

    device_name = (device.name or "Unknown")
    ret[device.address] = {
        'name' : device_name,
        'rssi' : str(adv_data.rssi),
    }

    decoded_data = None
    if args.decode:
        decoded_data = decode_ble_advertisment(adv_data, device.address)
        ret[device.address]['data'] = decoded_data
            
    if not args.json:
        print(device.address)
        print("\tName: " + device_name)
        print("\tRSSI: " + str(adv_data.rssi))
        if decoded_data:
            print("\tService Data: "+ str(decoded_data))

if args.json:
    print(json.dumps(ret, indent=2))
