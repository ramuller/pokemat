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
    
def gifting(port, phone):
    
    can_get_gifts = True
    can_send_gifts = True
    switch_order = False
    daily_limit = False
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)

    # create a list of all random letters
    l_and_d =  string.ascii_lowercase + string.digits
    shuffled_letters = random.sample(l_and_d, len(l_and_d))

        
    print("Start gifting using phone \"{}\" on port {}", phone, port)
    phone = TouchScreen(port, phone)
    phone.friendSortCanReceive()
    # phone.tapSearch()
    # phone.tap_screen(440, 837)
    # phone.tap_screen(440, 1150)
    giftsSent = 0
    giftsReceived = 0
    while can_send_gifts:
        log.info("Time : Send gifts {}".format(phone.getTimeNow()))
        try:
            # Wait for trainer screen
            for timeout in reversed(range(0,100)):
                if phone.color_match(444, 494, 255, 255, 255) and \
                   phone.color_match(812, 1851, 28, 135, 149):
                    break
                time.sleep(0.1)
            if timeout == 0:
                print("Wait for trainer screen : Timeout exit")
                return True
            print("trainer screen")
            while phone.color_match(52, 1335, 255, 255, 255):
                phone.tap_screen(612, 494)
                time.sleep(0.3)
            time.sleep(1)
            phone.selectAll()
            phone.typeString("\b")
            phone.typeString("!ff & !lucky")
            time.sleep(1)
            phone.tapTextOK()      
            time.sleep(0.3)
            # time.sleep(2)
            
            if phone.color_match(359, 884, 250,250,250):
                # can_send_gifts = phone.sendGift(has_gift = False)
                has_gift = False
            else:
                has_gift = True
                # can_send_gifts = phone.sendGift(has_gift = True)
                
            phone.selectFirstFriend()
            can_send_gifts = phone.sendGift(has_gift = has_gift)
            phone.tap_back()

                    
                
            # self.color_match_wait(161, 808, 246, 246, 246, match=False)
        except ExPokeLibFatal as e:
            log.fatal("Unrecoverable situation. Give up")
            sys.exit(1)
        
        # except Exception as e:
        #    print("Upps something went wrong but who cares?: {}", e)
    return False

def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("gifting")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    gifting(args.port, args.phone)
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
    