import serial
import sys
import time
import struct
import serial.tools.list_ports

print ("\n\n\n")
global serName
serName = None
portsList = list(serial.tools.list_ports.comports())
for detectedPort in portsList:
    if ("usb" in detectedPort[0]):
        print "We got one!"
        serName = detectedPort[0]

if (serName == None):
    print("No Arduino device detected. Closing program.")
    time.sleep(2)
    
global ser
ser = serial.Serial(serName, 115200, timeout = 1)
#ser = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=1)
print ("Connection established!\n",)
time.sleep(1)
while(True):
    ser.write("Hello there from Python.\n")
    time.sleep(2)
