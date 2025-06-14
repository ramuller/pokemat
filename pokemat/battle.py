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
from pokelib import PokeArgs

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
    
def battle(port, type, league):
    
    phone = TouchScreen(port)
    # phone.scroll(0, -100)
    # sys.exit(0)
    cont = True
    while cont:
        # cont = False
        try:
            phone.screen_go_to_home()
            connection_retry = 0
            log.info("Time : battle {}".format(phone.getTimeNow()))
            phone.screen_battle()
            if type == "league" or type == "l":
                phone.battle_league()
            elif type == "trainer1":
                phone.battleTrainer(1, league)
            elif type == "trainer2":
                phone.battleTrainer(2, league)
            elif type == "trainer3":
                phone.battleTrainer(3, league)
            
        except ExPokeLibFatal as e:
            sleep(1)
            if connection_retry > 100: # Seems really dead
                log.fatal("Unrecoverable situation. Give up")
                sys.exit(1)
            connection_retry += 1
            print(f"Retry phone connection {connection_retry}")

        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)

def main():

    parser = PokeArgs()
    global args
    parser.add_argument("-t", "--type", action="store", required=False, default="league", \
                        help="Battle type firstleague.")
    parser.add_argument("-L", "--league", action="store", required=False, default="great", \
                        help="Battle type firstleague.")
    args = parser.parse_args()

    global log 
    log = logging.getLogger("battle")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    battle(args.port, args.type, args.league)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    
