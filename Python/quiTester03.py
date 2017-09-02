#!/usr/bin/python3
# -*- coding: utf-8 -*-

## Adapted from http://zetcode.com/gui/pyqt5/firstprograms/ ##

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, 
    QPushButton,QApplication, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
#from PyQt5.QtGui import QIcon

winWid = 320
winHi = 240
## get default desktop resolution, use for width/height/placement?

class ooWin(QWidget):

    def __init__(self):
        super().__init__()
        global winWid, winHi
        if (len(sys.argv) > 1):
                winWid = int(sys.argv[1])
                winHi = int(sys.argv[1])
                if (len(sys.argv) > 2):
                    winHi = int(sys.argv[2])
        self.initUI()
    
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Close window or click <i>\'quit\'</i> to exit application.')
        
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>button</b>')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        
        quitBtn = QPushButton('Quit', self)
        quitBtn.clicked.connect(QCoreApplication.instance().quit)
        quitBtn.setToolTip('Click here to quit.')
        quitBtn.resize(quitBtn.sizeHint())
        quitBtn.move(150, 50)
        
        self.setGeometry(400, 200, winWid, winHi)
        self.setWindowTitle('Test Window 02')
        self.center()
        self.show()
        
    def center(self):
        screen = self.primaryScreen()
        print(screen)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
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
    