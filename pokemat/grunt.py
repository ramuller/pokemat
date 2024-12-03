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
   
    try:
        phone.waitMatchColorAndClick(305, 1773, 137, 216, 153, time_out_ms = 1500)
    except:
        pass
    time.sleep(1)
    phone.spinDisk()
    try:
        phone.waitMatchColorAndClick(656, 595, 240, 206, 179, time_out_ms = 1500)
    except:
        pass
    phone.tapScreen(656, 595)
    time.sleep(1)
    phone.tapScreen(656, 595)
    phone.waitMatchColorAndClick(354, 1535, 151, 217, 147)
    time.sleep(1)
    phone.waitMatchColorAndClick(366, 1791, 159, 218, 146)
    time.sleep(2)

    phone.doBattle()
    
    # Wait for trainer
    try:
        phone.waitCatchColorAndClick(512, 873, 203, 89, 50, time_out_ms = 3500)
    except:
       pass
    phone.tapScreen(512, 873) 

    phone.waitMatchColorAndClick(305, 1773, 137, 216, 153)
    sleep(3)
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
