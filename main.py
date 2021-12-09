"""communication via HC12 module

# if you see error like "serial.serialutil.SerialException: [Errno 13] could not open port /dev/ttyACM0: [Errno 13] Permission denied: ‘/dev/ttyACM0’."
sudo adduser pi dialout

pip install pyserial

# see what ports are open
python -m serial.tools.list_ports

"""

import time
import random
import serial

from cryptography.fernet import Fernet

# to control a servo to deploy a hook to capture the floating duck
from hook import RoboArm
from swim import ThisFakeDuck

HC12_DEVICE = '/dev/ttyAMA0'

#ENCRYPT_KEY = Fernet.generate_key()
# encrypt message with this key. Sender and receiver must use the same key
ENCRYPT_KEY = b'--jV7tldirQ3UBd1Gn25D_4uSE5QZBRy8kWWT8SqDrU='
fernet = Fernet(ENCRYPT_KEY)

# all valid message MUST start with code. ender and receiver must use the same code
SECRET_CODE = '119743'

ser = serial.Serial(port=HC12_DEVICE, baudrate=9600, timeout=1, writeTimeout=1)
assert ser.is_open

def main():
    arm = RoboArm()
    this_duck = ThisFakeDuck()
    while True:
        try:
            x = ser.readline()
            x = x.decode().strip().encode()
            decrypted_message = fernet.decrypt(x).decode()
            if not decrypted_message.startswith(SECRET_CODE):
                continue
            message = decrypted_message[6:]
            if message[:2] == 'A:':
                angle = int(message[2:])
                arm.angle(0, angle)
                print(f'Arm {angle}')
            elif message[:2] == 'D:':  # D:1 -> forward, D:2 backward, D:3 turn left, D:4 turn right
                direction = int(message[2:])
                this_duck.drive(direction)
                print(f'Drive {direction}')
        except Exception as e:
            print(e)
    ser.close()

main()