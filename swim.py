"""This is to control a motor driver MD03A from pololu.com
https://www.pololu.com/product/707/specs


The driver can control two DC motors. 

Each DC motor will drive a propeller (one is rotated Clockwise, another one is Counter Clock Wise)

To control two propellers we can control it to:

1. move forward
2. move backward
3. turn left
4. turn right


pip install RPi.GPIO

"""
import RPi.GPIO as GPIO


# On the Pi 4B and 400 (and CM4) you have two pairs of PWM channels.

# PWM0_0 available on GPIO 12, 18 or 52.
# PWM0_1 available on GPIO 13, 19, 45 or 53
# PWM1_0 available on GPIO 40
# PWM1_1 available on GPIO 41

BCM_PIN = {
    #'motor1_pwm': 18, 
    #'motor1_A': 15, 
    #'motor1_B': 14,

    'motor1_pwm': 18, 
    'motor1_A': 23, 
    'motor1_B': 24,

    'motor2_pwm': 27, 
    'motor2_A': 17, 
    'motor2_B': 22
}

BOARD_PIN = {
    #'motor1_pwm': 12, 
    #'motor1_A': 10, 
    #'motor1_B': 8,

    'motor1_pwm': 32, 
    'motor1_A': 31, 
    'motor1_B': 29,

    'motor2_pwm': 13, 
    'motor2_A': 11, 
    'motor2_B': 15
}

class Wheel:
    DIRECTION_FORWARD = 1
    DIRECTION_BACKWARD = 2
    DIRECTION_LEFT = 3
    DIRECTION_RIGHT = 4
    def __init__(self, mode=GPIO.BCM):  # or GPIO.BOARD
        GPIO.setmode(mode)  # Set Pi to use pin number when referencing GPIO pins.
        self.PIN = BCM_PIN if mode == GPIO.BCM else BOARD_PIN
        GPIO.setup(self.PIN['motor1_pwm'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_pwm'], GPIO.OUT)
        GPIO.setup(self.PIN['motor1_A'], GPIO.OUT)
        GPIO.setup(self.PIN['motor1_B'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_A'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_B'], GPIO.OUT)
        # the 1st motor
        self.pwm1 = GPIO.PWM(self.PIN['motor1_pwm'], 1000)   # Initialize PWM on pwmPin 1000Hz frequency
        # the 2nd motor
        self.pwm2 = GPIO.PWM(self.PIN['motor2_pwm'], 1000)   # Initialize PWM on pwmPin 1000Hz frequency
        self.pwm1.start(0) # Start the 1st motor  with 0% duty cycle
        self.pwm2.start(0) # Start the 2nd motor  with 0% duty cycle
        self.pwm1_forward_flag = 0
        self.pwm2_forward_flag = 0

    def stop(self):
        self.throttle(0)

    def _pin(self, a, b, c, d):
        GPIO.output(self.PIN['motor1_A'], a)
        GPIO.output(self.PIN['motor1_B'], b)
        GPIO.output(self.PIN['motor2_A'], c)
        GPIO.output(self.PIN['motor2_B'], d)

    def forward(self, percent=100):
        self.throttle(percent)
        self._pin(0, 1, 1, 0)

    def backward(self, percent=100):
        self.throttle(percent)
        self._pin(1, 0, 0, 1)

    def left(self, percent=100):
        self.throttle(percent)
        self._pin(0, 1, 0, 1)

    def right(self, percent=100):
        self.throttle(percent)
        self._pin(1, 0, 1, 0)

    def drive(self, direction:int, percent:int=100) -> None:
        assert 0 <= direction and direction <= 4
        if direction == 0:
            self.stop()
        elif direction == 1:
            self.forward(percent)
        elif direction == 2:
            self.backward(percent)
        elif direction == 3:
            self.left(percent)
        elif direction == 4:
            self.right(percent)
            
    def throttle(self, percentage: int = 100) -> None:
        assert 0 <= percentage and percentage <= 100
        self.pwm1.ChangeDutyCycle(percentage)
        self.pwm2.ChangeDutyCycle(percentage)

    def close(self):
        self.pwm1.stop()
        self.pwm2.stop()
        GPIO.cleanup()

if __name__ =='__main__':
    import time
    GPIO.cleanup()
    drive = Wheel()
    for direction in [1, 2, 3, 4]:
        drive.drive(direction)
        time.sleep(1)
    drive.drive(0)
    drive.close()