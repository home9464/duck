# duck
a raspberry project to drive a duck decoy.

1. It will "swim" in the water like a duck as a decoy for duck huting
2. Once the duck is shot down into the water, it will go and drag the duck back to the hunter

```bash
git add . && git commit -m "add code" && git push
```

## Serial port setup

We are going to use 2 HC12 modules to communicate between two Raspberry Pi 4B boards


reference:

https://howtoraspberrypi.com/enable-port-serial-raspberry-pi/


if you see error like "serial.serialutil.SerialException: [Errno 13] could not open port /dev/ttyACM0: [Errno 13] Permission denied: ‘/dev/ttyACM0’."

```bash
sudo adduser pi dialout
```

install package and test connected serial device

```bash
pip install pyserial

# see what ports are open
python -m serial.tools.list_ports

/dev/ttyAMA0
1 ports found
```

Now also need to change the settings

```bash
echo "dtoverlay=disable-bt" | sudo tee -a /boot/config.txt
sudo systemctl disable hciuart
sudo reboot
```


https://stackoverflow.com/questions/28343941/python-serialexception-device-reports-readiness-to-read-but-returned-no-data-d

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


By default, the communication between the serial port is wide open.

```bash
pip install cryptography
```

## joystick

We also need a joystick as the remote controller

https://tutorials-raspberrypi.com/raspberry-pi-joystick-with-mcp3008/




