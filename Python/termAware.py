import os
import sys
import time

def main():
    while(True):
        loop()
        #time.sleep(0.25) ## can reduce bottom-line flicker by including a slight delay -- coder discretion
    
def loop():
    sz = os.popen('stty size', 'r').read()
    cols = sz.split()[1]
    rows = sz.split()[0]
    myText = ""
    myText += "Terminal window is {0} cols wide and {1} rows tall!\n".format(cols, rows)
    for x in range(int(rows) - 3):
       myText += "\n"
    print(myText) ## trailing comma to prevent addition of '\n'?
    
    ## stdout doesn't append '\n' to the end of statements, but also is another import --  coder discretion
    #sys.stdout.write(myText) 
    
main()