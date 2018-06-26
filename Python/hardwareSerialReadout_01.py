import serial
import sys
import os
import time
import struct
import serial.tools.list_ports

import sys
import psutil as pea
from time import sleep, time

gib = 1073741824    ## Divide a # of bytes by this to get the # of gibibytes
gb = 1000000000     ## Divide a # of bytes by  this to get the # of gigabytes
mib = 1048576
mb = 1000000
kib = 1024
storMult = gb       ## Display storage info in units of mibibytes, megabytes, gigabytes, etc.


### FIXME: fix this thing 
## TODO: do this thing 
# CHANGED: Commenting style has adapted to include TextMate's to-do bundle; chord ctrl-shft-t for colated list

procCount = pea.cpu_count(logical=False)                   
threadCount = pea.cpu_count(logical=True)    
mem = pea.virtual_memory()    
parts = pea.disk_partitions(all = False)
allTexts = {}
oldDiskSpeed = {'Read':0, 'Write':0, 'time':0}
printerText = ''


######## BEGIN ########

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
    sleep(1)
    exit(1)
    
global ser
ser = serial.Serial(serName, 115200, timeout = 1)
#ser = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=1)
print ("Connection established!\n",)
sleep(1)

######### BEGIN HARDWARE

while(True):
    #ser.write("Hello there from Python.\n")
    #time.sleep(2)
    
    mem = pea.virtual_memory() ## We update every loop to refresh RAM readings
    procUse = pea.cpu_percent(0.75, True)
    diskUse = pea.disk_usage('/') #forEach partition get use
    
    totalMem = mem.total/(1024*1024) # in MB
    freeMem = mem.free/(1024*1024)
    usedMem = totalMem - freeMem
    
    allTexts['Processor'] = ""
    allTexts['Processor'] += "Physical CPU cores: {0}\n".format(procCount)
    for x in range(threadCount):
        allTexts['Processor'] += "    Logical Core {0}: {1}%\n".format(x, procUse[x])
    allTexts['Memory'] = ""
    #allTexts['Memory'] += "Installed RAM: {0:,.0f} MB".format(totalMem)
    allTexts['Memory'] += "RAM: \n    {0:.0f} MB free of total {1:.0f} MB\n".format(freeMem, totalMem)
    
    allTexts['Disk'] = ""
    #allTexts['Disk'] += "Disc ish stuff\n"
    #allTexts['Disk'] += "Disk:\n    Total disk space: {0}\n    Used: {1}\n".format((diskUse[0] / storMult), (diskUse[1] / storMult))
    
    #for x in diskUse:
    #    cap = (x / )
    #    allTexts['Disk'] += "{0}\n".format(cap)
    diskAccess = pea.disk_io_counters()
    
    totRead = 0
    totWrite = 0
    totTime = 0
    totRead += (diskAccess.read_bytes / 1000000)   ## Convert bytes to MB
    totWrite += (diskAccess.write_bytes / 1000000)
    totTime = time()
    
    dRead = (totRead - oldDiskSpeed['Read'])
    dWrite = (totWrite - oldDiskSpeed['Write'])
    dTime = (totTime - oldDiskSpeed['time'])    ## Change of time in seconds
    
    readRate = (dRead / dTime)
    writeRate = (dWrite / dTime)
    oldDiskSpeed['Read'] = totRead
    oldDiskSpeed['Write'] = totWrite
    oldDiskSpeed['time'] = totTime
    
    allTexts['Disk'] += "Disks:\n    Current Read Speed: {0:.2f} MB/s\n    Current Write Speed: {1:.2f} MB/s\n".format(readRate, writeRate)
    
    ## get old/new delta for read, write, divide by time, present for moment to moment xfer speeds
    ## also fill in the print based on template below
    
    diskTemplate = "{}"
    #print(diskTemplate.format("Device", "Mount", "Total", "Used", "Free", "Filesystem"))
    
#CP1 16% CP2  3%,CP3 10% CP4  5%,Free RAM: 194,Used RAM: 7998,Disk Rd: 0.00 MB/s,Disk Wr: 0.00 MB/sZ\    
    ## compare current read/write to old read/write, look at time delta
    
    curInfText = allTexts['Processor']
    curInfText += allTexts['Memory']
    curInfText += allTexts['Disk']
    #curInfText += str(parts)
    print(curInfText)

    #print("CP1 {0:2.0f}% CP2 {1:2.0f}%,CP3 {2:2.0f}% CP4 {3:2.0f}%,Free RAM: {4},Used RAM: {5},Disk Rd: {6:3.2f} MB/s,Disk Wr: {7:3.2f} MB/s".format(procUse[0], procUse[1], procUse[2], procUse[3], freeMem, usedMem, readRate, writeRate))
    ser.write("CP1 {0:2.0f}% CP2 {1:2.0f}%,CP3 {2:2.0f}% CP4 {3:2.0f}%,Free RAM: {4},Used RAM: {5},Disk Rd: {6:3.2f},Disk Wr: {7:3.2f}Z".format(procUse[0], procUse[1], procUse[2], procUse[3], freeMem, usedMem, readRate, writeRate))
    #Disk Read: {6} MB/s,Disk Write: {7} MB/s".format(procUse[0], procUse[1], procUse[2], procUse[3], freeMem, usedMem, readRate, writeRate))
    #sleep(2)
    