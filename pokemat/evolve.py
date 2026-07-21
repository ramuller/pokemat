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
from pokelib import ScreenRegion


import json
import sys
from datetime import datetime
from _operator import truediv

global log

def empty_search(p):
    if p.ocr.regex('.*Search*.',
        ScreenRegion(p,
            xs=p.rel_x(0.2),
            xe=p.rel_x(0.8),
            ye=p.rel_y(0.3),
            )):
        return True
    return False

def evolve(port, filter):
    
    print("Start evolutions \"{}\" on port {}", port)
    phone = TouchScreen(port)
    # phone.scroll(0, -100)
    # sys.exit(0)
    print(empty_search(phone))
    phone.select_pokemon(filter)
    sleep(2)

    evolve_count = 0
    print("Start time : Evolve {}".format(phone.getTimeNow()))

    while True:
        try:
            if empty_search(phone):
                phone.buttons.i_pokemon_search.press()
                time.sleep(1)
                phone.selectAll()
                phone.send_text_line(f'{filter}')
                sleep(0.5)
                phone.send_text_line(f'\n')
                time.sleep(1)                 
            if not phone.pokemon_select_first(retries=10):
                for i in range(3):
                    print('Try from home, if really no more pokemons for filter "{}" exist, the script will exit'.format(filter))
                    phone.screen.go_home()
                    phone.select_pokemon(filter)
                    if phone.pokemon_select_first(retries=10):
                        sleep(2)
                print("All pokemons for filter '{}' evolved!".format(filter))
                sys.exit(0)
            # if not phone.buttons.i_pokemon_search.press():
            #     print('Unknow situation')
            #     raise('Unknow situation')
            phone.evolve_pokemon()
            evolve_count = evolve_count + 1
            sleep(0.5)
            # phone.screen.go_pokemon()
            print("Time : Evolve {} ".format(phone.getTimeNow()))
            print("Pokemon evolved : {}".format(evolve_count))
        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            # sys.exit(1)

        except Exception as e:
           phone.select_pokemon(filter)
           print("Upps something went wrong but who cares?: {}", e)

def main():

    parser = PokeArgs()
    global args
    parser.add_argument("-f", "--filter", action="store", required=True, \
                        help="Pokemon filter string.")
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    evolve(args.port, args.filter)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    
