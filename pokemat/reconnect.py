#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal

import json
import sys
from datetime import datetime

def deleteRedBalls(phone):
    phone.goHome()
    phone.tapScreen()

def reconnect(port, phone):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start evolutions \"{}\" on port {}", phone, port)
    phone = TouchScreen(port, phone)
   
    while True:
        try:
            # phone.tapScreen(119, 1791) # Avatar
            phone.tapScreen(90, 30) # Clock
            time.sleep(2)
            phone.goHome()
            print("Check connection status")
            phone.waitMatchColorAndClick(914, 583, 149, 97, 121, time_out_ms=20000)
            print("Color match")
            time.sleep(1)
            phone.waitMatchColor(114, 136, 45, 49, 50, time_out_ms=30000)
            print("Connect screen detected")
            for x in range(230, 280, 4):
                r, g, b = phone.getRGB(x, 369)
                print("X {},{},{},{}".format(x, r, g ,b))
            # phone.waitMatchColorAndClick(241, 369, 143, 208, 218)
            time.sleep(1)
            print("TAP connect")
            phone.tapScreen(241, 369)
            phone.waitMatchColor(251, 1205, 66, 66, 66)
            time.sleep(1)
            print("TAP pair")
            phone.tapScreen(828, 1177)
            # phone.waitMatchColorAndClick(807, 1189, 29, 88, 102)
            print("Wait a minute to get the connection up!")
            for i in range(0,10):
                time.sleep(6)
                if phone.matchColor(914, 582, 255, 1, 0):
                    break
            time.sleep(30)
        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)
            
       
def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    reconnect(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
