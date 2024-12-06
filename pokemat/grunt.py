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

def raid(port, phone):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start batteling \"{}\" on port {}", phone, port)
    phone = TouchScreen(port, phone)

    no_grunt = False
    # no_grunt = True
    
    while no_grunt:
        for x in range(100, 900, 10):
            print("Search grunt {}, {}".format(x, 890))
            if phone.matchColor(x, 890, 73, 73, 75):
                phone.tapScreen(x, 890)
                if phone.matchColor(868, 197, 241, 247, 240):
                    no_grunt = False
        
   
    try:
        phone.waitMatchColorAndClick(305, 1773, 137, 216, 153, time_out_ms = 1500)
    except:
        pass
    time.sleep(1)
    phone.spinDisk()
    try:
        phone.waitMatchColorAndClick(592, 585, 241, 204, 176, threashold=20, time_out_ms = 3500)
    except:
        pass
    phone.waitMatchColorAndClick(380, 1544, 146, 216, 149, time_out_ms = 5500)
    phone.waitMatchColorAndClick(366, 1791, 159, 218, 146, time_out_ms = 5500)
    time.sleep(2)

    phone.doBattle()
    
    # Wait for trainer
    for i in range(1,10):
        try:
            phone.waitMatchColorAndClick(305, 1773, 137, 216, 153, time_out_ms = 2000)
        except:
               phone.tapScreen(305, 1773)
        pass
    phone.tapScreen(512, 873) 

    sleep(3)
    print("Try to catch")
    phone.catch       
       
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
    raid(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
