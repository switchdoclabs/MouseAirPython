#  
# filename: ID3LA_RFID.py 
# Version 1.0 04/01/14
#
# get RFID from device ID-3LA
# meant to run in a thread and report back to main thread
#
#

import sys
import time
import RPi.GPIO as GPIO
import serial

sys.path.append('./pclogging')
import pclogging
import utils


# if conflocal.py is not found, import default conf.py

# Check for user imports
try:
	import conflocal as conf
except ImportError:
	import conf


def  recieveLine(ser):

     timeout = True
     t = 10
                
     st = ''
     initTime = time.time()
     while True:
               st +=  ser.read()
	       if (len(st) > 15):
	       		print("after readline.  st=",st)
			break;
               if timeout and (time.time() - initTime > t) :
                    break


     return st	


def  checkForRFID(source, delay):

	time.sleep(delay)

	# setup serial port to ID-3LA


	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)



	while True:		
		response = recieveLine(ser)
		if (len(response) != 16):
			print("No response=", response)
		else:
			print("Found RFID Card.  response=", response)
			pclogging.log(pclogging.INFO, __name__, "Mouse Air Startup")
	
	



	

