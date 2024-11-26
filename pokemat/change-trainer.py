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
    print("Select new trinaer {}".format(trainer))
    phone.waitMatchColorAndClick(272, 1126, 160, 219, 147, time_out_ms = 30000)
    phone.waitMatchColorAndClick(253, 1019, 255, 255, 255)
    phone.waitMatchColor(503, 181, 233, 84, 50)
    sleep(1)
    if trainer == "pokeeizu":
        phone.tapScreen(439, 1199)
    elif trainer == "schlumpiz":
        sleep(1)
        phone.tapScreen(390, 1931)
    elif trainer == "pokeralle":
        sleep(1)
        phone.tapScreen(527, 1722)
    elif trainer == "higimmi222":
        sleep(1)
        phone.tapScreen(652, 1019)
    elif trainer == "aphex":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        phone.tapScreen(321, 714)
    elif trainer == "blond":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        # phone.tapScreen(321, 714)
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
    phone.waitMatchColorAndClick(500, 1798, 255, 57, 69)
    phone.waitMatchColorAndClick(940, 210, 212, 251, 204)
    for i in range(0,3):
        phone.scroll(0, -400, start_x=10)
    for y in range(1980, 1500, -20):
        if phone.matchColor(291, y, 250, 251, 248):
            phone.tapScreen(290, y)
            break
    phone.waitMatchColorAndClick(411, 1007, 138, 217, 152)
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
