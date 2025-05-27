#!/bin/env python
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import ExPokeNoHomeError
from pokelib import PokeArgs

import defeat_gym

import json
import sys
from datetime import datetime
from catch import catch

def rotate(angle = 40):
    print("Rotate {}", angle)
    sleep(1)
    p.scroll(angle * 10, 0, start_y=680, start_x = 500, stop_to=0.1)
        
def search_pokemon():
    while True:   
        # for y in range(1300, 600, -50):
        for y in range(1300, 800, -50):
        # for y in range(1300, 1049, -50):
            p.color_show(500, y)
            p.tap_screen(500, y)
            sleep(0.25)
            if not p.is_home():
                print("Not home")
                sleep(3)
                if p.screen_is_catch_pokemon():
                    print("Pokemon screen")
                    # p.screen_go_to_home()
                    return True
                if p.screen_is_pokestop() == "stop_and_spin" and args.spin:
                    p.spin_disk()
                    p.screen_go_to_home()
                if p.screen_gym_need_defeat() and False:
                    defeat_gym.defeat(args.port, args.phone)
                    heal.heal(args.port, args.phone)
                    p.screen_go_to_home()
                else:
                    print("Something else")
                    p.screen_go_to_home()
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
        p.screen_go_to_home()
        p.screen_go_to_home()
        if search_pokemon():
            # if not action(port, p, distance = 6, berry = "a", max_tries = 5, span = 3):
            if not catch(port, p, distance = 6, berry = "a", max_tries = 7, span = 2):
                # turn away if no action !!!
                rotate(90)
    
   
    
def main():

    parser = PokeArgs()
    parser.add_argument("-b", "--berry", action="store", required=False, default="a", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("-d", "--span", action="store", required=False, default=0, \
                        help="Vary distance by span.")
    parser.add_argument("-s", "--spin", action="store", required=False, default=False, \
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
