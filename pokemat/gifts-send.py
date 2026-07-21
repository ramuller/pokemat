#!/bin/env python

# All X/Y coordinates used a virtual playfield of 1000x2000
# Default scaling uses an S7 screen resulution of 576x1024
# paramters scale-x and scale-y can be used to overwrite default
# 139 + testing
# 52
# 74
# dreepy

import time
from time import sleep
import os
import logging
import traceback
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

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

    # create a list of all random letters
    l_and_d =  string.ascii_lowercase + string.digits
    shuffled_letters = random.sample(l_and_d, len(l_and_d))

        
    print("Start gifting using port {}", port)
    phone = TouchScreen(port)
    name = None
    # while name == None:
    #     name = phone.get_my_name()
    #     print(f"My name {name}")    

    # phone.tapSearch()
    # phone.tap_screen(440, 837)
    # phone.tap_screen(440, 1150)
    giftsSent = 0
    giftsReceived = 0
    phone.screen.go_friends()
    while can_send_gifts:
        log.info("Time : Send gifts {}".format(phone.getTimeNow()))
        try:
            # Wait for trainer screen
            phone.sort_send_gift()
            # phone.screen.go_friends()

            if phone.buttons.i_x_clear_text.press(retries=1):
               sleep(0.5)

            if not phone.buttons.i_friends_search.press():
                print('No SEARCH button found')
                phone.screen.go_home()
                raise Exception('No SEARCH button found')

            # friends_raw = phone.ocr.read_area_percent(xs=25 ,xe=45 , ys=30 , ye=90)

            # while phone.color_match(52, 1335, 255, 255, 255):
            #     phone.tap_screen(612, 494)
            #     time.sleep(0.3)
            time.sleep(1.5)
            phone.selectAll()
            phone.text_line_ok("\b")
            # phone.text_line_ok("!ff & !lucky & interactable")
            if args.all:
                phone.text_line_ok('!oksfknds')
            else:
                phone.text_line_ok("!fff")
            time.sleep(0.5)
            phone.text_line_ok('\\n')

            # phone.screen.go_friends()

            if phone.buttons.i_x_clear_text.press(retries=1):
               sleep(0.5)
            sleep(1)
            has_gift = phone.buttons.i_friends_gift.press()
            if not has_gift:
                ra = phone.ratio()
                y = phone.rel_y(0.7 / phone.ratio())
                phone.tap_screen(phone.rel_x(0.5), y, scale=False)
                
            can_send_gifts = phone.gift_send(has_gift = has_gift)
            max_tries = 0
            sleep(1)
            b = phone.buttons.t_friends.search(retries=1)
            while not b:
                phone.buttons.i_exits.press(retries=10)
                sleep(1)
                b = phone.buttons.t_friends.search(retries=1)
                max_tries += 1
                if max_tries > 10 \
                    or phone.screen.get_current_screen() == 'home':
                    phone.screen.go_friends()
                    break
            pass
            # phone.screen.go_friends()

        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)
        except Exception as e:
            traceback.print_exc()
            print(f'ERROR : sendgift {e}')
            phone.screen.go_friends()
        
        # except Exception as e:
        #    print("Upps something went wrong but who cares?: {}", e)
    return True

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
    # gifting(args.port, args.phone)
    go_on = True
    while go_on:
        try:
            go_on = gifting(args.port)
        except:
            print("Something went wrong")
            go_on = False
        
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
    
