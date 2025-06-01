#!/bin/env python
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

def raid(port, phone):
    print("Start evolutions \"{}\" on port {}", phone, port)
    phone = TouchScreen(port, phone)
    phone.tap_screen(650,1500)
    time.sleep(2)
    phone.tap_screen(650,1500)
    time.sleep(8)
    while phone.color_match(368, 203, 16, 146, 175):
        print("Wait for start")
        time.sleep(3)
    print("Raid starts")
    # self.color_match(500, 144, 70, 207, 181)
    while True:
        try:
            for x in range(200,700,150):
                if phone.color_match(333, 1013, 159, 218, 148):
                    phone.tap_screen(333,1013)
                phone.tap_screen(x, 1500)
                time.sleep(0.04)
                if phone.color_match(333, 1013, 159, 218, 148):
                    phone.tap_screen(333,1013)
                phone.tap_screen(x, 1840)
                time.sleep(0.04)
                # phone.atchColor(321, 1005, 160, 219, 147)
        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)
            
       
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()

    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    raid(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
