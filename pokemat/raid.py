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
    if args.now:
        print('Start battle now')
        _battle_raid(phone)
    reg1 = ScreenRegion(phone) #, xs=phone.rel_y(0.5), ye=phone.rel_y(0.5))
    # fp = phone.ocr.regex('FREE', reg1)
    fp = phone.ocr.regex('(FREE|RAID|PASS)', reg1)
    if fp:
        phone.tap_screen(phone.rel_x(0.5), phone.rel_y(0.5), scale=False)

    reg = ScreenRegion(phone, ys=phone.rel_y(0.5))

    for i in range(16):
        b = phone.buttons.i_raid_battle.press(retries=1)
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
    _battle_raid(phone)

def _battle_raid(p):
    while not p.buttons.t_raid_summary.search(retries=1):
        y1 = p.rel_y(0.88)
        y2 = p.rel_y(0.9)
        try:
            rejoin=0
                
            for x in [p.rel_x(0.2), p.rel_x(0.5), p.rel_x(0.7)]:
                print(f'TAP x{x} y{y1}')
                p.tap_screen(x, y1, scale=False)
                time.sleep(0.04)
                # p.tap_screen(x, y2, scale=False)
                time.sleep(0.04)
                # if rejoin % 5 == 0:
                #    p.buttons.b_raid_rejoin.press()
                rejoin += 1
                # phone.atchColor(321, 1005, 160, 219, 147)
        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)
            
       
def main():

    parser = PokeArgs()
    global args
    parser.add_argument("-n", "--now", action='store_true', \
                        help="Start battle immediatly")
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
