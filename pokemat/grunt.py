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
                if "BATTLE" in phone.pocr_read_line_center((444, 1464), (300, 120)):
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
        start, _ = phone.pocr_find_regex('USE THIS.*')
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

def prepare_battle(phone):
    if not select_team(phone):
        return False

    # try:
    #     phone.color_match_wait_click(338, 1779, 162, 220, 148, threashold=20, time_out_ms = 15500)
    # except:
    #     pass
    # watch_dog.reset()

    startTime = datetime.now()
    while not phone.black_screen():
        if ((datetime.now() - startTime).total_seconds() * 1000) > 10000:
            break
        print("Wait black screen")
        time.sleep(0.05)
    while phone.black_screen():
        if ((datetime.now() - startTime).total_seconds() * 1000) > 3000:
            break
        print("Wait black screen")
        time.sleep(0.05)
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
    
def grunt(port):
    print("Looking for grunt \"{}\" on port {}", port)
    phone = TouchScreen(port)
    try:
        phone.screen_go_to_home()
    except:
        pass
    # phone.dno_gruntoBattle()
    if args.autoconnect:
        connect(phone, del_balls=args.delete_balls)    
    no_grunt = False
    no_grunt = True
    while no_grunt:
        # rotate(phone)
        # if is_red_in_the_sky(phone):
        #     no_grunt = False
        no_grunt = scan_sky(phone, print, no_grunt)
        if not no_grunt:
            time.sleep(1)
            if is_grunt_in_gym(phone):
                no_grunt = False
        else:
            phone.screen_go_to_home()
            rotate(phone)

    try:
        phone.color_match_wait_click(463, 855, 203, 79, 41, time_out_ms = 1500)
    except:
        pass
    time.sleep(1)
    oponent = False
    try:
        i = 4
        no_grunt = True
        go_out = 2
        while i > 0:
            i = i -1
            print("Wait opponent and spin{}".format(i))

            phone.spin_disk()
            phone.tap_screen(498, 1824)
            sleep(3)
            print("after sleep")
            if phone.color_match(506, 849, 206, 92, 51, threashold = 20) or \
                   phone.color_match(506, 880, 206, 92, 51, threashold = 20) or \
                   phone.color_match(611, 880, 206, 92, 51, threashold = 20) or \
                   phone.color_match(620, 880, 206, 92, 51, threashold = 20):
                phone.tap_screen(506, 849)
                oponent = True
                print("Opponent found")
                i = 0
                break
            if phone.color_match(498, 1824, 235, 242, 242):
                phone.tap_screen(498, 1824)
            if phone.is_home():
                print("Is home")
                i = 0
        print("oponent {}".format(oponent))
        if not oponent:
            print("No opponent found")
    except Exception as e:
        print(e)
        pass
    print("Wait battle")

    i = 10
    start_grunt = False
    while i > 0:
        try:
            print("Wait for battle")
            battle, fs = phone.pocr_find_regex('BATTLE')
            if battle:
                g, fs = phone.pocr_find_regex('Grunt')
                if g:
                    print("Set start grunt to True")
                    start_grunt = True
                    i = 0
                    break
            phone.tap_screen(348, 1000)
            sleep(0.5)
            i -= 1
            
            # phone.color_match_wait_click(348, 1554, 151, 217, 149, threashold=20, time_out_ms = 1000)
        except:
            i = i -1
    if start_grunt:
        phone.tap_screen(battle['center'], scale=False)
        sleep(0.5)
        phone.tap_screen(battle['center'], scale=False)
        prepare_battle(phone)

        phone.screen_go_to_home()
        phone.screen_go_to_home()
        phone.heal_all()

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
            print("Upps something went wrong but who cares?: {}", e)    # ts.click(200,200)
    print("end")
    watch_dog.kill()
    # ts.click(200,y)
if __name__ == "__main__":
    main()
