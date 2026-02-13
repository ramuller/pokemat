#!/bin/env python
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

def wait_raid_start(p, start=True):
    startTime = datetime.now()
    while  (datetime.now() - startTime).total_seconds() < 120:
        reg = ScreenRegion(p, ye=p.rel_y(0.15))
        lines = p.ocr.read(reg)
        print(lines)
        for l in lines:
            if start:
                if not l['text'] in ['QUIT','ITEMS', 'GROUP','CODE']:
                    return True
            else:
                if l['text'] in ['QUIT','ITEMS', 'GROUP','CODE']:
                    return True
        sleep(3)

def raid(port):
    print("Start raid on port {}", port)
    phone = TouchScreen(port)
    b = phone.buttons.dark('.*BATTLE.*', retries=10)
    if not b:
        b = phone.buttons.i_exits.press()
        if b:
            sleep(1)
    # b = phone.buttons.dark('BATTLE')
    sleep(2.5)
    # for y in range(phone.rel_y(0.5), phone.rel_y(0.8), phone.rel_y(0.05)):
    #    print(y)
    #     sleep(0.1)
    #    phone.tap_screen(phone.rel_x(0.5), y, scale=False)
    # while phone.color_match(368, 203, 16, 146, 175):
    #     print("Wait for start")
    
    wait_raid_start(phone, start=False)
    wait_raid_start(phone)
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
    raid(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
