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
import re


from pokelib import ExPokeLibError, ExPokeNoHomeError, ExPokeLibFatal


def trainer_regex(trainer):
    
    if trainer in "eizu123":
        regex = "^eizu.*123.*"
    elif trainer in "pokeeizu123":
        regex = ".*Poke.*Eizu.*123.*"
    elif trainer in "schlumpiz":
        regex = ".*schlumpiz.*|.*rolf.*"
    elif trainer in "localhost":
        regex = ".*localhost.*"
    elif trainer in "plasticgirl..":
        regex = ".*Plastic.*"
    elif trainer in "pokeralle123":
        regex = ".*pokeralle.*"
    elif trainer in "higimmi222":
        regex = ".*gimmi222.*"        
    elif trainer in "higimmi1234":
        regex = ".*gimmi.*123.*"        
    elif trainer in "higimmi33" or trainer in "yellowthatsit":
        regex = ".*higimmi33.*|.*yellow.*"        
    elif trainer in "higimmi444"or trainer in "blue":
        regex = ".*gimmi444.*|.*Blue.*Bird.*"        
    elif trainer in "aphextvin":
        regex = ".*Aphex.*"        
    elif trainer in "helmutkaali":
        regex = ".*Helmut.*"        
    elif trainer in "higimmi555"or trainer in "blond2023":
        regex = ".*higimmi55.*|.*Blond.*"        
    elif trainer in "out":
        regex = "sdsadsadsadsad"        
    else:
        raise  ExPokeLibFatal(f"Unknow trainer {trainer}")
    return regex

def select_trainer(trainer):
    trainer = trainer.lower()
    print("Select new trainer {}".format(trainer))
    sleep(0.5)
    # try:
    #     phone.color_match_wait_click(272, 1126, 160, 219, 147, time_out_ms = 30000)
    #     phone.color_match_wait_click(253, 1019, 255, 255, 255)
    #     phone.color_match_wait(503, 181, 233, 84, 50)
    # except:
    #     return False

    regex = trainer_regex(trainer)
    
    print(f"RE {regex}")
     
    for i in range(2):
        t, _ = phone.pocr_find_regex(regex)
        if t:
            phone.tap_screen(t['center'], scale=False)
            return
        for i in range(2):
            print("Scroll up")
            phone.scroll(0, -1800, start_x=900, start_y=1900)
            sleep(1)
        
    return False
    
            
def detect_screen(phone):     
    fs = phone.pocr.easyocr_read_center((0, 0), (phone.specs['w'], phone.specs['h']), scale=False)
    print(fs[1])
    screen = "pogo"
    for i in range(len(fs)):
        if "account" in fs[i]["text"]:
            screen = "accounts"
            break
        if "Google" in fs[i]["text"]:
            screen = "login"
            break
        if "PLAYER" in fs[i]["text"]:
            screen = "start"
            break
    return screen, fs[i]["center"][0], fs[i]["center"][1]

def do_change_trainer(port, trainer):

    # text = phone.pocr_read_line((240, 320), (520, 70))
    screen,x , y = detect_screen(phone)
   
    print(f"On screen {screen}")
    
    if screen == "pogo":
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
            sleep(1)
            print("Click sign out")
            phone.tap_screen(40, 1450)
            sleep(1.5)
            phone.tap_screen(500,1000)
        except:
            pass
        while screen != "start":
            print("Check screen")
            screen,x , y = detect_screen(phone)
            sleep(2)
 
    if screen == "start":
        phone.tap_screen(x, y, scale=False)
        print("hit")
        while screen != "login":
            print("Check screen")
            screen,x , y = detect_screen(phone)
            sleep(2)

    if screen == "login":
        phone.tap_screen(x, y, scale=False)
        print("hit")
        while screen != "accounts":
            print("Check screen")
            screen,x , y = detect_screen(phone)
            sleep(2)
        

    if select_trainer(trainer):
        for to in range(0, 60):  # 1min.
            try:
                print("wait for home")
                if phone.is_home():
                    return True
                phone.color_match_wait_click(244, 1376, 155, 219, 150, ex=False, time_out_ms=500)
                if phone.pocr_wait_text((400, 1860), (200, 70), "DISMISS", pause=1, to_ms=1):
                    phone.tap_screen(500, 1700)
                sleep(1)
            except:
                pass
        
def change_trainer(port, trainer, check=False):
    print("Change trainers on port {}", port)
    global phone
    phone = TouchScreen(port)
    print(f"change_trainer{trainer}")
    regex = trainer_regex(trainer)
    t, _ = phone.pocr_find_regex(regex, ul=(0, phone.specs['h'] - phone.specs['h'] // 4), \
                                 lr=(phone.specs['w'] // 2, phone.specs['h'] // 4))
    if t:
        print(f"Trainer is already {t['text']}")
        return
    if not check:
        do_change_trainer(port, trainer)
    else:
        while phone.pocr_wait_text((280, 1100), (440, 75), "RETURNING", pause=2, to_ms=1) \
              or not trainer.lower() in TouchScreen(port).get_my_name().lower():
            print("Start change")
            do_change_trainer(port, trainer)
        
    
def main():

    parser = PokeArgs()
    parser.add_argument("trainer", help="Name of the new trainer")
    parser.add_argument("-c", "--check", action='store_true', help="Don't check current name")    
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    change_trainer(args.port, args.trainer, args.check)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
