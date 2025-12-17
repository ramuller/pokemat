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
    phone.tap_screen(916, 1552)
    sleep(0.75)
    for i in range(3):
        phone.scroll(0, -1800, start_x=900, start_y=1900)
        sleep(0.5)
    
    phone.tap_screen(491, 1458)
    sleep(2)
    phone.tap_screen(491, 1458)
    
def end_route(phone):
    print("End route!!!")
    phone.tap_screen(920, 1552)
    sleep(1)
    phone.tap_screen(920, 1552)    
    sleep(1)
    regex = ".*COMPLETE.*"
    # regex = ".*"
    t, _ = phone.pocr.find_regex(regex)
    if t:
        phone.tap_screen(t['center'], scale=False)
    else:
        return False
            
    sleep(1)
    if phone.color_match(390, 1046, 141, 218, 151):
        phone.tap_screen(390, 1046)
        sleep(0.5)    

    # t, _ = phone.pocr.find_regex('YES')
    # if t:
    #     phone.tap_screen(t['center'], scale=False)
    
    for i in range(18):
        phone.tap_screen(15, 100)
        sleep(0.5)
    return True

def screen_go_overview(phone):
    t, _ = phone.pocr.find_regex('.*RSVP.*')
    if t:
        return 0
    phone.screen_go_to_home()
    sleep(0.75)
    phone.tap_screen(900, 1850)
    sleep(0.75)


def follow_route(phone):
    screen_go_overview(phone)
    t, _ = phone.pocr.find_regex('.*ROUTE.*')
    phone.tap_screen(t['center'], scale=False)
    sleep(1)

    start = (0, phone.specs['h']//2)
    start = (0, 765)
    size = (phone.specs ['w'], 200)
    t, _ = phone.pocr.find_regex('.*NEARBY.*', start, size)
    phone.tap_screen(t['center'], scale=False)    
    sleep(1)
        
    t, _ = phone.pocr.find_regex('.*min.*', start, size)
    phone.tap_screen(t['center'], scale=False)    
    sleep(2)    
     
    if phone.color_match(385, 1556, 111, 211, 143):
        phone.tap_screen(385, 1556)
        sleep(0.5)
        phone.tap_screen(385, 1556)
        sleep(1.5)
    # t, _ = phone.pocr.find_regex('.*FOLLOW.*', verbose=1)
    # phone.tap_screen(t['center'], scale=False)    
    # sleep(1)    
    phone.tap_screen(15, 100)
    sleep(1.3)    

    phone.screen_go_to_home()

def route(port):
    print("Start on port {}", port)
    phone = TouchScreen(port)
    # quit_route(phone)
    # end_route(phone)
    # select route
    phone.screen_go_to_home()
    timeout = 1
    follow = False
    while True:
        try:
            while not phone.color_match(960, 1617, 255, 142, 142) \
                    and timeout > 0:

                if (phone.color_match(895, 1535, 255, 255, 255) and phone.color_match(947, 1576, 255, 255, 255) \
                                    and follow == False) or timeout == 0:
                    quit_route(phone)
                    follow = False
                    timeout = 0
                    break                       
                if phone.color_match(904, 1542, 255, 158, 0) or timeout == 0:
                    end_route(phone)
                    timeout = 0
                    follow = False
                    break
                phone.egg_handle()
                sleep(2)
                timeout -= 2
            phone.screen_go_to_home()
            follow_route(phone)
            follow = True
            timeout = 300
                
            
        except Exception as e:
            print(e, traceback.format_exc())
            print("Something went wrong ignore")
            sleep(10)
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
