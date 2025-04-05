#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import ExPokeNoHomeError
from catch import catch 

import json
import sys
from datetime import datetime

def rotate(angle = 40):
    print("Rotate {}", angle)
    sleep(1)
    p.scroll(angle * 10, 0, start_y=680, start_x = 500, stop_to=0.1)
        
def search_pokemon():
    while True:   
        # for y in range(1300, 600, -50):
        for y in range(1300, 800, -50):
        # for y in range(1300, 1049, -50):
            p.showColor(500, y)
            p.tap_screen(500, y)
            sleep(0.25)
            if not p.is_home():
                print("Not home")
                sleep(3)
                if p.screen_is_catch_pokemon():
                    print("Pokemon screen")
                    # p.goHome()
                    return True
                if p.screen_is_pokestop() and args.spin:
                    # p.spin_disk()
                    p.goHome()
                else:
                    print("Something else")
                    p.goHome()
                rotate()
        rotate()
            

def autocatch(port, phone_model):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Change trainers \"{}\" on port {}", phone_model, port)
    global p
    p = TouchScreen(port, phone_model)
    while True:
        not_home = True
        p.goHome()
        p.goHome()
        if search_pokemon():
            # if not catch(port, p, distance = 6, berry = "a", max_tries = 5, span = 3):
            if not catch(port, p, distance = 4, berry = "a", max_tries = 6, span = 4):
                # turn away if no catch !!!
                rotate(90)
    
   
    
def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("-s", "--spin", action="store", required=False, default=True, \
                        help="Spin pokestops")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    while True:
        try:
            autocatch(args.port, args.phone)
        except ExPokeNoHomeError as e:
            print("Problems to find home...")
            pass
        
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
