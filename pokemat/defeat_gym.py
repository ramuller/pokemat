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


def defeat_gym(port, phone_model, max_round=5):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start Deafeat \"{}\" on port {}", phone_model, port)
    global phone 
    phone = TouchScreen(port, phone_model)
    defeated = False
    round = 0
    while not defeated:
        # try:
            print("Start defeat")
            retry = 3
            in_defeat = False
            if phone.screen_go_to_gym() == False:
                print("Dont know how to enter defeat mode bye bye")
                phone.screen_go_to_home()
                return False
            if phone.screen_my_poke_in_gym():
                print("Already in gym")
                return True
            if phone.screen_gym_has_place():
                print("Gym is defeated")
                break
            if not phone.screen_gym_need_defeat():
                print("Panic")

            phone.tap_screen(829, 1605)
            print("Start battle")
            phone.color_match_wait_click(345, 777, 134, 217, 153)
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
            #                  and not phone.button_is_back() \
            while not phone.screen_is_in_gym() \
                  and not phone.is_home():
                for x in [250, 500, 750]:
                    phone.tap_screen(x,1750)
                    time.sleep(0.1)
                    
            round += 1
            if round > max_round:
                return "give-up"
            defeated = phone.screen_gym_has_place()
    
    phone.tap_screen(871, 1632)
    phone.pokemon_search("cp1500-2000")
    phone.pokemon_select_first()
    phone.color_match_wait_click(277, 1029, 162, 220, 148)
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
    defeat_gym(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
