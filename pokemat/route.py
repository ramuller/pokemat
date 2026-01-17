#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
import traceback
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

import json
import sys
from datetime import datetime


def quit_route(phone):
    print("Quit route!!!")
    phone.screen_go_to_home()
    phone.tap_screen(916, 1552)
    sleep(0.75)
    for i in range(3):
        phone.scroll(0, -1800, start_x=900, start_y=1900)
        sleep(0.5)
    phone.buttons.black_on_white('.*QUIT.*', action='press')
    sleep(1)
    phone.buttons.black_on_white('.*QUIT.*', action='press')
    sleep(1)

def end_route(phone):
    print("End route!!!")
    phone.tap_screen(920, 1552)
    sleep(1)
    phone.tap_screen(920, 1552)    
    sleep(1)
    button = phone.buttons.dark('.*COMPLETE.*')
    button = phone.buttons.dark('.*YES.*')
    sleep(4)    
    for i in range(10):
        phone.tap_screen(15, 100)
        sleep(0.5)
    return True

def screen_go_overview(phone):
    t, _ = phone.pocr.regex('.*RSVP.*')
    if t:
        return 0
    phone.screen_go_to_home()
    sleep(0.75)
    phone.tap_screen(900, 1850)
    sleep(0.75)


def follow_route(phone):
    screen_go_overview(phone)
    button = phone.buttons.black_on_white('.*ROUTE.*')
    button = phone.buttons.dark('.*NEARBY.*', retries=30)
    if not button:
        print("Failed to find NEARBY button")
        return False
    sleep(1)
    button = phone.buttons.black_on_white('.*KNOWN.*')
    button = phone.buttons.black_on_white('.*cross.*')
    button = phone.buttons.dark('.*FOLLOW.*', verbose=2)
    if not button:
        print("Failed to find FOLLOW button")
        return False
    sleep(1)
    # Tap to remove info banner
    phone.tap_screen(15, 100)
    sleep(1)    
    phone.tap_screen(15, 100)
    sleep(1)
    print("Following route")
    return True

def route(port):
    print("Start on port {}", port)
    phone = TouchScreen(port)
    # quit_route(phone)
    # end_route(phone)
    # select route
    # phone.screen_go_to_home()
    timeout = 3
    follow = False
    while True:
        try:
            while not phone.color_match(960, 1617, 255, 142, 142) \
                    and timeout > 0:
                timeout -= 1
                print("Following route, time left: {}s".format(timeout))
                screen, _ = phone.pocr.read(verbose=0)
                quit = any(
                    any(word in text.get("text", "") for word in \
                        ["PAUSED", "DISTANCE", "DIRECTION", "paused"])
                    for text in screen
                )
                if (phone.color_match(895, 1535, 255, 255, 255) and phone.color_match(947, 1576, 255, 255, 255) \
                                    and follow == False) or timeout <= 0 or quit:
                    quit_route(phone)
                    follow = False
                    timeout = 0
                    break                       
                if phone.color_match(904, 1542, 255, 158, 0):
                    end_route(phone)
                    timeout = 0
                    follow = False
                    break
                phone.egg_handle()
                sleep(1)
            phone.screen_go_to_home()
            if follow_route(phone):
                follow = True
                timeout = 600
                
            
        except Exception as e:
            print(e, traceback.format_exc())
            print("Something went wrong ignore")
            sleep(600)
            return
        

    
       
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()

    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    while True:
        try:
            route(args.port)
        except Exception as e:
            print(e, traceback.format_exc())
            print("Something went wrong ignore")

           
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
