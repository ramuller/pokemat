#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
import random
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal

import json
import sys
from datetime import datetime



def action(port, phone, distance = 15, right = True, berry = "g"):
    def getX(d, r, offset=0, tilt = 0.0):
        return math.sin(math.radians(d)) * float(r) + float(offset) + float(tilt)    
    def getY(d, r, offset=0, tilt = 0.0):
        return math.cos(math.radians(d)) * float(r) + float(offset) + float(tilt)

    p = TouchScreen(port, phone)
    rx = 220
    ry = 120
    degree = 0
    xs = int(getX(degree, ry, 500))
    ys = int(getY(degree, rx, 1000))
    p.tap_down(xs, ys)
    while True:
        degree += 10
        x = int(getX(degree*3, ry, 500)) + random.randint(-10, 10)
        y = int(getY(degree, rx, 1000)) + random.randint(-10, 10)
        p.moveCursor(xs, ys, x, y)
        p.tap_up(x, y)
        sleep(0.01)
        p.tap_down(x, y)
        xs = x
        ys = y
        sleep(0.01)
        
def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-d", "--distance", action="store", default=15, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
