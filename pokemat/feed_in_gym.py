#!/bin/env python
import time
import random
from time import sleep
import os
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
import logging

import json
import sys
from datetime import datetime


def heal(port):

    print("Feed in gym {}", port)
    global phone
    phone = TouchScreen(port)
    while True:
        f = random.uniform(0.01, 0.99)
        x = phone.rel_x(f)
        print(f'Select pomon X:{x}  f{f}')
        phone.tap_screen(x, 
                        phone.rel_y(0.62),
                        scale=False)
        sleep(1)
        phone.tap_screen(phone.rel_x(0.5), 
                      phone.rel_y(0.8),
                      scale=False)
        if not phone.buttons.i_gym_photo_disk.search(retries=1):
            phone.buttons.i_exits.press()
        sleep(1)
    # time.sleep(1)
    # phone.heal_all()
   
    
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    # global args
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    heal(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
