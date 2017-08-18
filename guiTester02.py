#!/usr/bin/python3
# -*- coding: utf-8 -*-

## Adapted from http://zetcode.com/gui/pyqt5/firstprograms/ ##

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

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
        self.setGeometry(400, 200, winWid, winHi)
        self.setWindowTitle('Test Window 02')
        self.setWindowIcon(QIcon('web.png'))
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    oow = ooWin()
    sys.exit(app.exec_())
    
    
#    w = QWidget()
#    ## if commandline args given, 1: squar 2: rect 0: default
#    if (len(sys.argv) > 1):
#        winWid = int(sys.argv[1])
#        winHi = int(sys.argv[1])
#        if (len(sys.argv) > 2):
#            winHi = int(sys.argv[2])
#    w.resize(winWid, winHi)
#    w.move(400, 200)
#    w.setWindowTitle('Test Window 01')
#    w.show()
#    
#    sys.exit(app.exec_())