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
            phone.tapScreen(125, 406)
            print("Check connection status")
            phone.waitMatchColorAndClick(750, 552, 146, 91, 121, time_out_ms=60000)
            print("Color match")
            try:
                phone.waitMatchColorAndClick(222, 1273, 81, 146, 222)
                phone.waitMatchColorAndClick(265, 1244, 81, 146, 222)
            except:
                log.info("No active sync needed")
                pass            
            phone.tapScreen(125, 406)
            print("Wait for connect screen")
            phone.waitMatchColor(564, 1744, 254, 253, 247, time_out_ms=60000)
            phone.tapScreen(602, 1736)
            log.info("Pair clicked")
            print("Wait a minute to get the connection up!")
            for i in range(0,10):
                time.sleep(6)
                if phone.colorMatch(564, 1744, 254, 253, 247):
                    phone.tapScreen(602, 1736)
                    
            time.sleep(60)
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