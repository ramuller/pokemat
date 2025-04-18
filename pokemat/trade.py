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
    
def trade(jsonFile):
    with open(jsonFile, 'r') as file:
        parameter = json.load(file)
        
    print("Paramter : {}".format(parameter))
    print("Mode {}".format(parameter["mode"]))
    if parameter["mode"] != "trade":
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
            host.selectFirstFriend()
            if host.hasGift():
                time.sleep(0.5)
                host.tap_screenBack()
            host.tapTrade()
            # time.sleep(2)
            while True:
                guest.screen_friend()
                if guest.color_match(41, 796, 255, 246, 208, debug=True) == True:
                    log.info("Found inviting friend")
                    break
                log.info("No one invites let's retry")
                    
                
            guest.selectFirstFriend()
            if guest.hasGift():
                print("Has gift")
                guest.tap_screenBack()
            time.sleep(1)
            guest.tapTrade()
            
            host.pokemon_search(parameter["host"]["filter"])
            guest.pokemon_search(parameter["guest"]["filter"])
            
            log.info("Time : Trading loop starts {}".format(host.getTimeNow()))
            while True:
                # Wait for the blue screen
                #try:
                #    host.color_match_wait(95, 396, 101, 179, 246, time_out_ms=1000)
                # except:
                #    pass
                # Select left corner
                time.sleep(1)
                host.color_match_wait_click(46, 724, 255, 255, 255)
                guest.color_match_wait_click(46, 724, 255, 255, 255)
                try:
                    host.color_match_wait_click(177, 724, 255, 255, 255, same=False)
                    guest.color_match_wait_click(177, 724, 255, 255, 255, same=False)
                except:
                    host.tap_screen(177, 724)
                    guest.tap_screen(177, 724)
                # tap twice because sometimes it missing a tap
                time.sleep(0.2)
                host.tap_screen(177, 724)
                guest.tap_screen(177, 724)
                # Click Next
                host.color_match_wait_click(371, 1605, 147, 217, 150)
                guest.color_match_wait_click(371, 1605, 147, 217, 150)
                # Click confirm
                host.color_match_wait_click(17, 1037, 92, 204, 146)
                guest.color_match_wait_click(17, 1037, 92, 204, 146)
                # Wait trade complete
                host.color_match_wait_click(482, 1849, 28, 135, 149, time_out_ms=30000)
                guest.color_match_wait_click(482, 1849, 28, 135, 149, time_out_ms=30000)
                host.tapTrade()
                guest.tapTrade()
                
                print("Fertig")
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
    parser.add_argument("-j", "--json", action="store", required=True, \
                        help="json file with the battle configuration.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("bf")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    trade(args.json)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    