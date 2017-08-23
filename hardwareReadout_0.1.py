#!/usr/bin/python3
# -*- coding: utf-8 -*-

## Adapted from http://zetcode.com/gui/pyqt5/firstprograms/ ##

import sys
import psutil as pea
from time import sleep
from PyQt5.QtWidgets import (QApplication, QToolTip, 
    QPushButton, QApplication, QMessageBox, QDesktopWidget, 
    QMainWindow, QAction, qApp, QWidget, QHBoxLayout, 
    QVBoxLayout, QLabel)
from PyQt5.QtGui import (QFont, QColor, QPainter)#, QIcon)
from PyQt5.QtCore import (QCoreApplication, Qt, QThread, pyqtSignal)

progName = 'Otterlot\'s Hardware Readout v0.1'
windowScale = 0.125 ## Ratio of application window to screen size; 
                   ## half the width and half the height = one quarter overall size                   
                   
procCount = pea.cpu_count()    
mem = pea.virtual_memory()    
parts = pea.disk_partitions()
allTexts = {}
x = True
                   

class mainFrame(QWidget):
    
    curInfo = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.curInfo.connect(self.setText)
        self.initUI()
        
    def initUI(self):
        global allTexts
        
        QToolTip.setFont(QFont('SansSerif', 10))
        #self.setMouseTracking(True)
        #self.setToolTip('Ceci n\'est pas un fenêtre.')
        
        #okBtn = QPushButton("OK")
        #cancelBtn = QPushButton("Cancel")
        #self.text = "(x,y): ({0},{1})".format(x, y)
        
        #textLayout = QHBoxLayout()
        #textLayout.setSpacing(10)
        #textLayout.addStretch(1)
        #textLayout.addWidget(self.label, 0, Qt.AlignTop)
        
        #procLayout = QVBoxLayout()
        allTexts['Processor'] = ""
        allTexts['Memory'] = ""
        
        #procText = QText('procInfo')
        #allTexts['Processor'] = QLabel(procText, procLayout)
        #procLayout.addWidget(allTexts['Processor'], 0, Qt.AlignTop)
        
        self.text = allTexts['Processor']
        self.text += allTexts['Memory']
        #self.label = QLabel(self.text, self)
        #buttonLayout = QHBoxLayout()
        #buttonLayout.addStretch(1)
        #buttonLayout.addWidget(okBtn)
        #buttonLayout.addWidget(cancelBtn)
        
        mainLayout = QVBoxLayout()
        #mainLayout.addWidget(self.label, 0, Qt.AlignTop)
        mainLayout.addStretch(1)
        #mainLayout.addLayout(textLayout)
        #mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)
        
        #quitBtn = QPushButton('Exit', self)
        #quitBtn.clicked.connect(QCoreApplication.instance().quit)
        #quitBtn.setToolTip('Click here to close application.')
        #quitBtn.resize(quitBtn.sizeHint())
        #quitBtn.move(150, 50)
        
        self.show() 
              
    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        
        #self.text = "(x,y): ({0},{1})".format(x, y) 
        #self.looper()
        #self.update()
        
    def setText(self, ourText):
        self.text = ourText
        self.update()
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp, self.text)
        qp.end()
        
    def drawText(self, event, qp, ourText):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('SansSerif', 15))
        qp.drawText(event.rect(), Qt.AlignTop, ourText)#self.text)

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
        self.infoThread = infoGetter()
        self.infoThread.start()
        
    def sizeCenter(self):
        defaultMonitor = QDesktopWidget().screenGeometry(-1)
        #print("Default monitor coordinates: {0}\n".format(defaultMonitor))
        screenHi = defaultMonitor.height()
        screenWid = defaultMonitor.width()
        winWid = screenWid * (windowScale * 2)
        winHi = screenHi * (windowScale * 2)
        self.setGeometry((screenWid * 0.5) - (winWid * 0.5), (screenHi * 0.5) - (winHi * 0.5), winWid, winHi)
        
    def jeQuitte(self):
        global x
        #x = False
        print("jeQuitte checking in!\n")
        #self.infoThread.stop()
        self.infoThread.exit(0)
        #self.infoThread.quit()
        #self.infoThread.wait()
        
    def closeEvent(self, event):
        self.jeQuitte()
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
    
    def __init__(self):
        QThread.__init__(self)
        #super().__init__(self)
        self.signal = pyqtSignal("curInfo")
        
    def __del__(self):
        self.wait()
    
    def stop(self):
        self._isRunning = False
        
    def run(self):
        #self.exec_()  <- try again after implementing signaling
        global allTexts
        global mem
        global procCount
        global x
        while(x):
            procUse = pea.cpu_percent(0.75, True)
            diskUse = pea.disk_usage('/') #forEach partition get use
            
            totalMem = mem.total/(1024*1024) # in MB
            freeMem = mem.free/(1024*1024)
        
            allTexts['Processor'] = ""
            allTexts['Processor'] += "Processor cores: {0}\n".format(procCount)
            for x in range(procCount):
                allTexts['Processor'] += "    Core {0}: {1}%\n".format(x, procUse[x])
            allTexts['Memory'] = ""
            allTexts['Memory'] += "Installed RAM: {0:,.0f} MB".format(totalMem)
        
            #oow.mainerFramer.text = allTexts['Processor']
            #oow.mainerFramer.text += allTexts['Memory']
            #oow.mainerFramer.update()
            ### Replace the above three lines with assignment to single string, then send string as signal to oow
            
            curInfText = allTexts['Processor']
            curInfText += allTexts['Memory']
            #self.emit(SIGNAL("curInfo"), curInfText)
            self.emit(self.signal, curInfText)
            #sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    oow = ooWin()
    sys.exit(app.exec_())
    