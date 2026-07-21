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
import re
import logging
from keyboard import press
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import ScreenRegion
from pokelib import TextFlat

import json
import sys
from datetime import datetime
from _operator import truediv

from concurrent.futures import ThreadPoolExecutor

global log

def tradeeeeeeee(host, guest):
    host.useThisParty()
    guest.useThisParty()
    
    while True:
        host.click(331, 1697)
        guest.click(331, 1697)
        for i in range(0,5):
            if host.color_match(100, 100, 0, 0, 0):
                log.info("Battle has ended")
                return True
            time.sleep(0.2)
    
def trainer_battle(jsonFile):
    with open(jsonFile, 'r') as file:
        parameter = json.load(file)
        
    print("Paramter : {}".format(parameter))
    print("Mode {}".format(parameter["mode"]))
    if parameter["mode"] != "battle-friend":
        print("Unsupported {}".format(parameter["mode"]))
        return
    
    print("start battle-friend mode")
    host = TouchScreen(parameter["host"]["port"], name = parameter["host"]["name"])
    guest = TouchScreen(parameter["guest"]["port"], name = parameter["guest"]["name"])
    tradesDone = 1
    
    while True:
        try:
            guest.screen.go_home()
            start_battle(
                        host, 
                        parameter["guest"]["name"],
                        parameter["league"]
                        )
            guest.buttons.t_friend_lets_battle.press(retries=5)

            if not guest.buttons.t_grunt_party.press(retries=15):
                raise 'failed to use party'

            while True:
                battle_start = datetime.now()
                with ThreadPoolExecutor(max_workers=2) as executor:
                    b_h = executor.submit(host.do_battle)
                    b_g = executor.submit(guest.do_battle)

                    r_h = b_h.result()
                    r_g = b_g.result()
                host.tap_screen(10,10,scale=False)
                guest.tap_screen(10,10,scale=False)
                if not host.buttons.b_friend_rematch.press(retries=25) or \
                   not guest.buttons.b_friend_rematch.press(retries=25):
                    raise 'No rematch'

                if not host.buttons.t_grunt_party.press(retries=15):
                    raise 'failed to use party'
                if not guest.buttons.t_grunt_party.press(retries=15):
                    raise 'failed to use party'
                dur = (datetime.now() - battle_start).total_seconds()
                print(f'Battle duration {dur}s')

        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)

        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)

def start_battle(p, trainer, league):
    p.screen.go_home()
    print(f'{trainer} - go friends')
    p.screen.go_friends()
    max_tries = 20
    b = None
    while not b:
        b = p.buttons.i_friends_search.press(retries=1)
        if b:
            break
        p.buttons.t_passenger.press(retries=1)
        sleep(2)
        max_tries -= 1
        if max_tries == 0:
            raise
    time.sleep(2.5)
    print("Friend screen")
    p.text_line_ok(f'\\a{trainer}')
    sleep(1)
    p.text_line_ok(f' \\n')

    sleep(2)
    t_no_case = re.compile(f'.*{trainer}.*', re.I)
    reg = ScreenRegion(p, process=True, blur=3)
    t = p.ocr.regex(t_no_case, reg=reg, find_all=True)
    p.tap_screen(t[1]['center'], scale=False)
    sleep(2)
    def wait_4_callback():
        has_gift = p.buttons.b_open_gift.search()
        if has_gift:
            p.tap_screen(100,100, button=3)
    sleep(1)
    b = p.buttons.t_friend_battle.press(retries=20, 
                                        retry_callback=wait_4_callback)
    b = p.buttons.t_friend_battle.press(retries=1)
    
    t_no_case = re.compile(f'.*{league}.*', re.I)
    but = TextFlat(ScreenRegion(p,
                                process=True),
                                t_no_case)
    
    for i in range(5):
        if but.press(retries=2, verbose=0):
            break

    sleep(1)

    p.buttons.t_friend_lets_battle.press(retries=5)

    p.buttons.t_grunt_party.press(retries=5)

    return True

def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "gifting - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    # parser.add_argument("-p", "--phone", action="store", \
    #                     help="Set phone name default path '/tmp'")
    parser.add_argument("json", help="json file with the battle configuration.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("bf")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    trainer_battle(args.json)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    
