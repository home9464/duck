# The Fake Duck
A raspberry project to drive a decoy duck. This "duck" will swim in the water like a duck as a decoy for duck huting. And if a real duck is shot down into the water, this "duck" will go and drag that duck back to the hunter at shoreline.


The duck hardware include:

- 2 x Raspberry Pi4

- 1 x [decoy duck](https://www.amazon.com/Decoys-Greenhead-Hunting-Plastic-Mallards/dp/B06XD85JWG/ref=sxin_13_pa_sp_search_thematic_sspa?cv_ct_cx=decoy+duck&keywords=decoy+duck&pd_rd_i=B06XD85JWG&pd_rd_r=fe9312dc-9279-4a5b-a99f-ccb52ab1fabf&pd_rd_w=0OXyX&pd_rd_wg=A4RHo&pf_rd_p=01ca3faa-aa5d-4f59-b840-a9a939665a91&pf_rd_r=742QMEWFJ92DEBQDXZFW&qid=1639210675&sr=1-1-a73d1c8c-2fd2-4f19-aa41-2df022bcb241-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFEOTJPOUJYWUs1TDgmZW5jcnlwdGVkSWQ9QTA3NDAwOTgzUVBVWlBOMDM1Sk1DJmVuY3J5cHRlZEFkSWQ9QTAzMjAzNTczUFpOS0lPQlI3OUYmd2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWMmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl). One for driving the duck, another is used as a remote controller.

- 2 x [HC 12](https://www.amazon.com/DAOKI-Wireless-Replace-Bluetooth-Antenna/dp/B07YKJ4LVF/ref=sr_1_3?crid=26M8YE5RDA7B3&keywords=hc12+module&qid=1639210037&sprefix=HC12+mo%2Caps%2C201&sr=8-3)
One as transmitter on controller, another one as receiver in the duck

- 1 x [Xbox One Controller](https://www.amazon.com/Xbox-Core-Controller-Robot-White-one/dp/B08DF26MXW/ref=sr_1_2?keywords=Xbox+One+Controller&qid=1639210153&sr=8-2)
The controller will connect to controller raspberry by wire

- 2 x [underwater thruster](https://www.amazon.com/LICHIFIT-Underwater-Propeller-Submarine-Accessories/dp/B07WY4MDYZ/ref=sr_1_10?keywords=waterproof+motor+CW+CCW&qid=1639210804&s=sporting-goods&sr=1-10-catcorr)
to move the duck

- 1 x [SG90 servo](https://www.amazon.com/Micro-Servos-Helicopter-Airplane-Controls/dp/B07MLR1498/ref=sr_1_3?crid=1UR26RCWCHGDK&keywords=sg90+servo&qid=1639211302&sprefix=SG90+se%2Caps%2C229&sr=8-3)
to deploy hook on the duck. The hook is used to capture real duck floating on water

## Serial port setup

2 x HC12 modules are used for communication between the duck and the controller. The setup steps are the same.

[Please follow this instruction for serial setup](serial.md#section)


## Gamepad setup

A Xbox gamepad is used as the remote controller

https://tutorials-raspberrypi.com/raspberry-pi-joystick-with-mcp3008/

Connect Xbox Controller to the Pi by USB

```bash
sudo apt-get install -y evtest
ls /dev/input/*
/dev/input/event0  /dev/input/event1  /dev/input/event2  /dev/input/js0  /dev/input/mice
```

## Auto start the duck service on booting (duck only)
Use systemd to start the servuce named "duck" when the system (Rasbian) booting.

Assuming the project dir is

```bash
/home/pi/Desktop/duck/
```


[duck.service](./duck.service)

### Install the service to systemd

```bash
sudo cp duck.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable duck
sudo systemctl start duck
sudo systemctl status duck

# optional
sudo systemctl stop duck
sudo systemctl disable duck
```

## Auto start the controller service on booting (controller only)
Use systemd to start the servuce named "duck" when the system (Rasbian) booting

[duckctl.service](./duckctl.service)


### Install the service to systemd

```bash
sudo cp duckctl.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable duckctl
sudo systemctl start duckctl
sudo systemctl status duckctl

# optional
sudo systemctl stop duckctl
sudo systemctl disable duckctl
```