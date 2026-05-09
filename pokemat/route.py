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


def _quit_route(phone):
    print("Quit route!!!")
    phone.screen_go_to_home()
    button = phone.buttons.i_route_started.press(retries=3)
    sleep(0.75)
    for i in range(5):
        phone.scroll(0, int(phone.specs['max_y'] * -0.8), 
                     start_x=phone.rel_x(0.1), 
                     start_y=phone.rel_y(0.9), 
                     scale=False)
        # phone.scroll(0, -1800, start_x=900, start_y=1900)
        sleep(0.5)
        if phone.buttons.b_route_quit.press():
            break
    sleep(1)
    phone.buttons.b_route_quit.press()
    sleep(1)

def _end_route(phone):
    print("End route!!!")
    sleep(.5)
    button = phone.buttons.i_route_started.press()
    sleep(.5)
    button = phone.buttons.i_route_started.press()
    button = phone.buttons.b_route_complete.press(retries=5)
    button = phone.buttons.b_yes.press(retries=5)
    sleep(1)    
    for i in range(10):
        phone.tap_screen(15, 100)
        sleep(0.5)
    return True

def screen_go_overview(phone):
    t = phone.ocr.regex('.*RSVP.*')
    if t != []:
        return 0
    phone.screen_go_to_home()
    sleep(0.75)
    phone.tap_screen(phone.rel_x(0.9), 940, scale=False)
    sleep(0.75)


def follow_route(phone):
    if phone.buttons.i_route_pause.search(verbose=0):
        _quit_route(phone)
        phone.screen.go_home()
        sleep(1)
    screen_go_overview(phone)
    phone.buttons.t_overview_route.press(retries=3, delay=1)
    button = phone.buttons.b_route_nearby.press(retries=15, delay=1)
    if not button:
        print("Failed to find NEARBY button")
        # return False
    sleep(1)
    button = phone.buttons.t_route_known.press(retries=5)
    sleep(1.5)
    for i in range(3):
        button = phone.buttons.text_only.press(f'.*{args.route}.*', 
                                        xs=phone.rel_x(0.15),
                                        xe=phone.rel_x(0.75),
                                        ys=phone.rel_y(0.20) + phone.rel_y(0.5 * i),
                                        ye=phone.rel_y(0.97),
                                        process=True
                                        )
        if button:
            break
    button = phone.buttons.b_route_follow.press(retries=6, delay=1)
    if not button:
        print("Failed to find FOLLOW button")
        return False
    sleep(1)
    button = phone.buttons.b_route_follow.search(retries=3)
    if button:
        print(f'Seems we are still in a route {button['text']}')
        return(False)
    # Tap to remove info banner
    phone.tap_screen(15, 100)
    sleep(1)    
    phone.tap_screen(15, 100)
    sleep(1)
    print("Following route")
    return True

def _in_route(phone, retries=1):

    b = phone.buttons.i_route_pause.search(verbose=0, retries=retries)
    if b:
        return 'pause'
    b = phone.buttons.i_route_started.search(verbose=0, retries=retries)
    if b:
        phone.buttons.i_route_started.update_area(b)
        if phone.color_match(b.center[0], b.center[1], 250,250, 250, scale=False):
            return 'in'
        else:
            return 'end'
    
    return 'no_route'

def route(port):
    print("Start on port {}", port)
    phone = TouchScreen(port)
    # quit_route(phone)
    # end_route(phone)
    # select route
    # phone.screen_go_to_home()
    pause = 3
    timeout = 3
    follow = False
    # _end_route(phone)
    _quit_route(phone)
    _in_route(phone, retries=1)
    while True:
        try:
            while _in_route(phone) not in ['end', 'pause' ] \
                    and timeout > 0 and follow:
                timeout -= pause
                print("Following route, time left: {}s".format(timeout))
                screen = phone.ocr.read(verbose=0)
                quit = any(
                    any(word in text.get("text", "") for word in \
                        ["PAUSED", "DISTANCE", "DIRECTION", "paused"])
                    for text in screen
                )
                if quit:
                    follow = False
                if _in_route(phone) == 'in':
                    print('Still in route')
                elif state == 'in' or state == 'pause':
                    _quit_route(phone)
                    follow = False            
                startTime = datetime.now()  
                phone.egg_handle()
                endTime = datetime.now()
                print(f'Time to handle egg: {(endTime - startTime).total_seconds()}')
                sleep(3)

            state = _in_route(phone)
            if state == 'end':
                    _end_route(phone)
            elif state == 'in' or state == 'pause':
                    _quit_route(phone)
                    follow = False
            follow = False
            phone.screen_go_to_home()
            if follow_route(phone):
                follow = True
                timeout = 600
            else:
                phone.screen_go_to_home()
                _quit_route(phone)
            
        except Exception as e:
            print(e, traceback.format_exc())
            print("Something went wrong ignore")
            sleep(600)
            return
        

    
       
def main():

    parser = PokeArgs()
    parser.add_argument("-r", "--route", action='store', 
                        help="Name of the route at least part",
                        default='cross')    
    global args
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
