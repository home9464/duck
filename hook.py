"""This is used to control a servo to deploy a hook for capturing the duck.

https://www.aranacorp.com/en/using-a-pca9685-module-with-raspberry-pi/

pip install adafruit-circuitpython-servokit
"""
from adafruit_servokit import ServoKit

class Servo:
    def __init__(self, max_angle=180):
        servos_indices = [0]  # only use one servo
        self.servokit = ServoKit(channels=16)
        self.max_angle = 180
        for i in servos_indices:
            self.servokit.servo[i].set_pulse_width_range(450, 2450)
            self.servokit.servo[i].actuation_range = self.max_angle

    def angle(self, index:int, angle:int)-> None:
        """
        Args:
        """
        #assert 0 <= index and index <= 1
        #assert 0 <= angle and angle <= self.max_angle
        self.servokit.servo[index].angle = angle


if __name__ == '__main__':
    import time
    srv = Servo()
    for i in range(0, 180, 15):
        srv.angle(0, i)
        time.sleep(1)
    time.sleep(1)
    srv.angle(0, 180)
    time.sleep(1)