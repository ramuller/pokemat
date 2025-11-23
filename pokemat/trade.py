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
            print("Friend screen")
            host.friend_search(parameter["guest"]["name"])
            host.friend_select_first()
            sleep(2)
            if host.hasGift():
                time.sleep(0.5)
                host.tap_screenBack()
            sleep(1)
            host.tap_trade()
            # time.sleep(2)
            retry = 0
            while True:
                if retry > 3:
                    raise
                retry += 1
                guest.screen_friend()
                sleep(3)
                if guest.color_match(41, 796, 255, 246, 208, debug=True) == True:
                    log.info("Found inviting friend")
                    break
                log.info("No one invites let's retry")
                                   
            guest.friend_select_first()
            sleep(2)
            if guest.hasGift():
                print("Has gift")
                guest.tap_screenBack()
            time.sleep(1)
            guest.tap_trade()
            
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
                host.color_match_wait_click(46, 724, 255, 255, 255, time_out_ms=60000)
                guest.color_match_wait_click(46, 724, 255, 255, 255, time_out_ms=60000)
                try:
                    host.color_match_wait_click(177, 724, 255, 255, 255, same=False, time_out_ms=60000)
                    guest.color_match_wait_click(177, 724, 255, 255, 255, same=False, time_out_ms=60000)
                except:
                    host.tap_screen(177, 724)
                    guest.tap_screen(177, 724)
                # tap twice because sometimes it missing a tap
                time.sleep(1.0)
                host.tap_screen(177, 724)
                guest.tap_screen(177, 724)
                time.sleep(0.5)
                host.tap_screen(177, 724)
                guest.tap_screen(177, 724)
                # Click Next
                host.color_match_wait_click(371, 1605, 147, 217, 150)
                guest.color_match_wait_click(371, 1605, 147, 217, 150)
                # for to in range(0, 10):
                #     host.pocr_wait_text_center((), (), "CONFIRM", pause=0.5)
                #     break
                # Click confirm
                host.color_match_wait_click(17, 1037, 92, 204, 146, time_out_ms=60000)
                guest.color_match_wait_click(17, 1037, 92, 204, 146, time_out_ms=60000)
                # Wait trade complete
                host.color_match_wait_click(482, 1849, 28, 135, 149, time_out_ms=60000)
                guest.color_match_wait_click(482, 1849, 28, 135, 149, time_out_ms=60000)
                time.sleep(2)
                host.tap_trade()
                guest.tap_trade()
                
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
    parser.add_argument("json", help="json file with the battle configuration.")
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
    