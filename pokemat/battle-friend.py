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
            if host.matchColor(100, 700, 0, 0, 0, threshold=1):
                log.info("Battle has ended")
                return True
            time.sleep(0.2)
    
def battleFriend(jsonFile):
    with open(jsonFile, 'r') as file:
        parameter = json.load(file)
        
    print("Paramter : {}".format(parameter))
    print("Mode {}".format(parameter["mode"]))
    if parameter["mode"] != "battle-friend":
        print("Unsupported {}".format(parameter["mode"]))
        return
    
    print("start batteling")
    host = TouchScreen(parameter["host"]["port"], name = parameter["host"]["name"])
    guest = TouchScreen(parameter["guest"]["port"], name = parameter["guest"]["name"])
    battlesPlayed = 1
    while True:
        log.info("Time : Batteling starts from beginning {}".format(host.getTimeNow()))
        try:
            host.goHome()
            guest.goHome()
        
            host.inviteFriend(parameter["guest"]["name"], parameter["league"])
            guest.acceptBattleInvite()
            go_on = True
            while go_on: 
                log.info("Time: Battle start from use this team {}".format(host.getTimeNow()))
                battle(host, guest)
                log.info("+++ Battles played {}".format(battlesPlayed))
                battlesPlayed += 1
                host_ok = guest_ok = False
                for i in range(0, 20):
                    try:
                        if not host_ok:
                            host.waitMatchColorAndClick(355, 1275, 147, 217, 150, threashold=20, time_out_ms=1000)
                            host_ok = True
                    except Exception as e:
                        pass
                    try:
                        if not guest_ok:
                            guest.waitMatchColorAndClick(355, 1275, 147, 217, 150, threashold=20, time_out_ms=1000)
                            guest_ok = True
                    except Exception as e:
                        pass
                    if host.isHome() or guest.isHome():
                        log.warn("Someone is home no rematch ")
                        go_on = False
                        i = 9999
                log.info("Time : Batteling ends {}".format(host.getTimeNow()))
        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)

        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)

def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "gifting - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    # parser.add_argument("-p", "--phone", action="store", \
    #                     help="Set phone name default path '/tmp'")
    parser.add_argument("-j", "--json", action="store", required=True, \
                        help="json file with the battle configuration.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("bf")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    battleFriend(args.json)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    