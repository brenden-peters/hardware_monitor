#!/usr/bin/python3
# -*- coding: utf-8 -*-

## Adapted from http://zetcode.com/gui/pyqt5/firstprograms/ ##

import sys
import socket
import psutil as pea
from time import sleep, time
from PyQt5.QtWidgets import (QApplication, QToolTip, 
    QPushButton, QApplication, QMessageBox, QDesktopWidget, 
    QMainWindow, QAction, qApp, QWidget, QHBoxLayout, 
    QVBoxLayout, QLabel)
from PyQt5.QtGui import (QFont, QColor, QPainter)#, QIcon)
from PyQt5.QtCore import (QCoreApplication, Qt, QThread, pyqtSignal, pyqtSlot, QTimer)

progName = 'Otterlot\'s Hardware Readout v0.3'
font = 'SansSerif'  ## GUI font
ptSize = 15         ## GUI font size
updateRate = 750    ## GUI base refresh rate in ms (some functions may update between clocked refreshes)
windowScale = 0.125 ## Ratio of application window to screen size; 
                    ##   half the width and half the height = one quarter overall size   

## PREFIXES                
giB = ("GiB", "gibi", 1073741824)    ## Divide a # of bytes by this to get the # of gibibytes
gB = ("GB", "giga", 1000000000)     ## Divide a # of bytes by this to get the # of gigabytes
miB = ("MiB", "mibi", 1048576)
mB = ("MB", "mega", 1000000)
kiB = ("kiB", "kibi", 1024)
kB = ("kB", "kilo", 1000)
noPrefix = ("B", "", 1)

storMult = gB       ## Display storage info in units of mibibytes, megabytes, gigabytes, etc.
netMult =  kB      ## Display network info in units of ... etc. 


### FIXME: fix this thing 
## TODO: do this thing 
# CHANGED: Commenting style has adapted to include TextMate's to-do bundle; chord ctrl-shft-t for colated list

procCount = pea.cpu_count(logical=False)                   
threadCount = pea.cpu_count(logical=True)    
mem = pea.virtual_memory()    
parts = pea.disk_partitions(all = False)
allTexts = {}
oldDiskSpeed = {'Read':0, 'Write':0, 'time':0}
oldNetworkRates = {}
printerText = ''
                   

class mainFrame(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(updateRate)
        
    def initUI(self):
        global allTexts
        
        QToolTip.setFont(QFont('SansSerif', 10))
        allTexts['Processor'] = ""
        allTexts['Memory'] = ""
        allTexts['Disk'] = ""
        allTexts['Networks'] = ""
        
        mainLayout = QVBoxLayout()
        mainLayout.addStretch(1)
        
        self.setLayout(mainLayout)
        
        #quitBtn = QPushButton('Exit', self)
        #quitBtn.clicked.connect(QCoreApplication.instance().quit)
        #quitBtn.setToolTip('Click here to close application.')
        #quitBtn.resize(quitBtn.sizeHint())
        #quitBtn.move(150, 50)
        
        self.infoThread = infoGetter()
        self.infoThread.start()
        
        self.show() 
        
      
    #@staticmethod  
    @pyqtSlot(str)    
    def setText(ourText):
        #self.text = ourText
        global printerText
        printerText = ourText
        #mainFrame.update()
        #mainFrame.update()
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp, printerText)
        qp.end()
        
    def drawText(self, event, qp, ourText):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont(font, ptSize))
        qp.drawText(event.rect(), Qt.AlignTop, ourText)

class ooWin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        global mainF
        QToolTip.setFont(QFont('SansSerif', 10))
        #self.setToolTip('Close window or click <i>Exit</i> to close application.')
        self.statusBar().showMessage(progName)
        self.mainerFramer = mainFrame()
        self.setCentralWidget(self.mainerFramer)
        
        ##exitAct = QAction(QIcon('exit.png'),'&Close Application', self)
        #exitAct = QAction('&Close Application', self)
        #exitAct.setShortcut('Ctrl+Q')
        #exitAct.setStatusTip('Exit application')
        #exitAct.triggered.connect(qApp.quit)
        
        #self.statusBar()
        
        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('&File')
        #fileMenu.addAction(exitAct)
        
        self.setWindowTitle(progName)
        self.sizeCenter()
        self.show()
        #self.infoThread = infoGetter()
        #self.infoThread.start()
        
    def sizeCenter(self):
        defaultMonitor = QDesktopWidget().screenGeometry(-1)
        #print("Default monitor coordinates: {0}\n".format(defaultMonitor))
        screenHi = defaultMonitor.height()
        screenWid = defaultMonitor.width()
        winWid = screenWid * (windowScale * 2)
        winHi = screenHi * (windowScale * 2)
        self.setGeometry((screenWid // 2) - (winWid // 2), (screenHi // 2) - (winHi // 2), winWid, winHi)
        
    def closeEvent(self, event):
        event.accept()    
        
    #def closeEvent(self, event):
        #reply = QMessageBox.question(self, 'Title bar text here',
        #    "Are you sure you wish to quit?", QMessageBox.Yes | QMessageBox.No,
        #    QMessageBox.No)
        #    
        #if reply == QMessageBox.Yes:
        #    event.accept()
        #else:
        #    event.ignore()
        
class infoGetter(QThread):
    
    curInfo = pyqtSignal(str)
    
    def __init__(self):
        QThread.__init__(self)
        #super()
        self.curInfo.connect(mainFrame.setText)
        
    def __del__(self):
        self.wait()
    
    def stop(self):
        self._isRunning = False
        
    def run(self):
        #self.exec_()  <- try again after implementing signaling
        global allTexts
        global mem
        global procCount
        global threadCount
        global parts
        global netInterfaces
        while(True):
            mem = pea.virtual_memory() ## We update every loop to refresh RAM readings
            #procUpdateRate = (updateRate / 1000) # locks processor updates to GUI refresh rate
            #procUse = pea.cpu_percent(procUpdateRate, True)
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
            
            allTexts['Disk'] += "Disks:\n    Current Read Speed: {0:.2f} MB/s\n    Current Write Speed: {1:.2f}MB/s\n".format(readRate, writeRate)
            
            ## get old/new delta for read, write, divide by time, present for moment to moment xfer speeds
            ## also fill in the print based on template below
            
            diskTemplate = "{}"
            #print(diskTemplate.format("Device", "Mount", "Total", "Used", "Free", "Filesystem"))
            
            
            ## compare current read/write to old read/write, look at time delta
            
            ## Network 
            ## TODO: let's break out each hardware piece into its own function
            
            allTexts['Networks'] = "Networks:\n"
            netInterfaces = pea.net_if_addrs()
            netInterfaces = filter(self.filterNetInterfaces, netInterfaces.items())
            networkIO = pea.net_io_counters(pernic=True)#, nowrap=False)
            #pea.net_io_counters.cache_clear()
            
            for net in netInterfaces:
                key = net[0]
                ip4 = "n/a"
                ip6 = "n/a"
                mac = "n/a"
                
                if key not in oldNetworkRates.keys():
                    oldNetworkRates[key] = {"rx":0, "tx":0,"time":0}
                
                curTime = time()
                curRx = networkIO[key].bytes_recv
                curTx = networkIO[key].bytes_sent
                
                dDataIn = (curRx - oldNetworkRates[key]["rx"])
                dDataOut = (curTx - oldNetworkRates[key]["tx"])
                dTime = (curTime - oldNetworkRates[key]["time"])
                
                dataInRate = ((dDataIn / dTime) / netMult[2])
                dataOutRate = ((dDataOut / dTime) / netMult[2])   
                
                oldNetworkRates[key]["rx"] = curRx
                oldNetworkRates[key]["tx"] = curTx
                oldNetworkRates[key]["time"] = curTime
                
                for addressType in net[1]:
                    if addressType.family == socket.AF_INET:
                        ip4 = addressType.address
                    elif addressType.family == socket.AF_INET6:
                        ip6 = addressType.address
                    elif addressType.family == pea.AF_LINK:
                        mac = addressType.address
                allTexts['Networks'] += "{net}:\n    ipv4: {v4}\n    ipv6: {v6}\n    MAC: {MAC}\n".format(net = key, v4 = ip4, v6 = ip6, MAC = mac)
                allTexts['Networks'] += "    {unit}bytes rec.: {rec}\n    {unit}bytes sent: {sent}\n".format(unit = netMult[1], rec = curRx/netMult[2], sent = curTx/netMult[2])
                allTexts['Networks'] += "    rx: {rec:.1f} {unit}/s\n    tx: {sent:.1f} {unit}/s\n".format(rec = dataInRate, unit = netMult[0], sent = dataOutRate)
            
            
            
            curInfText = allTexts['Processor']
            curInfText += allTexts['Memory']
            curInfText += allTexts['Disk']
            curInfText += allTexts['Networks']
            #curInfText += str(parts)
            #print(curInfText)
            self.curInfo.emit(curInfText)
            #sleep(1)

    def filterNetInterfaces(self, nis):
        key = nis[0]
        netmaskV4 = None
        netmaskV6 = None
        for addressType in nis[1]:
            if addressType.family == socket.AF_INET:
                netmaskV4 = addressType.netmask
            elif addressType.family == socket.AF_INET6:
                netmaskV6 = addressType.netmask
        # check for address family
        if (key[0] != 'e'): #doesn't start with 'e'
            return False
        elif (netmaskV4 == None and netmaskV6 == None): #doesn't have netmask for either ipv4 or ipv6
            return False
        else:
            return True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    oow = ooWin()
    sys.exit(app.exec_())
    
