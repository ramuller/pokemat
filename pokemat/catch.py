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
            print("wait ball")
            # p.buttons.ocr.process = False
            p.buttons.startx = int(p.specs['max_x'] * 0.40)            
            p.buttons.endx = int(p.specs['max_x'] * 0.60)            
            p.buttons.starty = int(p.specs['max_y'] * 0.65)            
            if p.buttons.dark('OK', action='press', retries=1, verbose=10):
            # if p.buttons.white_on_black('OK', action='press', 
            #                            verbose=10, retries=1):
                p.screen_go_to_home()
                return True
            elif p.buttons.i_catch_ball.search() is not None:
                print("Ball found")
                break
            elif p.buttons.black_on_white('BERRIES', action='check'):
               p.tap_screen(3, int(p.specs['max_y'] * 0.5), scale=False)

            elif p.screen.get_current_screen() == 'home':
                return False
            sleep(0.3)
        print("Ball ready")

        sleep(1)
        if berry in 'rbags':
            p.buttons.i_catch_berry.press()
            sleep(0.5)
            if berry == "a":
                p.pocr.starty = int(p.specs['max_y'] * 0.6)
                b = p.buttons.black_on_white('PINAP', action='check')
            elif berry == "g":
                b = p.buttons.black_on_white('GOLDEN', action='check')
            elif berry == "s":
                b = p.buttons.black_on_white('SILVER', action='check')
            elif berry == "r":
                b = p.buttons.black_on_white('RAZZ', action='check')
            elif berry == "b":
                b = p.buttons.black_on_white('NANAB', action='check')
        if b:
            p.tap_screen(b['center'][0], b['top'] - 3 * b['height'], scale=False)
            sleep(0.5)
            p.tap_screen(int(p.specs['max_x'] * 0.5), 
                         int(p.specs['max_y'] * 0.85),
                         scale=False)
        else:
            p.pocr.starty = int(p.specs['max_y'] * 0.5)
            p.pocr.endy = int(p.specs['max_y'] * 0.64)
            p.tap_screen(3, int(p.specs['max_y'] * 0.5), scale=False)

        sleep(3)

        if p.buttons.black_on_white('BERRIES', action='check'):
            p.tap_screen(3, int(p.specs['max_y'] * 0.5), scale=False)
        
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
