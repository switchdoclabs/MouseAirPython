#!/usr/bin/python3
import serial
import time

ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
print("connected to: " + ser.portstr)

ser.open()
time.sleep(1.0)

rcv = ''
while True:
    rcv += ser.readline()
    print("read line")
    print (rcv) 
