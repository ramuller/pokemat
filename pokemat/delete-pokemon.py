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
from pokelib import StdButtons

import json
import sys
from datetime import datetime
from _operator import truediv
from skimage.filters.rank.generic import threshold

global log

def delete_pokemon(port):
    
    can_get_gifts = True
    can_send_gifts = True
    # with open("phone-spec.json", 'r') as file:
    #     phones = json.load(file)
        
    print("Delete pokemon  on port {}", port)
    phone = TouchScreen(port)
    while True:
        log.info("Time : Send gifts {}".format(phone.getTimeNow()))
        try:
            phone.pokemon_select_first(retries=3, verbose=0)
            print("Click menu")
            if not phone.buttons.i_pokemon_menu.press(retries=8):
                raise 'No pokemenu found'
            if not phone.buttons.t_pokemon_transfer.press(retries=8):
                raise 'No transfer option'
            if not phone.buttons.b_yes.press(retries=8):
                raise 'No YES button'
            sleep(1)
            phone.buttons.b_yes.press(retries=3)
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
    delete_pokemon(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    