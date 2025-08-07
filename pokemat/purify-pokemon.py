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
            phone.tap_screen(189, 792)
            print("Click menu")
            phone.color_match_wait_click(366, 1775, 232, 128, 181)
            sleep(0.5)
            time.sleep(2)             
            phone.color_match_wait_click(333, 1146, 151, 217, 147)
            sleep(12)
            print("Ready")
            phone.color_match_wait_click(505, 1880, 28, 135, 149)
            sleep(3)
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
    