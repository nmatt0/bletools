import os
import binascii
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from cryptography.exceptions import InvalidTag

from bleak.backends.scanner import AdvertisementData

def bthome_decoder(adv_data:AdvertisementData, adv_mac:str) -> dict:
    """
    Parse the provided BTHome payload (UUID == FCD2)
    https://bthome.io/format/

    Encryption key can be passed as parameter (for testing)
    """
    ret = {}

    # Try to get encryption key from environment
    encryption_key = os.environ.get('BTHOME_KEY')

    for _, raw_bytes in adv_data.service_data.items():
        raw_hex = raw_bytes.hex().upper()

        # BTHome flags
        # bit 0: “Encryption flag” 1 (encrypted)
        # bit 1-4: “Reserved for future use”0000 (not used)
        # bit 5-7: “BTHome Version” 010 (version 2)
        device_data = raw_hex[0:2]  # needed for the nonce
        device_data_int = int(device_data, 16)
        is_encrypted = (device_data_int & 0x01) > 0

        ret['device_data'] = {
            'raw' : device_data,
            'version' : int(device_data_int >> 5 & 0x03),
            'encryption' : is_encrypted,
        }

        # Cleartext BTHome sensor data
        bthome_data = ""

        # Get encryption specific infos
        if is_encrypted:
            ret['encryption'] = {}

            if encryption_key:
                ret_encryption = bthome_decrypt("d2fc"+raw_hex, encryption_key, adv_mac)
                bthome_data = ret_encryption.pop("cleartext")
                ret['encryption'].update(ret_encryption)

            else:
                ret['encryption']['error'] = "No decryption key available."

        else:
            # Remove device data
            bthome_data = raw_hex[2:]

        ret['payload'] = {
            'raw' : bthome_data,
        } 
        ret['payload'].update(bthome_unpack(bthome_data))

    return {'bthome':ret}

def bthome_button_eventid(event_id:str)->str:
    """
    Convert BTHome button (0x3A) event id to string
    """
    return {
        '00' : 'None',
        '01' : 'press',
        '02' : 'double_press',
        '03' : 'triple_press',
        '04' : 'long_press',
        '05' : 'long_double_press',
        '06' : 'long_triple_press',
        '07' : 'hold_press',
    }[event_id.lower()]

def hex_to_uint(hexstr:str)->int:
    """Quick and dirty conversion"""
    return int(hexstr, 16)

def bthome_unpack(payload:str) -> dict:
    """
    Unpack the BTHome data
    https://bthome.io/format/

    Not all datatypes are (fully) implemented yet.
    """
    ret = {}

    datatypes = {
        # Key: object id in hex
        # Value: (length, label, conversion_function)
        '00' : (1, 'counter', hex_to_uint),  # uint8
        '01' : (1, 'battery', hex_to_uint),  # uint8
        '02' : (2, 'temperature', str),  # signed int16 * 0.01
        '03' : (2, 'humidity', str),  # unsigned int16 * 0.01
        '3a' : (1, 'button', bthome_button_eventid),
    }

    payload = payload.lower()

    idx = 0
    while idx < len(payload):
        idx_data = idx+2
        object_id = payload[idx:idx_data]
        length, label, conv = datatypes[object_id]
        idx_end = idx_data + 2*length
        data = payload[idx_data:idx_end]
        idx = idx_end
        ret[label] = conv(data)

    return ret

def bthome_decrypt(service_data:str, encryption_key:str , mac:str) -> dict:
    """
    Decryption function for BTHome data

    service_data must start with bthome uid

    https://bthome.io/encryption/
    https://github.com/Bluetooth-Devices/bthome-ble/blob/main/src/bthome_ble/bthome_v2_encryption.py
    """
    bthome_uid = service_data[0:4]
    if bthome_uid.lower() != "d2fc":
        return {'error':'Invalid BTHome payload (missing D2FC UID)'}

    device_data = service_data[4:6]  # 0x41
    mic = service_data[-8:]
    counter = service_data[-16:-8]
    ciphertext = service_data[6:-16]

    mac = mac.replace(":", "")

    # Build the nonce
    nonce = ""
    nonce += mac
    nonce += bthome_uid
    nonce += device_data
    nonce += counter

    ret_encryption = {
        'mic' : mic,
        'counter' : counter,
        'ciphertext' : ciphertext,
        'nonce' : nonce,
    }

    cipher = AESCCM(binascii.unhexlify(encryption_key), tag_length=4)

    try:
        decrypted_data = cipher.decrypt(
            binascii.unhexlify(nonce),
            binascii.unhexlify(ciphertext + mic),
            None,
        )
        ret_encryption['cleartext'] = decrypted_data.hex()

    except InvalidTag:
        # Straight from the documentation:
        # This will occur when the ciphertext has been changed,
        # but will also occur when the key, nonce, or associated data are wrong.
        ret_encryption['error'] = "Decryption failed (InvalidTag)"

    return ret_encryption

if __name__ == "__main__":
    """Let's test the functions"""

    # Test decryption with data from the example script
    mac = "54:48:E6:8F:80:A5"
    encryption_key = "231d39c1d7cc1ab1aee224cd096db932"
    service_data = "d2fc41e445f3c9962b332211006c7c4519"
    print(bthome_decrypt(service_data, encryption_key, mac))

    # Test BTHome payload unpacking
    # Counter, Battery, Temperature, Humdity, Button
    payload = "00AA013F02C40903BF133A01"
    print(bthome_unpack(payload))
