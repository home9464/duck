"""communication via HC12 module

pip install pyserial

screen /dev/cu.usbserial-0001 9600

https://tutorials-raspberrypi.com/raspberry-pi-joystick-with-mcp3008/

"""

import time
import random
import serial

from cryptography.fernet import Fernet

#ENCRYPT_KEY = Fernet.generate_key()
# encrypt message with this key
ENCRYPT_KEY = b'--jV7tldirQ3UBd1Gn25D_4uSE5QZBRy8kWWT8SqDrU='
fernet = Fernet(ENCRYPT_KEY)

# all valid message MUST start with code
SECRET_CODE = '119743'

#HC12_DEVICE = '/dev/cu.usbserial-0001'

HC12_DEVICE = '/dev/ttyAMA1'
ser = serial.Serial(port=HC12_DEVICE, baudrate=9600, timeout = 2, writeTimeout = 2)
assert ser.is_open

def transmit(message):
    """transmit encoded and encrypted message over wireless serial port
    """
    formated_message = f'{SECRET_CODE}{message}'
    encrypted_message = fernet.encrypt(formated_message.encode())
    ser.write(encrypted_message+b'\n')  # to be read by receiver as readline()


