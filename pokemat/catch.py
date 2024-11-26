#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal

import json
import sys
from datetime import datetime

def getX(d, r, offset=0):
    return math.sin(math.radians(d)) * float(r) + float(offset)

def getY(d, r, offset=0):
    return math.cos(math.radians(d)) * float(r) + offset

def catch(port, phone, right = True):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start catching on  \"{}\" on port {}", phone, port)
    
    p = TouchScreen(port, phone)
    p.tapScreen(114, 1757)
    sleep(0.5)
    if p.matchColor(814, 1373, 236, 227, 19):
        p.tapScreen(815, 1375)
        sleep(0.5)
        p.tapScreen(486, 1748)
        sleep(1)
    else:
        sleep(1)
        print("Reomve screen")
        p.tapScreen(795, 191)
        sleep(2)
    sleep(0.5)
    start = -60
    end = 460
    step = 8
    radius = 250 
    off_x = 500
    off_y = 1250
    off_y = 900
    x = getX(start, radius, off_x) 
    y = getY(start, radius, off_y)
    p.tapDown(x, y)
    a  = start + step
    b = 0.0
    while a < end + step:
        a = a + step + int(a / 60)
        b = b + 0.2
        t = radius + int(b)
        radius = t
         # for a in range(start + step, end + step, step):
        sx = x
        sy = y
        
        if right:
            x = off_x + getX(a, radius)
        else:  
            x = off_x - getX(a, radius)
        y = getY(a, radius, off_y) # - a * 2
        # print("x = {}".format(x))
        p.moveCursor(int(sx), int(sy), int(x), int(y))
        # canvas.create_line(sx, sy, x, y)
        # canvas.update()
        sleep(0.015)

    y1 = y
    for y2 in range(int(y) - 10 , int(y) - 100, -10):
        p.moveCursor(int(x), int(y1), int(x), int(y2))
        y1 = y2
    
    p.tapUp(x, y)
            
       
def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    catch(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
