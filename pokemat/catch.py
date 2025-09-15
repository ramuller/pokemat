#!/bin/env python
import time
from time import sleep
import os
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

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
    p.screen_go_to_home()

def catch(p, distance = 6, right = True, berry = "a", max_tries = 25, span = 0):
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
            colors = (239,230,19)
        elif berry == "g":
            colors = (255,129,35)
        elif berry == "s":
            colors = (162,178,179)
        elif berry == "r":
            colors = (40,69,91)
        elif berry == "b":
            colors = (247,113,129)
        elif berry == "a":
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
            elif p.color_match(500, 1718, 238, 232, 27):
                p.tap_screen(500, 1718)
                sleep(0.5)
                p.tap_screen(486, 1748)
                sleep(1)
                no_berry = False
        elif berry == "g":
            time.sleep(0.5)
            if not p.color_match(454, 1732, 255, 143, 9) \
               and not p.color_match(74, 1228, 206, 207, 202):
                p.scroll(800,0, start_y = 1750, tap_time = 1)
                time.sleep(0.5)
            # if p.color_match(454, 1732, 255, 143, 9):
            if p.color_match(151, 1726, 255, 147, 24):
                # p.tap_screen(454, 1718)
                p.tap_screen(168, 1718, duration = 130)
                sleep(0.5)
                p.tap_screen(186, 1718)
                sleep(1)
                no_berry = False
        elif berry == "s":
            # if not p.color_match(151, 1742, 181, 190, 191):
            #     p.scroll(800,0, start_y = 1750, tap_time = 1)
            # time.sleep(0.5)
            if p.color_match(151, 1742, 181, 190, 191):
                p.tap_screen(151, 1748)
                sleep(0.5)
                p.tap_screen(500, 1748)
                sleep(1)
                no_berry = False
        for y in [1375, 1750]:
            for x in [180, 500, 820]:
                if p.color_match(x, y, colors[0], colors[1], colors[2]):
                    # Select ball
                    p.tap_screen(x, y)
                    sleep(0.5)
                    # Throug ball
                    p.tap_screen(500, 1748)
                    sleep(1)
                    no_berry = False
                    break
        if no_berry:
            sleep(1)
            print("Remomve screen")
            p.tap_screen(795, 191)
            sleep(2)
        # sys.exit(0)
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
                
def action(port, distance = 15, right = True, berry = "a", span = 0):
    print("Start catching on  \"{}\" on port {}", port)
    
    p = TouchScreen(port)
    catch(p, distance, right, berry,span = span)

def main():

    global args
    parser = PokeArgs()

    parser.add_argument("-d", "--distance", action="store", default=6, \
                        help="TCP port for the connection.")
    parser.add_argument("-b", "--berry", action="store", required=False, default="a", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("-s", "--span", action="store", required=False, default=0, \
                        help="Vary distance by span.")
    args = parser.parse_args()

    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port, int(args.distance), berry = args.berry, span = int(args.span))
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
