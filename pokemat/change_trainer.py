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

def selectTrainer(trainer):
    trainer = trainer.lower()
    print("Select new trainer {}".format(trainer))
    sleep(0.5)
    # try:
    #     phone.color_match_wait_click(272, 1126, 160, 219, 147, time_out_ms = 30000)
    #     phone.color_match_wait_click(253, 1019, 255, 255, 255)
    #     phone.color_match_wait(503, 181, 233, 84, 50)
    # except:
    #     return False

    if trainer in "eizu123":
        regex = "^eizu.*123.*"
    elif trainer in "pokeeizu123":
        regex = ".*poke.*eizu.*123.*"
    elif trainer in "schlumpiz":
        regex = ".*schlumpiz.*|.*rolf.*"
    elif trainer in "localhost":
        regex = ".*localhost.*"
    elif trainer in "plasticgirl..":
        regex = ".*plastic.*"
    elif trainer in "pokeralle123":
        regex = ".*pokeralle.*"
    elif trainer in "higimmi222":
        regex = ".*gimmi222.*"        
    elif trainer in "higimmi1234":
        regex = ".*gimmi.*123.*"        
    elif trainer in "higimmi33" or trainer in "yellowthatsit":
        regex = ".*higimmi33.*|.*yellow.*"        
    elif trainer in "higimmi444"or trainer in "blue":
        regex = ".*gimmi444.*|.*blue.*bird.*"        
    elif trainer in "aphextvin":
        regex = ".*aphex.*"        
    elif trainer in "helmutkaali":
        regex = ".*helmut.*"        
    elif trainer in "higimmi555"or trainer in "blond2023":
        regex = ".*higimmi55.*|.*blond.*"        
    else:
        raise  ExPokeLibFatal(f"Unknow trainer {trainer}")
    
    print(f"RE {regex}")
    for y in range(100, 1900, 20):
        text = phone.pocr_read_line((200, y),(300, 50))
        if text != '':
            scan = text.lower()
            print(f"Read at {y} text : {scan}")
            if re.search(regex, scan):
                print("Result {}".format(re.search(f".*{regex}.*", scan)))
                phone.tap_screen(500, y + 10)
                sleep(10)
                return True

    for i in range(0,2):
        print("Scroll up")
        phone.scroll(0, -1800, start_x=900, start_y=1900)
        sleep(1)
        
    for y in range(100, 1900, 20):
        text = phone.pocr_read_line((200, y),(300, 50))
        if text != '':
            scan = text.lower()
            print(f"Read at {y} text : {scan}")
            if re.search(regex, scan):
                print("Result {}".format(re.search(f".*{regex}.*", scan)))
                phone.tap_screen(500, y + 10)
                sleep(10)
                return True
    return False
    
            
            
   

def do_change_trainer(port, phone_model, trainer):
    new_trainer = False
    text = phone.pocr_read_line((240, 320), (520, 70))
    if not "choose" in text.lower():
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
                sleep(1)
                print("Click sign out")
                phone.tap_screen(40, 1450)
                sleep(1.5)
                phone.tap_screen(500,1000)
            except:
                pass
        # One screen up
        phone.tap_screen(100, 100, 3)
        
        phone.pocr_wait_text((280, 1100), (440, 75), "RETURNING", pause=2, to_ms=60*1000)
        phone.color_match_wait_click(272, 1126, 160, 219, 147, time_out_ms = 3000)
        phone.pocr_wait_text((260, 1000), (440, 75), "Google", pause=1, to_ms=10*1000)
        phone.color_match_wait_click(253, 1019, 255, 255, 255)
        phone.pocr_wait_text((240, 320), (520, 70), "hoose", pause=1, to_ms=10*1000)

    if selectTrainer(trainer):
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
        
def change_trainer(port, phone_model, trainer):
    print("Change trainers \"{}\" on port {}", phone_model, port)
    global phone
    phone = TouchScreen(port, phone_model)
    t = phone.pocr_read_line((280, 1100), (440, 75))
    print(f"change_trainer{t}")
    while phone.pocr_wait_text((280, 1100), (440, 75), "RETURNING", pause=2, to_ms=1) \
          or not trainer.lower() in TouchScreen(port, phone_model).get_my_name().lower():
        print("Start change")
        do_change_trainer(port, phone_model, trainer)
        
    
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
