#!/bin/env python
import time
from time import sleep
import os
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
from pokelib import ScreenRegion


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
    p.buttons.b_catched_OK.press(retries=1)
    print("Go home")
    p.screen_go_to_home()

def catch(p, distance = 6, right = True, berry = "a", max_tries = 25, span = 0):
    while max_tries >= 0: # not p.color_match(90, 1414, 245, 254, 242):
        max_tries -= 1
        print("wait ball")
        if p.buttons.i_exit_man.search(retries=1, verbose=0) is not None:
            print('Exit man found')
        for to in range(20, 0, -1):
            # p.tap_screen(3, int(p.specs['max_y'] * 0.5), scale=False)
            if p.screen.get_current_screen() == 'home':
                print('On homescreen')
                return False
            elif p.buttons.i_button_ok.search(retries=1, verbose=0) is not None:
                print("OK found")
                end_catch(p)
                return True
            elif p.buttons.i_catch_ball.search(retries=1, verbose=0) is not None \
                and p.buttons.i_catch_berry.search(retries=1, verbose=0) is not None:
                print("Ball found")
                break
            elif p.buttons.text_only.search('BERRIES', ys=p.rel_y(0.6)):
                p.tap_screen(3, int(p.specs['max_y'] * 0.5), scale=False)
            elif p.buttons.i_exits.press(retries=1):
                p.screen.go_home()
                return True
            elif p.buttons.t_catch_caught.press(retries=1):
                print("Pokemon caught")
                end_catch(p)
                return True
            else:
                if to % 5 == 0:
                    # print(f'Waiting for ball {to} tap center')
                    p.tap_screen(p.rel_x(0.5), p.rel_y(0.5))
            sleep(0.5)
        print("Ball ready")

        sleep(1)
        if berry != "n":
            bs = select_berry(p, berry)            
            berry_already = p.buttons.b_catch_berry.search(retries=2)
            if berry_already:
                p.tap_screen(p.rel_x(0.1), berry_already['center'][1], scale=False)
                sleep(0.5)
            else:
                sleep(1.5)

        if span != 0:
            d = distance + randrange(-span,span)
        else:
            d = distance
        p.tap_screen(p.rel_x(0.5), p.rel_y(0.9), scale=False)
        sleep(1)
        print("distance {}".format(d))
        for i in range(20):
            ball = p.buttons.i_catch_ball.search(retries=1)
            if p.buttons.i_button_ok.search(retries=1, verbose=0) is not None:
                print("End catch OK found")
                end_catch(p)
                return True
            elif ball is not None:
                print("Throwing ball found start catch move")
                p.catch_move(distance = d)
                sleep(2)
                break
            if i % 5 == 0:
                p.tap_screen(p.rel_x(0.5), p.rel_y(0.9), scale=False)
            sleep(0.5)
        max_tries -= 1
        sleep(1)
    print('Catch failed')
    return True


def select_berry(p, berry):
    if berry in 'rbags':
        p.buttons.i_catch_berry.press()
        sleep(0.5)
        if berry == "a":
            bs = '.*PINAP BERRY.*'
        elif berry == "g":
            bs = '.*GOLDEN RAZZ.*'
        elif berry == "s":
            bs = '.*SILVER PINAP.*'
        elif berry == "r":
            bs = '.*RAZZ BERRY.*'
        elif berry == "b":
            bs = '.*NANAB BERRY.*'
        sleep(1)
        for i in range(5):
            b = p.buttons.scan_vertical.search(bs, 
                                               start_rel=0.6, 
                                               mode='line', 
                                               verbose=0)
            if not b:
                sleep(0.5)
                continue
            step = p.rel_x(1) // 3
            ys = b['top'] - 10
            ye = b['top'] + b['height'] + 10

            for x in range(3):
                b = p.buttons.text_only.search(bs, 
                                               xs=x*step, xe=x*step+step,
                                               ys=ys, ye=ye,
                                               mode='line',
                                               verbose=0)
                print(b)
                if b != []:
                    break
            if b == []:
                print(f'No berry {berry} found')
                return None
            else:
                break
        sleep(1)
        try:
            x = b['center'][0]
            y = b['top'] - b['height']
            p.tap_screen(x, y, scale=False)
        except Exception as e:
            print(f'Error selecting berry {berry} : {e}')
            return None

        return True
    return None
                
def action(port, distance = 15, right = True, berry = "a", span = 0):
    print("Start catching on  \"{}\" on port {}", port)
    
    p = TouchScreen(port)

    catch(p, distance, right, berry, span = span)

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
