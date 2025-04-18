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

def selectTrainer(trainer):
    trainer = trainer.lower()
    print("Select new trainer {}".format(trainer))
    sleep(0.5)
    phone.color_match_wait_click(272, 1126, 160, 219, 147, time_out_ms = 30000)
    phone.color_match_wait_click(253, 1019, 255, 255, 255)
    phone.color_match_wait(503, 181, 233, 84, 50)
    sleep(3)
    if trainer in "eizu123":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        sleep(1)
        phone.tap_screen(439, 900)
    if trainer in "pokeeizu":
        sleep(1)
        phone.tap_screen(439, 1199)
    elif trainer in "schlumpiz":
        phone.tap_screen(390, 1931)
    elif trainer in "localhost":
        phone.tap_screen(543, 828)
    elif trainer in "plastic":
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
    elif trainer in "aphex":
        for i in range(0,5):
            print("Scroll up")
            phone.scroll(0, -400, start_x=900)
            sleep(1)        
        phone.tap_screen(321, 714)
    elif trainer in "helmuteizu":
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
        
        print("Unknow trainer")
        sys.exit(1)

def change_trainer(port, phone_model, trainer):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Change trainers \"{}\" on port {}", phone_model, port)
    global phone
    phone = TouchScreen(port, phone_model)
    new_trainer = False
    while not new_trainer:
        t_ret = phone.read_text_line(280, 1100, 440, 75)
        t_gog = phone.read_text_line(260, 1000, 440, 75)
        if not "RETURNING" in t_ret \
           and not "Google" in t_gog:
            try:
                phone.screen_home()
                sleep(1)
                phone.color_match_wait_click(500, 1798, 255, 57, 69)
                phone.color_match_wait_click(940, 210, 212, 251, 204)
                sleep(0.5)
                for i in range(0,10):
                    phone.scroll(0, -800, start_x=10)
                    if "Sign Outt" in phone.read_text_line(40, 1400, 250, 100):
                        break
                    sleep(0.5)
                sleep(0.5)
                print("Click sign out")
                phone.tap_screen(500, y - 20)
                sleep(1)
                phone.tap_screem(500,1000)
            except:
                pass
        phone.tap_screen(100, 100, 3)
        for t in range(0, 20):
            if "RETURNING" in phone.read_text_line(280, 1100, 440, 75):
                # phone.tap_screen(280, 1100)
                break
            print("Wait for returning player")
            sleep(1)
            
        selectTrainer(trainer)
               
        for to in range(0, 60):  # 1min.
            try:
                print("wait for home")
                if phone.is_home():
                    return
                sleep(1)
            except:
                pass
        
    
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
