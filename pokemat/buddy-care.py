#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
import random
import math
from pokelib import TouchScreen
from pokelib import PokeArgs
from pokelib import ExPokeLibFatal

import json
import sys
from datetime import datetime



def action(port):
    p = TouchScreen(port)
    rx = int(p.rel_x(0.12))
    ry = int(p.rel_y(0.12))
    degree = 0
    xs = int(p.rel_x(0.5))
    ys = int(p.rel_y(0.6))

    p.tap_down(xs, ys)
    x = xs
    y = ys
    t = 0
    while True:
        t += 1
        dx = xs + int(random.uniform(-rx, rx))
        dy = ys + int(random.uniform(-ry, ry))
        p.moveCursor(x, y, dx, dy, scale=False)
        x = dx
        y = dy
        if t % 25 == 0:
            p.tap_up(x, y)
            sleep(0.4)
            p.tap_down(x, y)
        else:
            sleep(0.05)
        print(f"tap {x} {y} {dx} {dy}")
    while True:
        p.tap_down(xs , ys)
        for i in range(10):
            degree += 36
            x = int(rx * math.cos(math.radians(2*degree)))
            y = int(ry * math.sin(math.radians(degree)))
            dx = int(rx * math.cos(math.radians(2*degree+36)))
            dy = int(ry * math.sin(math.radians(degree+36)))
            p.moveCursor(xs + x, ys + y, xs + dx, ys + dy, scale=False)
            print(f"tap {xs + x} {ys + y} {dx} {dy}")
            p.tap_up(xs + dx, ys + dy)
            sleep(0.1)
            p.tap_down(xs + dx, ys + dy)
        #for d in range(-p.rel_x(0.2), p.rel_x(0.2), int(p.rel_x(0.2)/10)):
        #    p.tap_screen(xs + d, ys + d, scale=False)
        
def main():

    parser = PokeArgs()
    parser.add_argument("-a", "--autoconnect", action='store_true', required=False, default=False, \
                        help="Connnect to autocatch.")    
    parser.add_argument("-d", "--delete-balls", action='store_true', required=False, default=False, \
                        help="Delete all red balls before connect")
    parser.add_argument("-t", "--threads", type=int, action='store', required=False, default=2, \
                        help="Number of threads to find grunt.")    
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
