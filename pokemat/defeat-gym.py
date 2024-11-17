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
from _ast import If

def whiteScreen():
    for x in range(100, 800, 150):
        print("{}",format(phone.getRGB(x, 2 * x)))
        if not phone.matchColor(x, 2 * x, 255, 255, 255):
            print("NOOO White screen")
            return False
    print("White screen")
    return True

def inLobby():
    if phone.matchColor(861, 1570, 241, 246, 242) \
        and phone.matchColor(887, 1806, 236, 244, 239) \
        and phone.matchColor(493, 1839, 234, 241, 237) \
        and phone.matchColor(868, 210, 242, 251, 239):
        return True
    return False

def defeat(port, phone_model):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start Deafeat \"{}\" on port {}", phone_model, port)
    global phone 
    phone = TouchScreen(port, phone_model)
   
    while True:
        # try:
            print("Start defeat")
            noLobby = True
            for to in range(5,0,-1):
                print("Wait for lobbr {}",format(to))
                time.sleep(1)
                if inLobby():
                    noLobby = False
                    break
            if noLobby:
                print("Not in lobby")
                sys.exit(0)   
            phone.tapScreen(829, 1605)
            print("Start battle")
            phone.waitMatchColorAndClick(345, 777, 134, 217, 153)
            print("Wait for initial white screen")
            while not whiteScreen():
                time.sleep(0.2)
            print("Wait for initial white screen switch off")
            while whiteScreen():
                time.sleep(0.2)
            print("Sleep 2s")
            time.sleep(5)
            print("Verify white screen is off")
            while whiteScreen():
                time.sleep(0.2)
            print("Start fight")
            while not inLobby():
                for x in [250, 500, 750]:
                    phone.tapScreen(x,1750)
                    time.sleep(0.1)
        # except Exception as e:
        #     print("Upps something went wrong but who cares?: {}", e)
            
       
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
    defeat(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
