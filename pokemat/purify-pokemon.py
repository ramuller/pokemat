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

def delete_pokemon(port):
    
    can_get_gifts = True
    can_send_gifts = True
    # with open("phone-spec.json", 'r') as file:
    #     phones = json.load(file)
        
    print("Purify on port {}", port)
    phone = TouchScreen(port)
    while True:
        log.info("Time : Send gifts {}".format(phone.getTimeNow()))
        try:
            ys = phone.rel_y(0.30)
            while not phone.buttons.text_only.press('...*', ys=ys):
                sleep(1)

            # phone.tap_screen(189, 792)
            sleep(1)
            sx = int(phone.specs['width'] // 2 )
            sy = int(phone.specs['max_y'] * 0.5)           
            phone.scroll(0, int(phone.specs['max_y'] * -0.2), 
                     start_x=sx, start_y=sy, scale=False)
            sleep(1)
            phone.buttons.b_pomon_purify.press()
            sleep(1)
            phone.buttons.b_yes.press()
            sleep(10)
            for i in range(30):
                r = phone.ocr.regex('.*kg',ScreenRegion(phone, ys=phone.rel_y(0.5)))
                if r:
                    break
                sleep(1)
            phone.buttons.i_exits.press()
            sleep(1.6)
            print("Click menu")

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
    
