"""communication via HC12 module

pip install pyserial

# see what ports are open
python -m serial.tools.list_ports

"""

import time
import serial

HC12_DEVICE = '/dev/ttyAMA0'
ser = serial.Serial(port=HC12_DEVICE, baudrate=9600, timeout=2, writeTimeout=0)

print(ser.is_open)

counter = 0
while True:
    #ser.write(bytes(b'your_commands'))
    #ser.flush()
    x = ser.readline()
    print(x)

    #print('OK')
    #ser.close()