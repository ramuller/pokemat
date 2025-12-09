#!/bin/env python
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
from heal import heal

import json
import sys
from datetime import datetime
from _ast import If

def whiteScreen():
    for x in range(100, 800, 150):
        print("{}",format(phone.get_rgb(x, 2 * x)))
        if not phone.color_match(x, 2 * x, 255, 255, 255):
            print("NOOO White screen")
            return False
    print("White screen")
    return True


def defeat_gym(port, max_round=5):
    print("Start Deafeat on port {}", port)
    global phone 
    phone = TouchScreen(port)
    defeated = False
    round = 0
    while not defeated:
        try:
            print("Start defeat")
            retry = 3
            in_defeat = False
            if not phone.screen_is_in_gym():
                phone.screen_go_to_home()
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
            phone.pocr_wait_text_center((494, 789), (230, 80), "GO BATTLE")
            while "GO BATTLE" in phone.pocr_read_line_center((494, 789), (230, 80), "GO BATTLE"):
                phone.tap_screen(494, 789)
                sleep(1)
            # phone.color_match_wait_click(345, 777, 134, 217, 153)
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
            fight = True
            l = 0
            while not phone.screen_is_in_gym() \
                  and not phone.is_home() \
                  and not phone.color_match(501, 1828, 240, 246, 239) \
                  and not phone.color_match(500, 1886, 228, 242, 228) \
                  and not phone.color_match(500, 1000, 228, 242, 228) \
                  and fight:
                if phone.screen_is_in_gym():
                    for i in range(10):
                        sleep(0.2)
                        if not phone.screen_is_in_gym():
                            continue
                    break                    
                for x in [250, 500, 750]:
                    if not phone.screen_is_in_gym():
                        phone.tap_screen(x,1750)
                        time.sleep(0.1)
                    else:
                        print("Dont tap in gym")
                        if not phone.screen_is_in_gym():
                            phone.tap_screen(100, 100, button = 3)
                        fight = False
                l += 1
                # if l % 20:
                #     phone.tap_screen(501, 1859)
                    
            round += 1
            if round > max_round:
                return "give-up"
            if phone.screen_is_in_gym():
                defeated = phone.screen_gym_has_place()
            else:
                phone.screen_go_to_home()
            # heal(args.port)

        except Exception as e:
            phone.screen_go_to_home()
            print("Upps something went wrong but who cares?: {}", e)    
    # phone.pokemon_search("cp1500-2000")
    if phone.screen_go_to_gym() == False:
        print("Dont know how to enter defeat mode bye bye")
        phone.screen_go_to_home()
        return False    
    phone.tap_screen(871, 1632)
    phone.pokemon_search("cp10-100&0*,1*")
    # phone.pokemon_search("cp2800-5000&3*")
    phone.pokemon_select_first()
    phone.color_match_wait_click(277, 1029, 162, 220, 148)
    return defeated

            
       
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()

    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    defeat_gym(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
