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
            if host.matchColor(100, 100, 0, 0, 0):
                log.info("Battle has ended")
                return True
            time.sleep(0.2)
    
def evolve(port, phone, filter):
    
    can_get_gifts = True
    can_send_gifts = True
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start evolutions \"{}\" on port {}", phone, port)
    phone = TouchScreen(port, phone)
    # phone.scroll(0, -100)
    # sys.exit(0)
    phone.selectPokemon(filter)
    giftsSent = 0
    giftsReceived = 0
    while True:
        log.info("Time : Evolve {}".format(phone.getTimeNow()))
        try:
            phone.selectFirstPokemon()
            phone.evolvePokemon()
        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            # sys.exit(1)

        except Exception as e:
            phone.selectPokemon(filter)
            print("Upps something went wrong but who cares?: {}", e)

def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    # parser.add_argument("-p", "--phone", action="store", \
    #                     help="Set phone name default path '/tmp'")
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("-f", "--filter", action="store", required=True, \
                        help="Pokemon filter string.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    evolve(args.port, args.phone, args.filter)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    
