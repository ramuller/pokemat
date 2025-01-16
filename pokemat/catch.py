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

def catch(port, p, distance = 6, right = True, berry = "a"):
    while not p.matchColor(90, 1414, 245, 254, 242):
        try:
            p.waitMatchColor(420, 1923, 220, 220, 220, threashold = 35)
        except:
          print("Catch over")
          break
        p.tapScreen(114, 1757)
        sleep(1)
        no_berry = True
        if berry == "a":
            if p.matchColor(814, 1373, 236, 227, 19):
                p.tapScreen(815, 1375)
                sleep(0.5)
                p.tapScreen(486, 1748)
                sleep(1)
                no_berry = False
            elif p.matchColor(772, 1767, 248, 246, 76):
                p.tapScreen(772, 1767)
                sleep(0.5)
                p.tapScreen(486, 1748)
                sleep(1)
                no_berry = False
            elif p.matchColor(182, 1718, 238, 232, 27):
                p.tapScreen(182, 1718)
                sleep(0.5)
                p.tapScreen(486, 1748)
                sleep(1)
                no_berry = False
        elif berry == "g":
            if p.matchColor(454, 1732, 255, 143, 9):
                p.tapScreen(454, 1718)
                sleep(0.5)
                p.tapScreen(486, 1748)
                sleep(1)
                no_berry = False
        if no_berry:
            sleep(1)
            print("Reomve screen")
            p.tapScreen(795, 191)
            sleep(2)
        sleep(0.5)
        print("distance {}".format(distance))
        p.catch_move(distance = distance)
        sleep(5)
    sleep(1)
    
    p.tapScreen(378, 1382)
    print("Go home")
    p.goHome()
    sleep(1)

def action(port, phone, distance = 15, right = True):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start catching on  \"{}\" on port {}", phone, port)
    
    p = TouchScreen(port, phone)
    catch(port, p, distance, right)

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
    parser.add_argument("-b", "--berry", action="store", required=False, default="g", \
                        help="Name os the phone model. Check phones.json.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port, args.phone, int(args.distance), args.berry)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
