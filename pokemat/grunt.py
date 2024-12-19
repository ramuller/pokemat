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
    # phone.doBattle()
    no_grunt = False
    no_grunt = True
    gy = 500
    while no_grunt:
        if phone.matchColor(868, 197, 241, 247, 240):
            no_grunt = False
        if phone.matchColor(460, 849, 206, 92, 51, threashold = 20):
            print("Rocket found")
            no_grunt = False
            break
        for x in range(100, 900, 10):
            print("Search grunt {}, {}".format(x, 900))
            # if phone.matchColor(x, gy, 73, 73, 75):
            if phone.matchColor(x, gy, 166, 73, 66):
                print("Grunt R found")
                phone.tapScreen(x, gy + 500)
                time.sleep(1)
                if phone.matchColor(868, 197, 241, 247, 240) or \
                         phone.matchColor(506, 849, 206, 92, 51):
                    print("In stop")
                    x = 10000
                    no_grunt = False
        
   
    try:
        phone.waitMatchColorAndClick(463, 855, 203, 79, 41, time_out_ms = 1500)
    except:
        pass
    time.sleep(1)
    phone.spinDisk()
    try:
        i = 30
        no_grunt = True
        while i > 0:
            i = i -1
            print("Wait opponent {}".format(i))            
            if phone.matchColor(506, 849, 206, 92, 51, threashold = 20) or \
                   phone.matchColor(506, 880, 206, 92, 51, threashold = 20) or \
                   phone.matchColor(611, 880, 206, 92, 51, threashold = 20) or \
                   phone.matchColor(620, 880, 206, 92, 51, threashold = 20):
                phone.tapScreen(506, 849)
                i = 0
                break
            if phone.matchColor(498, 1824, 235, 242, 242):
                phone.tapScreen(498, 1824)
            sleep(1)
    except:
        pass
    print("Wait opponent")
    try:
        phone.waitMatchColorAndClick(348, 1554, 151, 217, 149, threashold=20, time_out_ms = 3500)
    except:
        pass
    time.sleep(1)
    phone.tapScreen(388, 1552)
    phone.waitMatchColor(350, 1771, 159, 222, 146)
    time.sleep(1)
    phone.tapScreen(970, 1452)
    time.sleep(1)
    print("Wait go battle")
    phone.tapScreen(500, 1800)
    
    # try:
    #     phone.waitMatchColorAndClick(338, 1779, 162, 220, 148, threashold=20, time_out_ms = 15500)
    # except:
    #     pass
    time.sleep(4)
    print("do battle")
    phone.doBattle()
    
    # Wait for trainer
    for i in range(1,10):
        try:
            phone.waitMatchColorAndClick(305, 1773, 137, 216, 153, time_out_ms = 2000)
        except:
            phone.tapScreen(305, 1773)
        pass
    phone.tapScreen(512, 873) 

    sleep(6)
    print("Try to catch")
    phone.catch()       
       
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
