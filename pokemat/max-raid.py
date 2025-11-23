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
    # Tap ready
    phone.tap_screen(650,1500)
    time.sleep(2)
    while not "Remaining" in phone.pocr_read_line_center((860, 228), (200, 80)):
        sleep(1)
    print("Raid starts")
    # self.color_match(500, 144, 70, 207, 181)
    while not "SKIP" in phone.pocr_read_line_center((503, 1792), (100, 60)):
        try:
            for x in range(200,700,150):
                phone.tap_screen(x, 1770)
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
