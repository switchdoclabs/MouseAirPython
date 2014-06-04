
from threading import Thread
import sys
import time
import datetime
sys.path.append('./pclogging')
sys.path.append('./Adafruit-Raspberry-Pi-Python-Code/Adafruit_LEDBackpack')

import subprocess
import pclogging
from Adafruit_8x8 import ColorEightByEight


def writeRow(grid,row,color):
    for y in range(0, 8):
      grid.setPixel(row, y, color)
      time.sleep(0.02)

def clearRow(grid,row):

    for y in range(0, 8):
      grid.setPixel(row, y, 0)


# Takes a single picture on System 
# filename: takeSinglePicture.py
# Version 1.0  10/31/13
#
# takes a picture using the camera 
#
#



def  takePicture(source):

        try:
		f = open("/home/pi/MouseAir/state/exposure.txt", "r")
		tempString = f.read()
		f.close()
		lowername = tempString

        except IOError as e:
                 lowername = "auto"

        exposuremode = lowername
	# take picture
	print "taking picture"
	cameracommand = "raspistill -o /home/pi/RasPiConnectServer/static/picameraraw.jpg -t 750 -ex " + exposuremode
	print cameracommand
	output = subprocess.check_output (cameracommand,shell=True, stderr=subprocess.STDOUT )
	print "adding tag to picture"
	output = subprocess.check_output("convert '/home/pi/RasPiConnectServer/static/picameraraw.jpg' -pointsize 72 -fill white -gravity SouthWest -annotate +50+100 'Mouse Air %[exif:DateTimeOriginal]' '/home/pi/RasPiConnectServer/static/picamera.jpg'", shell=True, stderr=subprocess.STDOUT)

	pclogging.log(pclogging.INFO, __name__, source )

	print "Thread ending. finished taking picture"
	return

# thread camera

def threadTakePicture(source):

	
	cameraThread = Thread(target=takePicture, args=(source,))
	cameraThread.daemon = True
	cameraThread.start()	
	print("camera Thread Starting")
	return

def writeState(ultrasonicsUse, ultrasonicsRange, RFIDUse, useCameraMotion, fireMouseNow):


	f = open("/home/pi/MouseAir/state/ultrasonicsUse.txt", "w")

	if (ultrasonicsUse == True):
		f.write("YES")
	else:
		f.write("NO")
	f.close()

	f = open("/home/pi/MouseAir/state/RFIDUse.txt", "w")
	if (RFIDUse == True):
		f.write("YES")
	else:
		f.write("NO")
	f.close()


	f = open("/home/pi/MouseAir/state/useCameraMotion.txt", "w")
	if (useCameraMotion == True):
		f.write("YES")
	else:
		f.write("NO")
	f.close()

	new_list = [ultrasonicsUse, ultrasonicsRange, RFIDUse, useCameraMotion, fireMouseNow]

	return new_list

def readState(ultrasonicsUse, ultrasonicsRange, RFIDUse, useCameraMotion, fireMouseNow):

	
        try:
		f = open("/home/pi/MouseAir/state/fireMouseNow.txt", "r")
		tempString = f.read()
		f.close()
		lowername = tempString

        except IOError as e:
                 lowername = "NO"

	if (lowername == "NO"):
		fireMouseNow = False
	else:
		fireMouseNow = True


	# mouse is one shot
        f = open("/home/pi/MouseAir/state/fireMouseNow.txt", "w")
        f.write("NO")
        f.close()       
 
        try:
		f = open("/home/pi/MouseAir/state/ultrasonicsUse.txt", "r")
		tempString = f.read()
		f.close()
		lowername = tempString

        except IOError as e:
                 lowername = "NO"

	if (lowername == "NO"):
		ultrasonicsUse = False
	else:
		ultrasonicsUse = True


        try:
		f = open("/home/pi/MouseAir/state/ultrasonicsRange.txt", "r")
		tempString = f.read()
		f.close()
		lowername = tempString

        except IOError as e:
                lowername = "8"

	ultrasonicsRange = int(lowername)


        try:
		f = open("/home/pi/MouseAir/state/RFIDUse.txt", "r")
		tempString = f.read()
		f.close()
		lowername = tempString

        except IOError as e:
                 lowername = "NO"

	if (lowername == "NO"):
		RFIDUse = False
	else:
		RFIDUse = True


        try:
		f = open("/home/pi/MouseAir/state/useCameraMotion.txt", "r")
		tempString = f.read()
		f.close()
		lowername = tempString

        except IOError as e:
                 lowername = "NO"

	if (lowername == "NO"):
		useCameraMotion = False
	else:
		useCameraMotion = True

	new_list = [ultrasonicsUse, ultrasonicsRange, RFIDUse, useCameraMotion, fireMouseNow]

	return new_list
