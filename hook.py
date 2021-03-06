"""This is used to control a servo to deploy a hook for capturing the duck.

https://www.aranacorp.com/en/using-a-pca9685-module-with-raspberry-pi/

pip install adafruit-circuitpython-servokit

sudo raspi-config

"3) interface options" -> "I5 I2C Enable/disable automatic loading of I2C kernel module"  -> "Yes"


"""
import time

from adafruit_servokit import ServoKit

class RoboArm:
    def __init__(self, max_angle=180):
        servos_indices = [0, 2]  # only use one servo
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


def test():
    srv = RoboArm()
    #for i in range(0, 180, 15):
    while True:
        srv.angle(0, 0)
        srv.angle(2, 0)
        time.sleep(1)
        srv.angle(0, 180)
        srv.angle(2, 180)
        time.sleep(1)
        srv.angle(0, 0)
        srv.angle(2, 0)

if __name__ == '__main__':
    test()
