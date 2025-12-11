#!/bin/env python
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


def quit_route(phone):
    print("Quit route!!!")
    phone.tap_screen(960, 1617)
    sleep(0.75)
    for i in range(3):
        phone.scroll(0, -1800, start_x=900, start_y=1900)
        sleep(0.5)
    
    phone.tap_screen(491, 1458)
    sleep(0.5)
    phone.tap_screen(491, 1458)
    
def end_route(phone):
    print("End route!!!")
    phone.tap_screen(920, 1552)
    sleep(1)
    phone.tap_screen(920, 1552)    
    sleep(1)
    regex = "COMPLETE ROUTE"
    t, _ = phone.pocr_find_regex(regex)
    if t:
        phone.tap_screen(t['center'], scale=False)
    else:
        return False
            
    sleep(1)
    t, _ = phone.pocr_find_regex('YES')
    if t:
        phone.tap_screen(t['center'], scale=False)
    
    for i in range(6):
        phone.tap_screen(373, 1000)
        sleep(0.5)
    return True


def route(port, phone):
    print("Start route \"{}\" on port {}", phone, port)
    phone = TouchScreen(port, phone)
    quit_route(phone)
    phone.screen_go_to_home()
    end_route(phone)
    # select route
    while True:
        try:
            if phone.color_match(923, 1542, 252, 255, 253) or phone.color_match(904, 1542, 255, 158, 0):
                quit_route(phone)
            sleep(0.75)
            phone.tap_screen(900, 1850)
            sleep(0.75)
            # route 
            phone.tap_screen(876, 287)
            # Nearby
            phone.color_match_wait_click(503, 1587, 114, 215, 156)
            sleep(2)
            # first route
            phone.tap_screen(300, 1600)
            phone.color_match_wait(338, 1533, 114, 215, 156, threashold=20)
            sleep(0.5)
            phone.tap_screen(338, 1533)
            sleep(1)
            phone.tap_screen(373, 1950)
            timeout = 300
            while not phone.color_match(960, 1617, 255, 142, 142) \
                    and timeout > 0:
                timeout -= 1
                if phone.color_match(960, 1617, 255, 142, 142):
                    quit_route(phone)
                       
                if phone.color_match(904, 1542, 255, 158, 0) or timeout == 0:
                    end_route(phone)
                    break
                phone.egg_handle()
                sleep(2)
                
            
        except:
            print("Something went wrong ignore")
            sleep(10)
        

    
       
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()

    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    route(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
