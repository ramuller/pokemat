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

def action(port, phone, distance = 15, right = True, berry = "g"):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start catching on  \"{}\" on port {}", phone, port)
            
    p = TouchScreen(port, phone)
    while True:
        p.tapScreen(500, 1590)
        sleep(0.1)
        p.tapScreen(500, 1790)
        sleep(0.1)

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
    action(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
