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

def deleteRedBalls(phone):
    phone.screen_go_to_home()
    phone.tap_screen()

def reconnect(port):
    print("Start reconnect on port {}", port)
    phone = TouchScreen(port)
   
    while True:
        try:
            # phone.tap_screen(119, 1791) # Avatar
            phone.tap_screen(90, 30) # Clock
            time.sleep(2)
            phone.screen_go_to_home()
            print("Check connection status")
            phone.color_match_wait_click(914, 585, 149, 97, 121, time_out_ms=20000)
            print("Color match")
            time.sleep(1)
            phone.color_match_wait(114, 136, 45, 49, 50, time_out_ms=30000)
            print("Connect screen detected")
            for x in range(230, 280, 4):
                r, g, b = phone.getRGB(x, 369)
                print("X {},{},{},{}".format(x, r, g ,b))
            # phone.color_match_wait_click(241, 369, 143, 208, 218)
            time.sleep(1)
            print("TAP connect")
            phone.tap_screen(241, 369)
            phone.color_match_wait(251, 1205, 66, 66, 66)
            time.sleep(1)
            print("TAP pair")
            phone.tap_screen(828, 1177)
            # phone.color_match_wait_click(807, 1189, 29, 88, 102)
            print("Wait a minute to get the connection up!")
            for i in range(0,10):
                time.sleep(6)
                if phone.color_match(914, 582, 255, 1, 0):
                    break
            time.sleep(180)
        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)
            
       
def main():

    parser = PokeArgs()
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
