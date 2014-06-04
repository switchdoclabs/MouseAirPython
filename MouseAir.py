#!/usr/bin/python

import sys
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

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


import servo as servo

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


# initialise the PWM device using the default address
pwm = PWM(0x50, debug=True)
pwm.setPWMFreq(60)

servo.initServo(pwm)



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

# command from RasPiConnect Execution Code

def completeCommand():

        f = open("/home/pi/MouseAir/state/MouseCommand.txt", "w")
        f.write("DONE")
        f.close()

def processCommand():

        f = open("/home/pi/MouseAir/state/MouseCommand.txt", "r")
        command = f.read()
        f.close()

	if (command == "") or (command == "DONE"):
		# Nothing to do
		return False

	# Check for our commands
	pclogging.log(pclogging.INFO, __name__, "Command %s Recieved" % command)

	print "Processing Command: ", command
	if (command == "FIREMOUSE"):
		fireMouse()
		completeCommand()
		return True
			
	if (command == "TAKEPICTURE"):
		utils.threadTakePicture("Picture Taken -RasPiConnect Command")
		completeCommand()
		return True

	if (command == "SHOOTSOLENOID"):
		GPIO.output(SOLENOID_LEFT, 0)
		GPIO.output(SOLENOID_RIGHT, 1)
		time.sleep(SOLENOID_ON_TIME)
		GPIO.output(SOLENOID_LEFT, 0)
		GPIO.output(SOLENOID_RIGHT, 0)

		completeCommand()
		return True

	if (command == "PANTOMOUSE"):
		servo.setServo(pwm, servo.SERVO_TILT, 430)	
		servo.setServo(pwm, servo.SERVO_PAN, 450)	
		
		completeCommand()
		return True

	if (command == "PANTOCAT"):
		servo.setServo(pwm, servo.SERVO_TILT, 340)	
		servo.setServo(pwm, servo.SERVO_PAN, 300)	
		
		completeCommand()
		return True

	if (command == "PANLEFT"):
		servo.servoIncrement(pwm, servo.SERVO_PAN, 10)	
		completeCommand()
		return True
			
	if (command == "PANRIGHT"):
		servo.servoIncrement(pwm, servo.SERVO_PAN, -10)	
		completeCommand()
		return True
			
	if (command == "TILTUP"):
		servo.servoIncrement(pwm, servo.SERVO_TILT, 10)	
		completeCommand()
		return True
			
	if (command == "TILTDOWN"):
		servo.servoIncrement(pwm, servo.SERVO_TILT, -10)	
		completeCommand()
		return True
			
	if (command == "TOPSERVOOPEN"):
		pwm.setPWM(servo.SERVO_CHAMBER, 0, servo.servoMin)
		completeCommand()
		return True
			
	if (command == "TOPSERVOCLOSE"):
		pwm.setPWM(servo.SERVO_CHAMBER, 0, servo.servoMax)
		completeCommand()
		return True
			

	if (command == "BOTTOMSERVOOPEN"):
		pwm.setPWM(servo.SERVO_LOAD, 0, servo.servoMin)
		completeCommand()
		return True
			
	if (command == "BOTTOMSERVOCLOSE"):
		pwm.setPWM(servo.SERVO_LOAD, 0, servo.servoMax)
		completeCommand()
		return True
			

	if (command == "MOTORSON"):
		GPIO.output(RIGHT_MOTOR, RIGHT_ON)
		time.sleep(0.5)
		GPIO.output(LEFT_MOTOR, LEFT_ON)

		completeCommand()
		return True

	if (command == "MOTORSOFF"):
		GPIO.output(RIGHT_MOTOR, RIGHT_OFF)
		GPIO.output(LEFT_MOTOR, LEFT_OFF)

		completeCommand()
		return True

	if (command == "ULTRASONICON"):
		utils.writeState(True, ultrasonicsRange, RFIDUse, useCameraMotion, fireMouseNow)
		completeCommand()
		return True
			
	if (command == "ULTRASONICOFF"):
		utils.writeState(False, ultrasonicsRange, RFIDUse, useCameraMotion, fireMouseNow)
		completeCommand()
		return True
			
	if (command == "RFIDON"):
		utils.writeState(ultrasonicsUse, ultrasonicsRange, True, useCameraMotion, fireMouseNow)
		completeCommand()
		return True
			
	if (command == "RFIDOFF"):
		utils.writeState(ultrasonicsUse, ultrasonicsRange, False, useCameraMotion, fireMouseNow)
		completeCommand()
		return True
			
			
	if (command == "CAMERAMOTIONON"):
		utils.writeState(ultrasonicsUse, ultrasonicsRange, RFIDUse, True, fireMouseNow)
		completeCommand()
		return True
			
	if (command == "CAMERAMOTIONOFF"):
		utils.writeState(ultrasonicsUse, ultrasonicsRange, RFIDUse, False, fireMouseNow)
		completeCommand()
		return True
			
			
	completeCommand()


	return False

def fireMouse():
	pclogging.log(pclogging.INFO, __name__, "Mouse Launched!")
	time.sleep(1.0)
	grid.clear()




	# Step 1 - Drop Mouse into Chamber	
	
  	# Change speed of continuous servo on channel SERVO_CHAMBER
	print("Step 1 - Chamber Mouse")
	pwm.setPWM(servo.SERVO_CHAMBER, 0, servo.servoMin)
	time.sleep(1)
	pwm.setPWM(servo.SERVO_CHAMBER, 0, servo.servoMax)
	time.sleep(1)
	pwm.setPWM(servo.SERVO_CHAMBER, 0, servo.servoMin)
	time.sleep(1)
	pwm.setPWM(servo.SERVO_CHAMBER, 0, servo.servoMax)
	time.sleep(1)
	utils.writeRow(grid,0,__HT16K33_RED)


	# Step 3 - Drop Mouse into Position


  	# Change speed of continuous servo on channel SERVO_LOAD
	print("Step 2 - Load Mouse")
	pwm.setPWM(servo.SERVO_LOAD, 0, servo.servoMin)
	time.sleep(1)
	pwm.setPWM(servo.SERVO_LOAD, 0, servo.servoMax)
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

	utils.writeRow(grid,6,__HT16K33_YELLOW)
	utils.writeRow(grid,7,__HT16K33_YELLOW)
	utils.writeRow(grid,6,__HT16K33_GREEN)
	utils.writeRow(grid,7,__HT16K33_GREEN)
	
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
print("Mouse Air Version 1.3")
pclogging.log(pclogging.INFO, __name__, "Mouse Air 1.3 Startup")

#myIP = util.track_ip()
#utils.sendEmail("test", "Mouse Air Pi Startup\n" + str(myIP), "The Raspberry Pi has rebooted.", conf.notifyAddress,  conf.fromAddress, "");

detection.initUltrasonic()
# start RFID reading

detection.initRFID()

# set up a communication queue
queueRFID = Queue()
RFIDThread = Thread(target=detection.RFIDDetect, args=(__name__,0,queueRFID,))
RFIDThread.daemon = True
RFIDThread.start()

#set state variables

ultrasonicsUse = False
ultrasonicsRange = 20
RFIDUse = False
useCameraMotion = False
fireMouseNow = False

# the main loop

while True:

	new_list = utils.readState(ultrasonicsUse, ultrasonicsRange, RFIDUse, useCameraMotion, fireMouseNow)
	ultrasonicsUse = new_list[0]
	ultrasonicsRange = new_list[1]
	RFIDUse = new_list[2]
	useCameraMotion = new_list[3]
	fireMouseNow = new_list[4]

	#print(new_list)
	fireMouseNow = False	# we don't use this state anymore

	# process commands from RasPiConnect

	processCommand()	

	inRange = detection.ultrasonicDetect(7, 0)
	if (ultrasonicsUse == True):

		if (inRange == True) :
			utils.writeRow(grid,7,__HT16K33_RED)
			utils.threadTakePicture("Picture Taken -Ultrasonic Trigger")
			fireMouse()

		else:	
			utils.writeRow(grid,7,__HT16K33_GREEN)


	# write out to the ultasonics file

	#	print ("detectlist=", detection.datalist)
	response = ""
	valuecount = ""
        f = open("/home/pi/MouseAir/state/UltrasonicGraph.txt", "w")
	for i in range(len(detection.datalist)):
	 	response += str(detection.datalist[i])
		valuecount += str(i)
		if (i < len(detection.datalist)-1):
			response +="^^"
			valuecount +="^^"
		
	if (len(response) != 0):
		fullresponse = response + "||" + valuecount	
	else:
		fullresponse = ""

        f.write(fullresponse)
        f.close()

	# check to see if RFID is in queue (thus a detection happened)  	

	if (RFIDUse == True):
		try:
			print("Queue depth = ", queueRFID.qsize())
			if (queueRFID.get(False)):
				utils.writeRow(grid,6,__HT16K33_RED)
				utils.threadTakePicture("Picture Taken -RFID Trigger")
				# clear queue

				try:
					while True:
						queueRFID.get(False)
				except:	
					fireMouse()
					#print ("Fire MOUSE")

		

		except:	
			utils.writeRow(grid,6,__HT16K33_GREEN)

	

	time.sleep(0.1)
