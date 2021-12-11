"""communication via HC12 module
git add . && git commit -m "add code" && git push
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
        direction = 0
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
                print(f'Servo: {angle}')
            elif message[:2] == 'D:':  # D:1 -> forward, D:2 backward, D:3 turn left, D:4 turn right
                direction = int(message[2:])
        except Exception as e:
            print(e)
        this_duck.drive(direction)
        print(f'Drive: {direction}')
    ser.close()

main()