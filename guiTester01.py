#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget

winWid = 320
winHi = 240
## get default desktop resolution, use for width/height/placement?

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    print(sys.argv)
    
    w = QWidget()
    ## if commandline args given, 1: squar 2: rect 0: default
    if (len(sys.argv) > 1):
        winWid = int(sys.argv[1])
        winHi = int(sys.argv[1])
        if (len(sys.argv) > 2):
            winHi = int(sys.argv[2])
    w.resize(winWid, winHi)
    w.move(400, 200)
    w.setWindowTitle('Test Window 01')
    w.show()
    
    sys.exit(app.exec_())