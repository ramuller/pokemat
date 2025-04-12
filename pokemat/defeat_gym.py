#!/bin/env python
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
from _ast import If

def whiteScreen():
    for x in range(100, 800, 150):
        print("{}",format(phone.getRGB(x, 2 * x)))
        if not phone.color_match(x, 2 * x, 255, 255, 255):
            print("NOOO White screen")
            return False
    print("White screen")
    return True


def defeat(port, phone_model):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start Deafeat \"{}\" on port {}", phone_model, port)
    global phone 
    phone = TouchScreen(port, phone_model)
    defeated = False
    while not defeated:
        # try:
            print("Start defeat")
            retry = 3
            in_defeat = False
            while not phone.screen_is_defeat_gym():
                if phone.is_home():
                    print("is home try to tap gym and wait 5 seconds")
                    phone.tap_screen(500, 600)
                    sleep(5)
                elif phone.button_is_back():
                    print("Has back button")
                    phone.tap_back()
                    sleep(3)
                retry -= 1
                if retry < 1:
                    print("Dont know how to enter defeat mode bye bye")
                    return "give-up"
    
            phone.tap_screen(829, 1605)
            print("Start battle")
            phone.ccolor_match_wait_click(345, 777, 134, 217, 153)
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
            while not phone.screen_is_defeat_gym() \
                  and not phone.button_is_back() \
                  and not phone.is_home():
                for x in [250, 500, 750]:
                    phone.tap_screen(x,1750)
                    time.sleep(0.1)
        # except Exception as e:
        #     print("Upps something went wrong but who cares?: {}", e)
            
       
def main():

    parser = PokeArgs()
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
