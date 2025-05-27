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
from pokelib import PokeArgs

import json
import sys
from datetime import datetime
from _operator import truediv
from skimage.filters.rank.generic import threshold

global log

def delete_pokemon(port, phone):
    
    can_get_gifts = True
    can_send_gifts = True
    # with open("phone-spec.json", 'r') as file:
    #     phones = json.load(file)
        
    print("Delete difts phone \"{}\" on port {}", phone, port)
    phone = TouchScreen(port, phone)
    while True:
        log.info("Time : Send gifts {}".format(phone.getTimeNow()))
        try:
            phone.pokemon_select_first()
            print("Click menu")
            sleep(0.5)
            phone.color_match_wait_click(866, 1800, 28, 135, 149)
            print("Click transfer")
            sleep(0.5)
            phone.color_match_wait_click(800, 1634, 42, 108, 120)
            sleep(0.5)
            print("Tap transfer")
            phone.color_match_wait_click(637, 1123, 80, 211, 162, threashold=20)
            try:
                phone.color_match_wait_click(368, 1031, 146, 216, 149, time_out_ms = 1500)
            except:
                print("No extra tab")
                pass
            # phone.color_match_wait_click(352, 1044, 150, 218, 149)
            time.sleep(2)             
            print("Ready")
            # sys.exit(0)
        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)

        # except Exception as e:
        #    print("Upps something went wrong but who cares?: {}", e)

def main():


    parser = PokeArgs()
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("gifting")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    delete_pokemon(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    