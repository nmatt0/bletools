# bletools
BLE pentesting scripts

## BLE Hacking Resources

- [Bluetooth Hacking: Tools And Techniques](https://www.youtube.com/watch?v=8kXbu2Htteg)
    - great intro to BLE hacking
- [Bluetooth: With Low Energy Comes Low Security](https://www.youtube.com/watch?v=Mo-FsEmaqpo)
    - talk about why Legacy Pairing is bad and how to defeat it
- [crackle](https://github.com/mikeryan/crackle/)
    - tool for cracking BLE Legacy Pairing
- [nRF Connect for Desktop](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop)
    - tool for use with nRF52840 USB dongle
    - not open source :(
- [Example Python GATT Server](https://github.com/Douglas6/cputemp)

## setup bluetooth on arch linux

```
pacman -S bluez bluez-utils
systemctl start bluetooth
bluetoothctl power on
```

## BLE Testing Tools

All of the following client programs use the Bleak python library:
https://bleak.readthedocs.io/en/latest/index.html

```
pip3 install bleak
```

### scan.py

This program scans for BLE devices that are advertising

```
usage: ./scan.py <scan time>
```

### services.py

This program connects to a BLE device and enumerates its services

```
usage: ./services.py <device MAC>
```

### read.py

This program connects to a BLE device and reads a characteristic

```
usage: ./read.py <device MAC> <characteristic UUID>
```

