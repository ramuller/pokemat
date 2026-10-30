#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
from pokelib import CButtAutoCatchConnect, CButtAutoCatchPair

import json
import sys
from datetime import datetime
# from delete_balls import delete_red_balls

def deleteRedBalls(phone):
    phone.screen_go_to_home()
    phone.tap_screen()

def connect(phone, del_balls=False):
    try:
        # Retry because there might be some berries in the view
        status = phone.buttons.i_autocatch.search(retries=5)
        if not status:
            print('STATUS : Icon not found status unkown')
            return False
        if status.icon_name == 'on':
            print(f'STATUS : Connected, nothing to do')
            return True

        print('STATUS : No connection, try to connect')
      
        try:
            if args.delete_balls:
                delete_red_balls(phone)
                delete_red_balls(phone)
                delete_red_balls(phone)
        except:
            try:
                if del_balls:
                    delete_red_balls(phone)
                    delete_red_balls(phone)
                    delete_red_balls(phone)
            except:
                pass
        but = phone.buttons.i_autocatch.press(retries=5)
        if not but:
            print('ERROR : button not found')
        
        if CButtAutoCatchConnect(phone).press(retries=45) is not None:
            ret = CButtAutoCatchPair(phone).press(retries=30)
            if ret is not None:
                return True
        return False
    except Exception as e:
        print("Upps something went wrong but who cares?: {}", e)
        return False
            
def reconnect(port):
    print("Start reconnect on port {}", port)
    phone = TouchScreen(port)
    while True:
        connect(phone)
        time.sleep(20)
        phone.egg_handle()
        

def main():

    parser = PokeArgs()
    parser.add_argument("-d", "--delete-balls", action='store_true', required=False, default=False, \
                        help="Delete all red balls before connect")    
    
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    reconnect(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
