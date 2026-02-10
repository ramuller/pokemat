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
        print("wait ball")
        for to in range(20, 0, -1):
            p.tap_screen(3, int(p.specs['max_y'] * 0.5), scale=False)
            if p.screen.get_current_screen() == 'home':
                print('On homescreen')
                return False
            elif p.buttons.i_catch_ball.search(retries=1) is not None:
                print("Ball found")
                break
            elif p.buttons.text_only.search('BERRIES', ys=p.rel_y(0.6)):
                p.tap_screen(3, int(p.specs['max_y'] * 0.5), scale=False)
            elif p.buttons.i_exits.press(retries=1):
                p.screen.go_home()
                return True
            else:
                p.tap_screen(p.rel_x(0.5), p.rel_y(0.5))
            sleep(0.3)
        print("Ball ready")

        sleep(1)
        if berry in 'rbags':
            p.buttons.i_catch_berry.press()
            sleep(0.5)
            if berry == "a":
                bs = 'PINAP'
            elif berry == "g":
                bs = 'GOLDEN'
                b = p.buttons.black_on_white('GOLDEN', action='check')
            elif berry == "s":
                bs = 'SILVER'
                b = p.buttons.black_on_white('SILVER', action='check')
            elif berry == "r":
                bs = 'RAZZ'
                b = p.buttons.black_on_white('RAZZ', action='check')
            elif berry == "b":
                bs = 'NANAB'
    
            for i in range(5):
                b = p.buttons.text_only.search(bs, ys=p.rel_y(0.6))
                if b:
                    sleep(0.5)
                    print(f'tap on x{b['center'][0]} y{b['top'] - 3 * b['height']}')
                    p.tap_screen(b['center'][0], b['top'] - 3 * b['height'], scale=False)
                    p.tap_screen(b['center'][0], b['top'] - 3 * b['height'], scale=False)
                    sleep(1)
                    if p.buttons.b_catch_berry.search():
                        p.tap_screen(3, int(p.specs['max_y'] * 0.5), scale=False)
                        sleep(1)
                    else:
                        sleep(1.5)
                        # Feed the berry
                        p.tap_screen(int(p.specs['max_x'] * 0.5), 
                                 int(p.specs['max_y'] * 0.85),
                                 scale=False)
                break

        if span != 0:
            d = distance + randrange(-span,span)
        else:
            d = distance
        print("distance {}".format(d))
        for i in range(20):
            if p.buttons.i_catch_ball.search(retries=1) is not None:
                p.catch_move(distance = d)
                break
            sleep(0.5)
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
