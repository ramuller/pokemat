#!/bin/env python

# All X/Y coordinates used a virtual playfield of 1000x2000
# Default scaling uses an S7 screen resulution of 576x1024
# paramters scale-x and scale-y can be used to overwrite default

import argparse
import time
from time import sleep
import os
import logging
from xlwt.ExcelFormulaParser import RB
from sympy.core.tests import test_truediv
from _ast import And

maxX = 100000
maxY = 200000

global log

class TouchScreen:
    def __init__(self, fifoName):
        log.info("Pokemat phone : {}".format(fifoName))
        fd = os.open("{}.sh".format(fifoName), os.O_RDWR|os.O_CREAT)
        self.fi = os.fdopen(fd, "r")
        self.fi.seek(0, 2)            
        self.fo = fifoName

    def writeToTouch(self, cmd):
        log.debug("Send CMD - {}".format(cmd))
        with open(self.fo, 'w') as fo:
            fo.write(cmd)
    
    def click(self, x, y, button = 1, duration = 300):
        log.info("click:{},{},{},{}\n".format(x,y,button, duration))
        self.writeToTouch("click:{},{},{},{}\n".format(x,y,button, duration))
        time.sleep(0.001 * duration)
    
    def getRGB(self, x, y):
        self.fi.seek(0, 2)            
        self.writeToTouch("color:{},{}\n".format(x,y))
        # time.sleep(1)
        l = ""
        while not "color" in l:
            l = self.fi.readline().rstrip()
            time.sleep(0.005)
        # Create a list
        ll = l.split(":")
        # create value list
        log.debug(ll)
        vl = ll[1].split(",")
        # print(vl)
        r,g,b = int(vl[2]), int(vl[3]), int(vl[4])
        log.debug("getRGB : ({},{}) r{} g{} b{}".format(x, y, r, g,b))
        return r, g, b
    

    '''
    Wait for timeOut until color is on the pixel
    '''
    def matchColor(self, x, y, r, g, b, threshold=10, timeOutMs=1):
        while timeOutMs > 0:
            sr, sg, sb = self.getRGB(x, y)
            if      sr < (r + threshold) and  sr > (r - threshold) and \
                    sg < (g + threshold) and  sg > (g - threshold) and \
                    sb < (b + threshold) and  sb > (b - threshold):
                    log.debug("color match ({},{},{})-({},{},{})".format(r,g,b,sr,sg,sb))
                    return True
            sleep(0.100)
            timeOutMs = timeOutMs - 100
            # raise Exception('goHome : Color mismatch!')
        return False
    
    def cancel(self):
        log.debug("cancel")
        self.click(501, 1857)
        
    def pressOK(self):
        self.matchColor(623,1062,83,212,162, timeOutMs=5)
        self.click(623,1062)
        return True

    def exitMode(self):
        log.debug("exit mode")
        self.click(85,190)
        self.pressOK()
        
    def goHome(self):
        log.info("Go to homescreen")
        while self.matchColor(5000,18420,255,56,69) == False:
            if self.matchColor(5000,18570,38,133,148):
                self.cancel()
            elif self.matchColor(5000,18570,113,174,173):
                self.cancel()
            # elif self.matchColor(83,191,135,150,0):
            #     self.exitMode()
            else:
                raise Exception("goHome : Unknow situation")
            sleep(1)
    
    def trainerScreen(self):
        log.debug("Trainer screen")
        self.click(116,1810)
        print(self.matchColor(821,760,250,250,250, timeOutMs=2000))
        
    def sortHasGift(self):
        log.debug("Has gift")
        self.click(403, 741)
        self.matchColor(400,891, 31, 133, 151, timeOutMs=2000)
        self.click(400, 744)
        
    

def gifting():
    canReceive = True   # Changes after Daily limit reached
    canSend = True
    
    log.info("Start gifting mode")
    ts = TouchScreen(args.phone)
    ts.goHome()
    ts.trainerScreen()
    # ts.sortHasGift()

def attack():
    log.info("Start attack mode")
    ts = TouchScreen(args.phone)
    
    while True:
        ts.click(int(maxX / 2), int(maxY - 0.09 * maxY))
        for x in range(int(maxX / 20), maxX, int(maxX / 8)):
            y = maxY - x
            log.debug("Atack {} {}". format(x,y))
            ts.click(x, y, duration = 70)
            ts.click(int(maxX - x) , y, duration = 70)
 
   
        
def testing():
    ts = TouchScreen(args.phone)
    for y in range(200,201,1):
        #print("read Y : {}".format(y))
        # time.sleep(1)
        #print(ts.getRGB(200,y))
        print(ts.getRGB(200,200))
        
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
                        "gifting - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.DEBUG)
    parser.add_argument("-p", "--phone", action="store", required=True, \
                        help="Set phone name default path '/tmp'")
    global args
    args = parser.parse_args()
    if args.phone[0] != "/":
        args.phone = "/tmp/{}".format(args.phone)
        
    global log 
    log = logging.getLogger(args.phone.split("/")[-1])
    logging.basicConfig(level=args.loglevel)
    log.debug("args")
    
    if args.mode == "gifting":
        gifting()
    elif args.mode == "attack":
        attack()()
    else:
        log.error("Unknow operationl mode {}".format(args.mode))
        exit(1)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    