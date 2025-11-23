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

def tradeeeeeeee(host, guest):
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
    
def trainer_battle(jsonFile):
    with open(jsonFile, 'r') as file:
        parameter = json.load(file)
        
    print("Paramter : {}".format(parameter))
    print("Mode {}".format(parameter["mode"]))
    if parameter["mode"] != "battle-friend":
        print("Unsupported {}".format(parameter["mode"]))
        return
    
    print("start trading")
    host = TouchScreen(parameter["host"]["port"], name = parameter["host"]["name"])
    guest = TouchScreen(parameter["guest"]["port"], name = parameter["guest"]["name"])
    tradesDone = 1
    
    while True:
        try:
            host.screen_go_to_home()
            guest.screen_go_to_home()
            host.screen_friend()
            host.friend_search(parameter["guest"]["name"])
            host.friend_select_first()
            sleep(2)
            if host.hasGift():
                time.sleep(0.5)
                host.tap_screenBack()
            sleep(1)
            host.tap_battle()
            host.battle_friend(parameter["league"])
            # guest.screen_go_to_home()
            # guest.screen_friend()
            # guest.friend_search(parameter["host"]["name"])
            # guest.friend_select_first()
            # sleep(2)
            # if guest.hasGift():
            #     time.sleep(0.5)
            #     guest.tap_screenBack()
            # sleep(1)
            # guest.tap_battle()           # time.sleep(2)
            log.info("Time : Battle loop starts {}".format(host.getTimeNow()))
            guest.color_match_wait_click(451, 1226, 126, 215, 155)
            while True:
                guest.color_match_wait_click(486, 1750, 119, 215, 155)
                host.color_match_wait_click(486, 1750, 119, 215, 155)
                sleep(2)
                guest.doBattle(opponent = host)
                host.color_match_wait_click(482, 1232, 119, 215, 155)
                guest.color_match_wait_click(482, 1232, 119, 215, 155)
                print(f"Round completed {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                # sys.exit(0)

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
    parser.add_argument("json", help="json file with the battle configuration.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("bf")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    trainer_battle(args.json)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    
