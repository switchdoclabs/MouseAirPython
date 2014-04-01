#!/usr/bin/python

import sys
import time
import RPi.GPIO as GPIO
import utils

from raspirobotboard import *

sys.path.append('./Adafruit-Raspberry-Pi-Python-Code/Adafruit_LEDBackpack')
sys.path.append('./Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver')
sys.path.append('./pclogging')

import pclogging

from Adafruit_LEDBackpack import LEDBackpack
from Adafruit_8x8 import ColorEightByEight
from Adafruit_PWM_Servo_Driver import PWM

SERVO_LOAD = 0
SERVO_CHAMBER = 1

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

GPIO.setmode(GPIO.BCM)

RIGHT_MOTOR = 29
LEFT_MOTOR = 31
RIGHT_ON = 0
RIGHT_OFF = 1
LEFT_ON = 1
LEFT_OFF = 0

SOLENOID_LEFT = 28
SOLENOID_RIGHT = 30
SOLENOID_ON_TIME = 0.1

GPIO.setup(RIGHT_MOTOR, GPIO.OUT)
GPIO.setup(LEFT_MOTOR, GPIO.OUT)
GPIO.output(RIGHT_MOTOR, RIGHT_OFF)
GPIO.output(LEFT_MOTOR, LEFT_OFF)

#GPIO.output(RIGHT_MOTOR, RIGHT_ON)
#GPIO.output(LEFT_MOTOR, LEFT_ON)


GPIO.setup(SOLENOID_LEFT, GPIO.OUT)
GPIO.setup(SOLENOID_RIGHT, GPIO.OUT)
GPIO.output(SOLENOID_LEFT, 0)
GPIO.output(SOLENOID_RIGHT, 0)

rr = RaspiRobot()
# get range finder working
lastrange = rr.get_range_inch()
print ("rangeinch=%f" % rr.get_range_inch())

# set up Servos

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
# initialise the PWM device using the default address
pwm = PWM(0x50, debug=True)
pwm.setPWMFreq(60)



# Blink rate
__HT16K33_BLINKRATE_OFF                 = 0x00
__HT16K33_BLINKRATE_2HZ                 = 0x01
__HT16K33_BLINKRATE_1HZ                 = 0x02
__HT16K33_BLINKRATE_HALFHZ              = 0x03

#Colors

__HT16K33_OFF		= 0
__HT16K33_GREEN		= 1
__HT16K33_RED		= 2
__HT16K33_YELLOW	= 3

# setup backpack
grid = ColorEightByEight(address=0x72)
backpack = LEDBackpack(address=0x72)


def fireMouse():
	pclogging.log(pclogging.INFO, __name__, "Mouse Launched!")
	time.sleep(1.0)
	grid.clear()




	# Step 1 - Drop Mouse into Chamber	
	
  	# Change speed of continuous servo on channel SERVO_CHAMBER
	print("Step 1 - Chamber Mouse")
  	pwm.setPWM(SERVO_CHAMBER, 0, servoMin)
  	time.sleep(1)
  	pwm.setPWM(SERVO_CHAMBER, 0, servoMax)
  	time.sleep(1)
	utils.writeRow(grid,0,__HT16K33_RED)


	# Step 3 - Drop Mouse into Position


  	# Change speed of continuous servo on channel SERVO_LOAD
	print("Step 2 - Load Mouse")
  	pwm.setPWM(SERVO_LOAD, 0, servoMin)
  	time.sleep(1)
  	pwm.setPWM(SERVO_LOAD, 0, servoMax)
  	time.sleep(1)

	utils.writeRow(grid,1,__HT16K33_RED)

	# Step 3 - Start Motors
	print("Step 3 - Motors Starting")
	GPIO.output(RIGHT_MOTOR, RIGHT_ON)
	time.sleep(0.5)
	GPIO.output(LEFT_MOTOR, LEFT_ON)

	utils.writeRow(grid,2,__HT16K33_RED)

	#

	# Step 4 - Launch Mouse 
	# now move solenoid out (launch mouse!)
	print("Step 4 - Mouse launched")
	time.sleep(1.0)
	GPIO.output(SOLENOID_LEFT, 0)
	GPIO.output(SOLENOID_RIGHT, 1)
	time.sleep(SOLENOID_ON_TIME)
	GPIO.output(SOLENOID_LEFT, 0)
	GPIO.output(SOLENOID_RIGHT, 0)
	utils.writeRow(grid,3,__HT16K33_RED)
	backpack.setBlinkRate(__HT16K33_BLINKRATE_2HZ)
	
	# Step 5 - Stop Motors
	print("Step 5 - Motors Stopping")
	GPIO.output(RIGHT_MOTOR, RIGHT_OFF)
	GPIO.output(LEFT_MOTOR, LEFT_OFF)

	time.sleep(2.0)
	backpack.setBlinkRate(__HT16K33_BLINKRATE_OFF)
	utils.writeRow(grid,4,__HT16K33_RED)

	time.sleep(1.0)

	# Step 6 - now move solenoid out (pull back)
	print("Step 6- Rearmed")	

	utils.writeRow(grid,5,__HT16K33_RED)
	GPIO.output(SOLENOID_LEFT, 1)
	GPIO.output(SOLENOID_RIGHT, 0)
	time.sleep(SOLENOID_ON_TIME)
	GPIO.output(SOLENOID_LEFT, 0)
	GPIO.output(SOLENOID_RIGHT, 0)

	grid.clear()

# main loop
pclogging.log(pclogging.INFO, __name__, "Mouse Air Startup")

#myIP = util.track_ip()
#utils.sendEmail("test", "Mouse Air Pi Startup\n" + str(myIP), "The Raspberry Pi has rebooted.", conf.notifyAddress,  conf.fromAddress, "");



while True:

	lastrange = rr.get_range_inch()
	time.sleep(1.0)
	lastrange = rr.get_range_inch()
	if(lastrange < 1.5):
		lastrange = 8

	print ("checking for ultrasonic rangeinch=%f" % lastrange)
	utils.writeRow(grid,7,__HT16K33_GREEN)
	

	if (lastrange < 7):
		utils.writeRow(grid,7,__HT16K33_RED)
		utils.takePicture("Picture Taken -Ultrasonic Trigger")
		fireMouse()


	time.sleep(1.0)
