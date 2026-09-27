from typing import Any
from bleak.backends.scanner import AdvertisementData

from .bthome import bthome_decoder

DECODERS = {
    'FCD2' : bthome_decoder,  # Allterco (BTHome)
}

def decode_ble_advertisment(adv_data:AdvertisementData, adv_mac:str) -> dict[str, Any]:
    """
    Decode the BLE advertisement
    MAC address is needed for some protocols (nonce in encrypted BTHome)
    """
    ret = {}

    if len(adv_data.service_data) > 1:
        # Given the short allowed length for a BLE advertisment data, this may never be the case.
        # The exact thing to do must be figured out the day it happens.
        print("WARNING: More than 1 item in service data. Protocol decode may produce weird results.")
        print(adv_data.service_data)

    for bleak_uid, raw_bytes in adv_data.service_data.items():
        # Find out what the vendor ID is. If there is a UUID, it's in chars 5 to 8.
        # Last part of the bleak_uid is a MAC address of the receiver
        # bleak_uid = '0000fcd2-0000-1000-8000-xxxxxxxxxxxx' --> BLE UUID is FCD2 (Allterco)
        ble_uuid = bleak_uid.split("-")[0][4:8].upper()
        ret['ble_uuid'] = ble_uuid
        ret['ble_data'] = raw_bytes.hex().upper()

        # Decode raw data if we have a decoder for given BLE UUID
        decoder = DECODERS.get(ble_uuid)
        if decoder:
            ret.update(decoder(adv_data, adv_mac))

    return ret

