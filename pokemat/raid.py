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

def wait_raid_start(p, wait_inside=True):
    startTime = datetime.now()
    while  (datetime.now() - startTime).total_seconds() < 120:
        if p.screen.is_in_lobby() != wait_inside:
            return True
        sleep(3)
    return False

def raid(port):
    print("Start raid on port {}", port)
    phone = TouchScreen(port)
    reg1 = ScreenRegion(phone) #, xs=phone.rel_y(0.5), ye=phone.rel_y(0.5))
    # fp = phone.ocr.regex('FREE', reg1)
    fp = phone.ocr.regex('(FREE|RAID|PASS)', reg1)
    if fp:
        phone.tap_screen(phone.rel_x(0.5), phone.rel_y(0.5), scale=False)

    reg = ScreenRegion(phone, ys=phone.rel_y(0.5))

    for i in range(10):
        b = phone.buttons.t_raid_battle.press(retries=1)
        reg.npa = None
        if b or phone.ocr.regex('RAID', reg):
            sleep(1)
            break
        sleep(1)
    if not b and not phone.ocr.regex('RAID', reg):

        b = phone.buttons.i_exits.press()
        if b:
            sleep(1)
    # b = phone.buttons.dark('BATTLE')
    sleep(2.5)
    for y in range(phone.rel_y(0.5), phone.rel_y(0.8), phone.rel_y(0.05)):
       print(y)
       sleep(0.1)
       phone.tap_screen(phone.rel_x(0.5), y, scale=False)
    # while phone.color_match(368, 203, 16, 146, 175):
    #     print("Wait for start")

    # Wait until in lobby
    wait_raid_start(phone, wait_inside=False)
    wait_raid_start(phone)
    print("Raid starts")

    # self.color_match(500, 144, 70, 207, 181)
    reg = ScreenRegion(phone, ys=phone.rel_y(0.75))
    while not phone.buttons.t_raid_summary('.*SUMMARY.*', reg=reg,
                                 action='check', retries=1):
        reg.npa = None
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
