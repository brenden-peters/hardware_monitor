#!/usr/bin/python3
# -*- coding: utf-8 -*-

## Adapted from http://zetcode.com/gui/pyqt5/firstprograms/ ##

import sys
from PyQt5.QtWidgets import (QApplication, QToolTip, 
    QPushButton, QApplication, QMessageBox, QDesktopWidget, 
    QMainWindow, QAction, qApp, QWidget, QHBoxLayout, 
    QVBoxLayout, QLabel)
from PyQt5.QtGui import (QFont, QColor, QPainter)#, QIcon)
from PyQt5.QtCore import QCoreApplication, Qt

windowScale = 0.25 ## Ratio of application window to screen size; 
                   ## half the width and half the height = one quarter overall size

class mainFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Ceci n\'est pas un fenêtre.')
        
        x = 0
        y = 0
        
        self.setMouseTracking(True)
        okBtn = QPushButton("OK")
        cancelBtn = QPushButton("Cancel")
        self.text = "(x,y): ({0},{1})".format(x, y)
        #self.label = QLabel(self.text, self)
        
        #textLayout = QHBoxLayout()
        #textLayout.setSpacing(10)
        #textLayout.addStretch(1)
        #textLayout.addWidget(self.label, 0, Qt.AlignTop)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(okBtn)
        buttonLayout.addWidget(cancelBtn)
        
        mainLayout = QVBoxLayout()
        mainLayout.addStretch(1)
        #mainLayout.addLayout(textLayout)
        mainLayout.addLayout(buttonLayout)
        
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
        
        self.text = "(x,y): ({0},{1})".format(x, y) 
        self.update()
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
        
    def drawText(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('SansSerif', 12))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

class ooWin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Close window or click <i>Exit</i> to close application.')
        #self.statusBar().showMessage('Ready')
        self.mainerFramer = mainFrame()
        self.setCentralWidget(self.mainerFramer)
        
        #exitAct = QAction(QIcon('exit.png'),'&Close Application', self)
        exitAct = QAction('&Close Application', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        
        #self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        
        self.setWindowTitle('Test Window 04')
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
    