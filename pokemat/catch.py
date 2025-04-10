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
from mercurial.hgweb.common import continuereader
from random import randrange

def getX(d, r, offset=0):
    return math.sin(math.radians(d)) * float(r) + float(offset)

def getY(d, r, offset=0):
    return math.cos(math.radians(d)) * float(r) + offset

def end_catch(p):    
    sleep(1)
    print("Catch over")
    p.tap_screen(378, 1352)
    print("Go home")
    p.goHome()

def catch(port, p, distance = 6, right = True, berry = "a", max_tries = 25, span = 0):
    while max_tries >= 0: # not p.color_match(90, 1414, 245, 254, 242):
        max_tries -= 1
        for to in range(20, 0, -1):
            if p.color_match(392, 1400, 142, 219, 152) or to == 0:
                print("game over")
                end_catch(p)
                return
            elif p.is_home():
                return
            try:
                if p.color_match_wait(420, 1912, 220, 220, 220, threashold=35, time_out_ms=1000):
                    print("Ball found")
                    break
            except:
                pass
            sleep(1)
        print("Ball ready")
        p.tap_screen(500, 1748)
        sleep(0.5)
        p.tap_screen(114, 1757)
        sleep(1)
        no_berry = True
        if berry == "a":
            if p.color_match(814, 1373, 236, 227, 19):
                p.tap_screen(815, 1375)
                sleep(0.5)
                p.tap_screen(486, 1748)
                sleep(1)
                no_berry = False
            elif p.color_match(772, 1767, 248, 246, 76):
                p.tap_screen(772, 1767)
                sleep(0.5)
                p.tap_screen(486, 1748)
                sleep(1)
                no_berry = False
            elif p.color_match(182, 1718, 238, 232, 27):
                p.tap_screen(182, 1718)
                sleep(0.5)
                p.tap_screen(486, 1748)
                sleep(1)
                no_berry = False
        elif berry == "g":
            if not p.color_match(454, 1732, 255, 143, 9):
                p.scroll(800,0, start_y = 1750, tap_time = 1)
            time.sleep(0.5)
            if p.color_match(454, 1732, 255, 143, 9):
                p.tap_screen(454, 1718)
                sleep(0.5)
                p.tap_screen(486, 1748)
                sleep(1)
                no_berry = False
        elif berry == "s":
            if not p.color_match(151, 1742, 181, 190, 191):
                p.scroll(800,0, start_y = 1750, tap_time = 1)
            time.sleep(0.5)
            if p.color_match(151, 1742, 181, 190, 191):
                p.tap_screen(151, 1748)
                sleep(0.5)
                p.tap_screen(500, 1748)
                sleep(1)
                no_berry = False
        if no_berry:
            sleep(1)
            print("Reomve screen")
            p.tap_screen(795, 191)
            sleep(2)
        sleep(0.5)
        if span != 0:
            d = distance + randrange(-span,span)
        else:
            d = distance
        print("distance {}".format(d))            
        p.catch_move(distance = d)
        sleep(5)
        if p.color_match(392, 1400, 142, 219, 152) or to == 0:
            print("game over")
            end_catch(p)
            return False
    return True
                
def action(port, phone, distance = 15, right = True, berry = "a", span = 0):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start catching on  \"{}\" on port {}", phone, port)
    
    p = TouchScreen(port, phone)
    catch(port, p, distance, right, berry,span = span)

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
    parser.add_argument("-b", "--berry", action="store", required=False, default="a", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("-s", "--span", action="store", required=False, default=0, \
                        help="Vary distance by span.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port, args.phone, int(args.distance), berry = args.berry, span = int(args.span))
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
