"""communication via HC12 module

pip install pyserial
"""

import time
import serial

HC12_DEVICE = '/dev/ttyAMA0'
ser = serial.Serial(port=HC12_DEVICE,
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)

print(ser)
counter = 0
while 1:
    x = ser.readline()
    print(x)