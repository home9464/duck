"""communication via HC12 module

pip install pyserial
"""

import time
import serial

HC12_DEVICE = '/dev/cu.usbserial-0001'

ser = serial.Serial(port=HC12_DEVICE, baudrate=9600, timeout = 1, writeTimeout = 1)


print(ser.is_open)
counter = 0
#while True:
#    x = ser.readline()
#    print(x)

while True:
    ser.write(bytes(b'your_commands'))
    ser.flush()
    time.sleep(1)
    print('OK')
