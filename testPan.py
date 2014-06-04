
import sys
import time
import RPi.GPIO as GPIO
import utils
from threading import Thread
from Queue import Queue

from raspirobotboard import *

sys.path.append('./Adafruit-Raspberry-Pi-Python-Code/Adafruit_LEDBackpack')
sys.path.append('./Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver')
sys.path.append('./pclogging')
sys.path.append('./detect')

import pclogging
import detection


from Adafruit_LEDBackpack import LEDBackpack
from Adafruit_8x8 import ColorEightByEight
from Adafruit_PWM_Servo_Driver import PWM


SERVO_PAN = 3
SERVO_TILT = 2

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print( "%d us per period" % pulseLength)
  pulseLength /= 4096                     # 12 bits of resolution
  print( "%d us per bit" % pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)


# set up Servos

servoMin = 150  # Min pulse length out of 4096
servoMax = 630  # Max pulse length out of 4096
# initialise the PWM device using the default address
pwm = PWM(0x50, debug=True)
pwm.setPWMFreq(60)


i = servoMin
increment = 10
while True:
	#time.sleep(1)
	#pwm.setPWM(SERVO_TILT, 0, (servoMax + servoMin)/2 )
	#time.sleep(1)
	#pwm.setPWM(SERVO_PAN, 0, (servoMax +servoMin)/2)
	
	pwm.setPWM(SERVO_PAN, 0, i)
	time.sleep(0.5)
	i = i + increment
	print "servo set to: ", i

	if (i > servoMax):
		increment = -10
	if (i < servoMin):
		increment = 10

		
	#pwm.setPWM(SERVO_PAN, 0, servoMin)
	#time.sleep(1)
	#pwm.setPWM(SERVO_PAN, 0, servoMax)
	#time.sleep(1)

	#pwm.setPWM(SERVO_TILT, 0, servoMin)
	#time.sleep(1)
	#pwm.setPWM(SERVO_TILT, 0, servoMax)
	#time.sleep(1)


