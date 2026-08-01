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

global log

def deleteGifts(port):
    
    can_get_gifts = True
    can_send_gifts = True
    print("Delete difts phone port {}", port)
    phone = TouchScreen(port)
    while True:
        log.info("Time : Send gifts {}".format(phone.getTimeNow()))
        try:
            if not phone.buttons.i_gifts_trash.press(retries=10):
                print('No gifts left')
                return
            if not phone.buttons.b_yes.press(retries=10):
                print('dont know where I am')
                return
            
            # sys.exit(0)
        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)

        # except Exception as e:
        #    print("Upps something went wrong but who cares?: {}", e)

def main():

    parser = PokeArgs()
    global args
    parser.add_argument("-a", "--all", action='store_true', \
                        help="No special filter")
    args = parser.parse_args()
    global log 
    log = logging.getLogger("gifting")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    deleteGifts(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    
