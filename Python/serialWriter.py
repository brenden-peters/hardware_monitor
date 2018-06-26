import serial
import sys
import os
import time
import struct
import serial.tools.list_ports

print ("\n\n\n")
global serName
serName = None

usbKeyword = 'usb'
usbIndex = 0

if (os.name == 'nt'):  ## Corrects behavior around Windows' quirks regarding COM port info and naming
    usbKeyword = 'USB'
    usbIndex = 1
    
portsList = list(serial.tools.list_ports.comports())
for detectedPort in portsList:
    if (usbKeyword in detectedPort[usbIndex]):
        print "We got one!"
        serName = detectedPort[0]

if (serName == None):
    print("No Arduino device detected. Closing program.")
    time.sleep(1)
    exit(1)
    
global ser
ser = serial.Serial(serName, 115200, timeout = 1)
#ser = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=1)
print ("Connection established!\n",)
time.sleep(1)
while(True):
    ##ser.write("Hello there from Python.\n")
    ser.write("Hello: hi,line 02 calling,third entry yes!,Last line :0) {}")
    time.sleep(2)
