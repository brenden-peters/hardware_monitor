#!/usr/bin/python3
# -*- coding: utf-8 -*-

## Adapted from http://zetcode.com/gui/pyqt5/firstprograms/ ##

import sys
from PyQt5.QtWidgets import (QApplication, QToolTip, 
    QPushButton, QApplication, QMessageBox, QDesktopWidget, 
    QMainWindow, QAction, qApp, QWidget, QHBoxLayout, 
    QVBoxLayout)
from PyQt5.QtGui import (QFont)#, QIcon)
from PyQt5.QtCore import QCoreApplication

windowScale = 0.25 ## Ratio of application window to screen size; 
                   ## half the width and half the height = one quarter overall size

class mainFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Close window or click <i>Exit</i> to close application.')
        #self.statusBar().showMessage('Ready')
        
        okBtn = QPushButton("OK")
        cancelBtn = QPushButton("Cancel")
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okBtn)
        hbox.addWidget(cancelBtn)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        quitBtn = QPushButton('Exit', self)
        quitBtn.clicked.connect(QCoreApplication.instance().quit)
        quitBtn.setToolTip('Click here to close application.')
        quitBtn.resize(quitBtn.sizeHint())
        quitBtn.move(150, 50)
        
        #self.setWindowTitle('Main Frame')
        #self.sizeCenter()
        self.show()    

class ooWin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Close window or click <i>Exit</i> to close application.')
        #self.statusBar().showMessage('Ready')
        
        okBtn = QPushButton("OK")
        cancelBtn = QPushButton("Cancel")
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okBtn)
        hbox.addWidget(cancelBtn)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        quitBtn = QPushButton('Exit', self)
        quitBtn.clicked.connect(QCoreApplication.instance().quit)
        quitBtn.setToolTip('Click here to close application.')
        quitBtn.resize(quitBtn.sizeHint())
        quitBtn.move(150, 50)
        
        #exitAct = QAction(QIcon('exit.png'),'&Close Application', self)
        exitAct = QAction('&Close Application', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        
        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        
        self.setWindowTitle('Test Window 03')
        self.sizeCenter()
        self.show()
        
    def sizeCenter(self):
        defaultMonitor = QDesktopWidget().screenGeometry(-1)
        #print("Default monitor coordinates: {0}\n".format(defaultMonitor))
        screenHi = defaultMonitor.height()
        screenWid = defaultMonitor.width()
        winWid = screenWid * (windowScale * 2)
        winHi = screenHi * (windowScale * 2)
        self.setGeometry((screenWid * 0.5) - (winWid * 0.5), (screenHi * 0.5) - (winHi * 0.5), winWid, winHi)
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Title bar text here',
            "Are you sure you wish to quit?", QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)
            
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    oow = ooWin()
    sys.exit(app.exec_())
    