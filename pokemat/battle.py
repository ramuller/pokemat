#!/bin/env python

# All X/Y coordinates used a virtual playfield of 1000x2000
# Default scaling uses an S7 screen resulution of 576x1024
# paramters scale-x and scale-y can be used to overwrite default
# 139 + testing
# 52
# 74
# dreepy

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
from _operator import truediv

global log

def battle(host, guest):
    host.useThisParty()
    guest.useThisParty()
    
    while True:
        host.click(331, 1697)
        guest.click(331, 1697)
        for i in range(0,5):
            if host.color_match(100, 100, 0, 0, 0):
                log.info("Battle has ended")
                return True
            time.sleep(0.2)
    
def battle(port, phone, type, league):
    
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start battle\" on port {}", phone, port)
    phone = TouchScreen(port, phone)
    # phone.scroll(0, -100)
    # sys.exit(0)
    cont = True
    while cont:
        # cont = False
        try:
            phone.goHome()
            log.info("Time : battle {}".format(phone.getTimeNow()))
            phone.goBattle()
            if type == "league" or type == "l":
                phone.battleLeague()
            elif type == "trainer1":
                phone.battleTrainer(1, league)
            elif type == "trainer2":
                phone.battleTrainer(2, league)
            elif type == "trainer3":
                phone.battleTrainer(3, league)
            
        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)

        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)

def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "battle - send and receive gifts")
    # parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    # parser.add_argument("-p", "--phone", action="store", \
    #                     help="Set phone name default path '/tmp'")
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("-t", "--type", action="store", required=False, default="trainer2", \
                        help="Battle type firstleague.")
    parser.add_argument("-L", "--league", action="store", required=False, default="great", \
                        help="Battle type firstleague.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("battle")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    battle(args.port, args.phone, args.type, args.league)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    