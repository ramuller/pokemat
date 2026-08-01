#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

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
            print(f'STATUS : Connection on, nothing to do')

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
            return False
        for i in range(30):
            if status.icon_name == 'on':
                print('STATUS : connected')
                return True
            text, reg = phone.ocr.read_and_npa()
            res =  phone.ocr.regex('.*connect', 
                                   reg=reg,
                                   update_npa=False)
            if res:
                print('STATUS : connect found')
                phone.tap_screen(res['center'])
                for i in range(30):
                    res =  phone.ocr.regex('.*connect')
                    if not res:
                        break
            sleep(1)

        for i in range(30):
            if status.icon_name == 'on':
                print('STATUS : connected')
                return True
            text, reg = phone.ocr.read_and_npa()
            res =  phone.ocr.regex('Pair', 
                                   reg=reg,
                                   update_npa=False)
            if res:
                print('STATUS : Pair found')
                phone.tap_screen(res['center'])
                break
            sleep(1)
        print('STATUS: Assuming connection is comming up')
        return True




        return True
    except Exception as e:
        print("Upps something went wrong but who cares?: {}", e)
        return False
            
def reconnect(port):
    print("Start reconnect on port {}", port)
    phone = TouchScreen(port)
    while True:
        connect(phone)
        time.sleep(60)
        
   


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
