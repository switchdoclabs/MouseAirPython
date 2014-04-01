
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
	cameracommand = "raspistill -o /home/pi/RasPiConnectServer/static/picameraraw.jpg -rot 180 -t 750 -ex " + exposuremode
	print cameracommand
	output = subprocess.check_output (cameracommand,shell=True, stderr=subprocess.STDOUT )
	output = subprocess.check_output("convert '/home/pi/RasPiConnectServer/static/picameraraw.jpg' -pointsize 72 -fill white -gravity SouthWest -annotate +50+100 'Mouse Air %[exif:DateTimeOriginal]' '/home/pi/RasPiConnectServer/static/picamera.jpg'", shell=True, stderr=subprocess.STDOUT)

	pclogging.log(pclogging.INFO, __name__, source )

	print "finished taking picture"
	return



