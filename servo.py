#!/usr/bin/python
# routines for controlling servos of Mouse Air
# 04/05/2014 JCS
#
#


import sys
import time
import RPi.GPIO as GPIO
import utils

sys.path.append('./Adafruit-Raspberry-Pi-Python-Code/Adafruit_LEDBackpack')
sys.path.append('./Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver')
sys.path.append('./pclogging')
sys.path.append('./detect')

import pclogging
import detection


from Adafruit_PWM_Servo_Driver import PWM

SERVO_LOAD = 0
SERVO_CHAMBER = 1

SERVO_PAN = 3
SERVO_TILT = 2

# set up Servos

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

panServoMin = 250 
panServoMax = 500
tiltServoMin =  300 
tiltServoMax = 500

def initServo(pwm):
	global tiltServoCurrentValue 
	global panServoCurrentValue 
	tiltServoCurrentValue = 340
	panServoCurrentValue = 300
	setServo(pwm, SERVO_PAN, panServoCurrentValue)
	setServo(pwm, SERVO_TILT, tiltServoCurrentValue)


def servoIncrement(pwm, servoUnit, increment):
	

	servoValue = 350
	if (servoUnit == SERVO_TILT):
        	servoValue = tiltServoCurrentValue + increment
		if (servoValue <  tiltServoMin):
			servoValue = tiltServoMin
		if (servoValue > tiltServoMax):
			servoValue = tiltServoMax
	if (servoUnit == SERVO_PAN):
        	servoValue = panServoCurrentValue + increment
		if (servoValue <  panServoMin):
			servoValue = panServoMin
		if (servoValue > panServoMax):
			servoValue = panServoMax

	setServo(pwm, servoUnit, servoValue)
	return

def setServo(pwm, servoUnit, servoValue):

	global tiltServoCurrentValue 
	global panServoCurrentValue 
	pwm.setPWM(servoUnit, 0, servoValue) 
	if (servoUnit == SERVO_TILT):
		tiltServoCurrentValue = servoValue
		return
	if (servoUnit == SERVO_PAN):
		panServoCurrentValue = servoValue
		return
	
	return
	
def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print( "%d us per period" % pulseLength)
  pulseLength /= 4096                     # 12 bits of resolution
  print( "%d us per bit" % pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)


