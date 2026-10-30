#!/bin/env python
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
from pokelib import CButtGymDefeat, CButtGymMyTeam, CButtYes
from pokelib import CButtSelectFirstPM
from heal import heal

import json
import sys
from datetime import datetime

def whiteScreen():
    for x in range(100, 800, 150):
        print("{}",format(phone.get_rgb(x, 2 * x)))
        if not phone.color_match(x, 2 * x, 255, 255, 255):
            print("NOOO White screen")
            return False
    print("White screen")
    return True

def add_pokemon_to_gym(phone, max_cp=2000, min_cp=1000):
    phone.screen.go_gym()
    if CButtGymMyTeam(phone).press():
        sleep(1)
        # The comma is needed to not find the search string for in the next button
        phone.select_pokemon("cp{}-{},".format(min_cp, max_cp))
        CButtSelectFirstPM(phone).press(retries=3)
        if CButtYes(phone).press(retries=5):
            print("Pokemon added to gym")
            return True
    print("No pokemon added to gym")
    return False

def defeat_gym(phone, max_round=5, y_coord=None):
    defeated = False
    round = 0
    while not defeated:
        try:
            print("Start defeat")
            retry = 3
            in_defeat = False
            if not phone.screen.go_gym():
                print("Not in gym after timeout")
                return False
            if CButtGymMyTeam(phone).search():
                print('my gym')
                return True
            # Calculate where to press for attack
            det = phone.buttons.i_exits.search()
            y_press = det.quad[0][1] - int(phone.specs['max_y'] * 0.028)
            CButtGymDefeat(phone).press()
            CButtGymDefeat(phone).press()
            sleep(1)
            phone.buttons.t_go_battle_gym.press(retries=5, verbose=1)
            phone.buttons.t_go_battle_gym.press(retries=1)

            sleep(5)

            fight = True
            l = 0
            gap = phone.specs['max_x'] // 4
            while not phone.buttons.i_exits.search(retries=1):
                for x in [gap, 2*gap, 3*gap]:
                    phone.tap_screen(x, y_press, scale=False)
                    time.sleep(0.1)

            fight = False   
            round += 1
            if round > max_round:
                return "give-up"
            if CButtGymMyTeam(phone).search():
                defeated = phone.screen_gym_has_place()
            else:
                phone.screen_go_to_home()
            # heal(args.port)

        except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)    
            phone.screen_go_to_home()
    return defeated

def action(port):
    phone = TouchScreen(port)
    if defeat_gym(phone):
        if phone.screen.go_gym():
            add_pokemon_to_gym(phone)
    phone.screen.go_home()
       
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()

    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
