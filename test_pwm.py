#!/usr/bin/env python

# Import required modules
import time
import RPi.GPIO as GPIO

# set up GPIO pins
A_PIN = 19
B_PIN = 21
PWM_PIN = 18

# Declare the GPIO settings
GPIO.setmode(GPIO.BOARD)


GPIO.setup(A_PIN, GPIO.OUT) # Connected to BIN1
GPIO.setup(B_PIN, GPIO.OUT) # Connected to BIN2
GPIO.setup(PWM_PIN, GPIO.OUT) # Connected to PWMB

pwm = GPIO.PWM(PWM_PIN, 1000)
pwm.start(0)
pwm.ChangeDutyCycle(100)
time.sleep(3)
pwm.stop()
GPIO.cleanup()
