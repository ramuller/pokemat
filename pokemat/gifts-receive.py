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
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
from pokelib import ScreenRegion

import string
import random

import json
import sys
from datetime import datetime
from _operator import truediv

global log

def battle(host, guest):
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
    
def gifting(port):
    
    can_get_gifts = True
    can_send_gifts = True
    switch_order = False
    daily_limit = False
    # with open("phone-spec.json", 'r') as file:
    #     phones = json.load(file)

    # create a list of all random letters
    l_and_d =  string.ascii_lowercase + string.digits
    shuffled_letters = random.sample(l_and_d, len(l_and_d))

    phone = TouchScreen(port)
    print("Start receiving gifts using port {}", port)
    name = None
    while name == None and False:
        name = phone.get_my_name()
        print(f"My name {name}")
    phone.screen.go_friends()

    giftsSent = 0
    giftsReceived = 0
    receive_gifts = True
    last_tries = 3
    while receive_gifts or True:  # and len(shuffled_letters) > 0:
        try:
            # Wait for trainer screen
            phone.sort_has_gift()
            # phone.screen.go_friends()

            if phone.buttons.i_x_clear_text.press(retries=1):
               sleep(0.5)

            # bt = phone.buttons.i_friends_search.search(retries=1)
            # sleep(0.5)
            if not phone.buttons.i_friends_search.press():
                print('No SEARCH button found')
                # phone.screen.go_home()
                # raise Exception('No SEARCH button found')

            # friends_raw = phone.ocr.read_area_percent(xs=25 ,xe=45 , ys=30 , ye=90)

            # while phone.color_match(52, 1335, 255, 255, 255):
            #     phone.tap_screen(612, 494)
            #     time.sleep(0.3)
            # time.sleep(0.5)
            phone.selectAll()
            phone.text_line_ok("\b")
            if args.all:
                phone.text_line_ok("!ff & !lucky & interactable")
            elif len(shuffled_letters) > 0:
                phone.text_line_ok("!ff & !lucky & {}".format(shuffled_letters[0]))
            else:
                last_tries -= 1
                if last_tries <= 0:
                    phone.screen_go_to_home()
                    sys.exit(0)
                # phone.text_line_ok("!ff & !lucky & interactable")
                phone.text_line_ok("!ff & !lucky")
            time.sleep(0.5)
            phone.text_line_ok('\\n')

            # phone.buttons.t_input_ok.press(verbose=0)
            sleep(0.5)
            g = phone.buttons.i_friends_gift.press()

            if not g and shuffled_letters[0] != " ":
                shuffled_letters.pop(0)
                print("No gift. Letters to go {}".format(len(shuffled_letters)))
            else:
                print("Friend has gift")
                b = phone.buttons.b_open_gift.press(retries=10)

            # Back to friends
            max_tries = 0
            b = phone.buttons.t_friends.search(retries=1)
            while not b:
                phone.buttons.i_exits.press(retries=1)
                sleep(2)
                b = phone.buttons.t_friends.search(retries=1)
                phone.buttons.t_passenger.search(retries=1)
                max_tries += 1
                if max_tries > 30:
                    phone.screen.go_friends()
                    break
            pass
 
                
            # self.color_match(161, 808, 246, 246, 246, match=False)
        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)
        except Exception as e:
            print("Something went wrong, ignore!!! {}".format(e))
         
        print("ca_get {}, can_send {}".format(can_get_gifts, can_send_gifts))
        # except Exception as e:
        #    print("Upps something went wrong but who cares?: {}", e)
    return False

def main():

    parser = PokeArgs()
    global args
    parser.add_argument("-a", "--all", action='store_true', \
                        help="No special filter")
    args = parser.parse_args()
    global log 
    log = logging.getLogger("gifting")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    gifting(args.port)
    go_on = True
    while go_on:
        try:
            go_on = gifting(args.port, args.phone)
        except:
            print("Something went wrong")
            go_on = False
        
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    
