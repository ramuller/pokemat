#!/bin/env python
import argparse
import threading
import time
from time import sleep
import os
import logging
import random

from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import WatchDog
from pokelib import PokeArgs
from pokelib import ScreenRegion
from pokelib import IconButton, StdButtons

from catch import catch
from reconnect import connect

import json
import sys
from sys import exit
from datetime import datetime

def is_grunt_in_gym(p):

    if True \
        and p.color_match(861, 1850, 194, 150, 253) \
        and p.color_match(67, 1850, 194, 150, 253):
        return True
    if True \
        and p.color_match(861, 1917, 61, 64, 63) \
        and p.color_match(67, 1925, 61, 64, 63):
        return True
    if True \
        and p.color_match(902, 1949, 147, 100, 232) \
        and p.color_match(450, 1949, 147, 100, 232) \
        and p.color_match(100, 1949, 147, 100, 232):
        return True
    if p.color_match(585, 826, 211, 90, 49) \
            and p.color_match(659, 830, 209, 88, 47) \
            and p.color_match(614, 876, 205, 88, 50) \
            and p.color_match(555, 871, 205, 88, 50):
        return True
    if True \
            and p.color_match(41, 1802, 48, 50, 52) \
            and p.color_match(975, 1763, 48, 50, 52) \
            and p.color_match(375, 1859, 255, 147, 113):
        return True
    if True \
            and p.color_match(46, 1816, 78, 78, 80) \
            and p.color_match(950, 1816, 78, 78, 80) \
            and p.color_match(762, 1880, 78, 78, 80):
        return True
    if True \
            and p.color_match(46, 1816, 48, 51, 50) \
            and p.color_match(950, 1816, 48, 51, 50) \
            and p.color_match(762, 1880, 48, 51, 50):
        return True
    if True \
            and p.color_match(50, 1837, 31, 132, 241) \
            and p.color_match(951, 1792, 31, 132, 241) \
            and p.color_match(500, 1330, 40, 174, 247):
        return True
    if True \
            and p.color_match(39, 1875, 31, 106, 222) \
            and p.color_match(489, 1951, 31, 106, 222) \
            and p.color_match(946, 1810, 31, 106, 222):
        return True
        

    if p.color_match(62, 1601, 222, 145, 255):
        return True

    if True \
            and p.color_match(468, 804, 212, 91, 50) \
            and p.color_match(529, 855, 206, 90, 49) \
            and p.color_match(463, 871, 203, 89, 50):
        return True
    if True \
            and p.color_match(404, 857, 206, 90, 49) \
            and p.color_match(418, 814, 211, 90, 49):
        return True

    if True \
            and p.color_match(404, 857, 206, 90, 49) \
            and p.color_match(418, 814, 211, 90, 49):
        return True
    if True \
            and p.color_match(390, 814, 206, 90, 49) \
            and p.color_match(390, 857, 206, 90, 49) \
            and p.color_match(390, 900, 205, 80, 49)\
            :
        return True

    # print("No grunt")
    return False

def is_red_in_the_sky(p):
    if p.color_match(465, 394, 155, 64, 61):
        print("bingo")
        sys.exit(0)

def rotate(phone):
    phone.scroll(0, 800, start_y=200, start_x = 980, stop_to=0.1)
    phone.scroll(0, 800, start_y=200, start_x = 980, stop_to=0.1)
    # phone.scroll(0, 800, start_y=200, start_x = 980, stop_to=0.1)


def scan_sky(phone, print, no_grunt):
    
    phone.screen_go_to_home()
    gy = 400
    while gy < 880 and no_grunt:
        x = 100
        while x < 900 and no_grunt:
        # if phone.color_match(x, gy, 73, 73, 75):
            if phone.color_match(x, gy, 166, 73, 66) \
                    or phone.color_match(x, gy, 152, 60, 60) \
                    or phone.color_match(x, gy, 180, 90, 70) \
                    or phone.color_match(x, gy, 225, 130, 115) \
                    or phone.color_match(x, gy, 192, 99, 82) \
                    or phone.color_match(482, 582, 209, 127, 114):
                print("Grunt R found")
                for i in range(3):
                    y = gy + random.randrange(100, 201)
                    phone.tap_screen(x, y)
                    sleep(0.1)
                time.sleep(4)
                no_grunt = False
            if is_grunt_in_gym(phone) \
                    or phone.color_match(868, 197, 241, 247, 240) \
                    or phone.color_match(506, 849, 206, 92, 51):
                if "BATTLE" in phone.ocr_read_line_center((444, 1464), (300, 120)):
                    print("Max battle or so")
                    continue
                no_grunt = False
            x = x + 35
        print("Search grunt {}, {}".format(x, gy))
        watch_dog.reset()
        gy = gy + 20

    return no_grunt


def select_team(phone):    
    start = None
    for i in range(15):
        start, _ = phone.ocr_find_regex('USE THIS.*')
        print(f"Start {start}")
        if start:
            watch_dog.reset()
            print("Found grunt")
            # sleep(1)
            break
        sleep(1)
    if start: 

        phone.tap_screen(970, 1452)
        time.sleep(2)
        phone.tap_screen(start['center'], scale=False)
        print("Wait go battle")
    return start

def start_battle(phone):
    startTime = datetime.now()
    # while not phone.black_screen():
    #     if ((datetime.now() - startTime).total_seconds() * 1000) > 10000:
    #         break
    #     print("Wait black screen")
    #     time.sleep(0.05)
    # while phone.black_screen():
    #     if ((datetime.now() - startTime).total_seconds() * 1000) > 3000:
    #         break
    #     print("Wait black screen")
    #     time.sleep(0.05)
    print("do battle")
    phone.doBattle()

    # Wait for trainer
    for i in range(1,10):
        try:
            phone.color_match_wait_click(305, 1773, 137, 216, 153, time_out_ms = 2000)
            break
        except:
            print("Wait for rescue")
            phone.tap_screen(305, 773)
        pass
    phone.tap_screen(512, 873)

    sleep(2)
    print("Try to catch")    
    watch_dog.reset()
    catch(phone, distance = 6, max_tries = 12, span = 2)
    watch_dog.reset()
    # action(port, phone, berry = "g")
    print("Try to action")
    
def find_grunt(phone):
    reg = ScreenRegion(phone, color='rgb', ye=phone.rel_y(0.5))
    bw_reg = ScreenRegion(phone, color='rgb', ye=phone.rel_y(0.5))
    reg.npa = phone.image.scan_region(reg)
    for r in range(250, 100, -10):
        g = r * 120 // 200
        b = r * 100 // 200
        # g = b = r
        vf  = f'r{r}-g{g}-b{b}'
        print(vf)
        bw_reg.npa = phone.image.find_rgb(reg, r, g, b, wait=1, verbose=0, tolerance=15)
        b = IconButton(bw_reg, 'grunt_r')

        det = b.search(retries=1, no_scan=True, verbose=0)
        print(f'Detextion {det}')
        if det:
            x = det.center[0]
            y = det.center[1]
            y += det.quad[3][1] - det.quad[0][1]
            phone.tap_screen(x, y, scale=False)
            return det
        
    return None

def grunt(port):
    print("Looking for grunt \"{}\" on port {}", port)
    phone = TouchScreen(port)
    phone.screen.go_home()
    try:
        phone.screen_go_to_home()
    except:
        pass
    # phone.dno_gruntoBattle()
    if args.autoconnect:
        connect(phone, del_balls=args.delete_balls)    
    grunt = None
    while not grunt:
        # rotate(phone)
        # if is_red_in_the_sky(phone):
        #     no_grunt = False
        # no_grunt = scan_sky(phone, print, no_grunt)
        grunt = find_grunt(phone)
        if grunt:
            time.sleep(1)
            phone.spin_disk()
            for i in range(30):
                if phone.buttons.t_pokestop_battle.press(retries=1):
                    break
                phone.buttons.i_exits.press()
                phone.tap_screen(phone.rel_x(0.3), phone.rel_y(0.9), scale=False)
                sleep(1.5)

            print('time to battle')


            reg = ScreenRegion(phone, ys=phone.rel_y(0.55))
            sb = StdButtons(reg)

            # def cb():
            #     if phone.ocr.regex('.*Team|Grunt|seeing|many|been.*', reg=reg) \
            #         or phone.buttons.dark('BATTLE', action='check'):
            #         phone.tap_screen(phone.rel_x(.5), phone.rel_y(.5))
            #     return False
            # if not sb.dark('BATTLE', call_back=cb, action='press', retries=30):
            #     return

            if not phone.buttons.t_grunt_party.search(retries=20):
                phone.screen_go_to_home()
                phone.screen_go_to_home()
                break
            phone.tap_screen(phone.rel_x(.98), phone.rel_y(.75), scale=False)
            sleep(1)
            if not phone.buttons.t_grunt_party.press(retries=20):
                phone.screen_go_to_home()
                phone.screen_go_to_home()
                break
            sleep(0.5)
            start_battle(phone)

            phone.screen_go_to_home()
            phone.screen_go_to_home()
            phone.heal_all()

        else:
            phone.screen_go_to_home()
            rotate(phone)



def wd_callback():
    print("Watchdog timeout strike just exit {}".format(threading.main_thread().native_id))
    watch_dog.kill()

def main():
    global watch_dog
    
    parser = PokeArgs()
    parser.add_argument("-a", "--autoconnect", action='store_true', required=False, default=False, \
                        help="Connnect to autocatch.")    
    parser.add_argument("-d", "--delete-balls", action='store_true', required=False, default=False, \
                        help="Delete all red balls before connect")
    global args
    args = parser.parse_args()
    
    global log
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    watch_dog = WatchDog(time_out = 240, _callback = wd_callback)
    while True:
        try:
            grunt(args.port)
        except Exception as e:
            print(f'Upps something went wrong but who cares?: {e}')    # ts.click(200,200)
    print("end")
    watch_dog.kill()
    # ts.click(200,y)
if __name__ == "__main__":
    main()
