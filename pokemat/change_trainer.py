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

from pokelib import ExPokeLibError, ExPokeNoHomeError, ExPokeLibFatal

def selectTrainer(trainer):
    trainer = trainer.lower()
    print("Select new trainer {}".format(trainer))
    sleep(0.5)
    try:
        phone.color_match_wait_click(272, 1126, 160, 219, 147, time_out_ms = 30000)
        phone.color_match_wait_click(253, 1019, 255, 255, 255)
        phone.color_match_wait(503, 181, 233, 84, 50)
    except:
        return False
    sleep(3)
    if trainer in "eizu123":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        sleep(1)
        phone.tap_screen(439, 900)
    elif trainer in "pokeeizu123":
        sleep(1)
        phone.tap_screen(439, 1199)
    elif trainer in "schlumpiz":
        phone.tap_screen(390, 1931)
    elif trainer in "localhost":
        phone.tap_screen(543, 828)
    elif trainer in "plasticgirl..":
        sleep(2)
        phone.tap_screen(546, 656)
    elif trainer in "pokeralle123":
        print("Try pokeralle")
        sleep(2)
        phone.tap_screen(527, 1750)
    elif trainer in "higimmi222" or trainer in "bluebird":
        sleep(1)
        phone.tap_screen(652, 1019)
    elif trainer in "bluebird":
        sleep(1)
        phone.tap_screen(500, 1363)
    elif trainer in "higimmi333" or trainer in "yellowthatsit":
        sleep(1)
        phone.tap_screen(565, 1570)
    elif trainer in "higimmi444"or trainer in "blue":
        sleep(1)
        phone.tap_screen(565, 1400)
    elif trainer in "aphextvin":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        phone.tap_screen(321, 714)
    elif trainer in "helmutkaali":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        phone.tap_screen(321, 1430)
    elif trainer in "higimmi555"or trainer in "blond2023":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        phone.tap_screen(449, 1091)
    else:
        raise  ExPokeLibFatal("Unknow trainer {trainer}")

def change_trainer(port, phone_model, trainer):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Change trainers \"{}\" on port {}", phone_model, port)
    global phone
    phone = TouchScreen(port, phone_model)
    new_trainer = False
    while not new_trainer:
        if not phone.pocr_wait_text((280, 1100), (440, 75), "RETURNING") \
           and not phone.pocr_wait_text((260, 1000), (440, 75), "Google"):
            try:
                phone.screen_go_to_home()
                sleep(1)
                phone.color_match_wait_click(500, 1798, 255, 57, 69)
                phone.color_match_wait_click(940, 210, 212, 251, 204)
                sleep(0.5)
                for i in range(0,10):
                    phone.scroll(0, -800, start_x=10)
                    sleep(1)
                    if phone.pocr_wait_text((40, 1400), (250, 100), "Sign Out"):
                        break
                sleep(0.5)
                print("Click sign out")
                phone.tap_screen(40, 1450)
                sleep(1)
                phone.tap_screen(500,1000)
            except:
                pass
        # One screen up
        phone.tap_screen(100, 100, 3)
        
        phone.pocr_wait_text((280, 1100), (440, 75), "RETURNING", pause=2, to_ms=60*1000)

        selectTrainer(trainer)
               
        for to in range(0, 60):  # 1min.
            try:
                print("wait for home")
                if phone.is_home():
                    return True
                sleep(1)
            except:
                pass
        # return False
        
    
def main():

    parser = PokeArgs()
    parser.add_argument("trainer", help="Name of the new trainer")
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    change_trainer(args.port, args.phone, args.trainer)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
