#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
import random
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal

import json
import sys
from datetime import datetime
from yaml import _yaml
import _ruamel_yaml
from ply.yacc import yacc

def action(port, phone, distance = 15, right = True, berry = "g"):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    p = TouchScreen(port, phone)
    x = 500
    y = 1250
    r = 220
    while True:
        x1 = x + random.randint(-r,r) 
        y1 = y +  random.randint(-r,r) 
        x2 = x + random.randint(-r,r) 
        y2 = y +  random.randint(-r,r)
        p.tapDown(x1, y1)
        for xa in range(x1, x2, int((x2 - x1) / 10)):
            for ya in range(y1, y2, int ((y2 - y1) / 10)):
                p.moveCursor(x1, y1, xa, ya)
                x1 = xa
                y1 = yacc
        sleep(0.1)           
        p.tapUp(x2, y2)

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
