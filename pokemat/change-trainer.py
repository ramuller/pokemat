#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal

import json
import sys
from datetime import datetime

def selectTrainer(trainer):
    print("Select new trainaer {}".format(trainer))
    sleep(0.5)
    phone.waitMatchColorAndClick(272, 1126, 160, 219, 147, time_out_ms = 30000)
    phone.waitMatchColorAndClick(253, 1019, 255, 255, 255)
    phone.waitMatchColor(503, 181, 233, 84, 50)
    sleep(1)
    if trainer in "pokeeizu":
        sleep(1)
        phone.tapScreen(439, 1199)
    elif trainer in "schlumpiz":
        sleep(1)
        phone.tapScreen(390, 1931)
    elif trainer in "localhost":
        sleep(1)
        phone.tapScreen(543, 828)
    elif trainer in "plastic":
        sleep(1)
        phone.tapScreen(546, 656)
    elif trainer in "pokeralle":
        sleep(1)
        phone.tapScreen(527, 1722)
    elif trainer in "higimmi222":
        sleep(1)
        phone.tapScreen(652, 1019)
    elif trainer in "bluebird":
        sleep(1)
        phone.tapScreen(500, 1363)
    elif trainer in "higimmi333":
        sleep(1)
        phone.tapScreen(565, 1570)
    elif trainer in "higimmi444":
        sleep(1)
        phone.tapScreen(565, 1400)
    elif trainer in "aphex":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        phone.tapScreen(321, 714)
    elif trainer in "helmuteizu":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        phone.tapScreen(321, 1430)
    elif trainer in "blond":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        phone.tapScreen(449, 1091)
    else:
        
        print("Unknow trainer")
        sys.exit(1)

def changeTrainer(port, phone_model, trainer):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Change trainers \"{}\" on port {}", phone_model, port)
    global phone
    phone = TouchScreen(port, phone_model)
    phone.goHome()
    sleep(1)
    phone.waitMatchColorAndClick(500, 1798, 255, 57, 69)
    phone.waitMatchColorAndClick(940, 210, 212, 251, 204)
    for i in range(0,4):
        phone.scroll(0, -400, start_x=10)
    for y in range(1980, 1400, -20):
        print("y = {}".format(y))
        if phone.matchColor(291, y, 250, 251, 248):
            phone.tapScreen(290, y)
            break
        480, 1076, 120, 216, 156
    phone.waitMatchColorAndClick(411, 1037, 133, 217, 152, time_out_ms = 14000)
    selectTrainer(trainer)
    sys.exit(0)
    
    
def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("-t", "--trainer", action="store", required=True, \
                        help="Name os the phone model. Check phones.json.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    changeTrainer(args.port, args.phone, args.trainer)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
