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
from pokelib import TouchScreen, ocr
from pokelib import ExPokeLibFatal
from pokelib import ScreenRegion
from pokelib import TextFlat

import json
import sys
from datetime import datetime
from _operator import truediv


from concurrent.futures import ThreadPoolExecutor

from regex import F

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

def trade(jsonFile):
    with open(jsonFile, 'r') as file:
        parameter = json.load(file)
        
    print("Paramter : {}".format(parameter))
    print("Mode {}".format(parameter["mode"]))
    if parameter["mode"] != "trade":
        print("Unsupported {}".format(parameter["mode"]))
        return
    
    print("start trading")
    host = TouchScreen(parameter["host"]["port"], name = parameter["host"]["name"])
    guest = TouchScreen(parameter["guest"]["port"], name = parameter["guest"]["name"])
    guest.buttons.t_friend_trade.search(retries=1)
    guest.buttons.t_friend_trade.search(retries=1)
    guest.buttons.t_friend_trade.search(retries=1)
    global trade_started
    trade_started = {
        parameter["host"]["name"]: False,
        parameter["guest"]["name"]: False
    }
    tradesDone = 1
    # start_trade(guest, parameter["host"]["name"], parameter["host"]["filter"])

    while True:
        tradeing = False
        try:
            with ThreadPoolExecutor(max_workers=2) as executor:
                trade_host = executor.submit(start_trade,
                                          host,                                          
                                          parameter["guest"]["name"],
                                          parameter["host"]["filter"])
                trade_guest = executor.submit(start_trade,
                                          guest,
                                          parameter["host"]["name"],
                                          parameter["guest"]["filter"])

                # Wait for both to finish (and propagate exceptions)
                trade_host.result()
                trade_guest.result()

            # time.sleep(2)
            retry = 0

            tradeing = True
    
            # traded_pokemon(host)

            log.info("Time : Trading loop starts {}".format(host.getTimeNow()))
            while True:
                with ThreadPoolExecutor(max_workers=2) as executor:
                    trade_h = executor.submit(trade_pokemon,
                                                host, parameter["host"]["name"])

                    trade_g = executor.submit(trade_pokemon,
                                                guest, parameter["guest"]["name"])
                    # Wait for both to finish (and propagate exceptions)
                    trade_h.result()
                    trade_g.result()
                pass



        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)

        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)
            trade_host.cancel()
            trade_guest.cancel()
            if tradeing:
                trade_h.cancel()
                trade_g.cancel()

def search_and_press(button):
    print(f'Searching for button {button.ts.url}')
    # wait until button is found and press it
    if button.search(retries=30) is None:
        raise Exception("Button not found")
    # press it until button is not found anymore
    counter = 0
    while button.press(retries=1):
        counter += 1
        if counter > 230:
            raise Exception("Button still there after 20 retries")
        print(f'Button pressed address {button.ts.url} counter {counter}')
        sleep(1)

def trade_pokemon(p, trainer):
    # Initialize the attribute if it doesn't exist yet
    retries = 35
    print(f'{trainer} - waiting for trade to start {retries}')
    while not p.ocr.regex('POK.MON', 
                      ScreenRegion(p, ye=p.rel_y(0.25)),
                      retries=1, pause=1):
        print(f'{trainer} - waiting for trade to start {retries}')
        p.buttons.t_friend_trade.press(retries=1)
        if retries <= 0:
            raise Exception(f"{trainer} - Trade not started yet")
        retries += 1
        sleep(0.75)
    print(f'{trainer} - pokemon screen found')
    trade_started[trainer] = True
    retries=20
    while p.ocr.regex('POK.MON', 
                      ScreenRegion(p, ye=p.rel_y(0.12)),
                      retries=1, pause=1):
        print(f'{trainer} - select first pokemon retries {retries}')
        p.pokemon_select_first(verbose=0)
        retries -= 1
        if retries == 0:
            raise Exception(f"{trainer} - Could not select first pokemon after 20 retries")
        sleep(1)
    print(f'{trainer} - press next')
    # p.buttons.b_trade_next.press(retries=50)
    search_and_press(p.buttons.b_trade_next)
    print(f'{trainer} - confirm')
    # p.buttons.t_trade_confirm.press(retries=50)
    search_and_press(p.buttons.t_trade_confirm)
    print(f'{trainer} - wait for pokemon received')
    p.buttons.i_exits.press(retries=30)
    print(f'{trainer} - pokemon received exit pressed')

def start_trade(p, trainer, filter):
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
    t_no_case = re.compile(trainer, re.I)
    t = p.ocr.regex(t_no_case, find_all=True)
    p.tap_screen(t[1]['center'], scale=False)
    sleep(2)
    def wait_4_trade_callback():
        has_gift = p.buttons.b_open_gift.search()
        if has_gift:
            p.tap_screen(100,100, button=3)
    sleep(1)
    b = p.buttons.t_friend_trade.press(retries=20, 
                                        retry_callback=wait_4_trade_callback)
    b = p.buttons.t_friend_trade.press(retries=20)
    
    but = TextFlat(ScreenRegion(p,
                    ye=p.rel_y(0.40)),
                    'Search')
    
    for i in range(5):
        if but.press(retries=1, verbose=0):
            break
        elif p.buttons.i_pokemon_search.press():
            break

    sleep(1)

    p.text_line_ok(f'\\a{filter}')
    sleep(.5)
    p.text_line_ok(f' \\n')
    print(f'{trainer} - ready for trading')
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
    trade(args.json)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    