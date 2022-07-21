# bletools
BLE pentesting scripts

##

setup bluetooth on arch linux
```
pacman -S bluez bluez-utils
systemctl start bluetooth
bluetoothctl power on
```

## Example Server

use this project to run a GATT server:
https://github.com/Douglas6/cputemp

## Example Client Programs

All of the following client programs use the Bleak python library:
https://bleak.readthedocs.io/en/latest/index.html

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

