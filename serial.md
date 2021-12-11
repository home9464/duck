## Communication via serial port

We are going to use 2 HC12 modules to communicate between two Raspberry Pi 4B boards


The HC12 module will need to use PIN 8 (TX) and PIN 10 (RX) to transmit data. However, to enable serial communication we have to disable bluetooth. So the XBox Game Controller can not connect to the Pi 4 through bluetooth. In this case,
we can either use wired connection or a 2.4 Ghz wirelss gamepad

### 1. change user group

```bash
sudo adduser pi dialout
```

### 2. install package and test connected serial device

```bash
pip install pyserial evdev cryptography

# see what ports are open
python -m serial.tools.list_ports

/dev/ttyAMA0
1 ports found
```

### 3. disable bluetooth

```bash
echo "dtoverlay=disable-bt" | sudo tee -a /boot/config.txt
sudo systemctl disable hciuart
sudo reboot
```

### 4. additional steps to remove possible serial exceptions

remove **<u>console=serial0,115200</u>** from /boot/cmdline.txt
```bash
sudo nano /boot/cmdline.txt
```

Change line from

```bash
console=tty1 console=serial0,115200 root=PARTUUID=fdc83649-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```

to

```bash
console=tty1 root=PARTUUID=fdc83649-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```


## References:

- https://stackoverflow.com/questions/28343941/python-serialexception-device-reports-readiness-to-read-but-returned-no-data-d

- https://howtoraspberrypi.com/enable-port-serial-raspberry-pi/
