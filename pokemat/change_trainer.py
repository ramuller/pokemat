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
        regex = ".*Gimmi.*123.*"        
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

    regex = trainer_regex(trainer)
    print(f"RE {regex}")
     
    for i in range(2):
        if phone.buttons.text_only.press(regex, 
                                         xs=phone.rel_x(0.2),
                                         mode='line',
                                         invert=True,
                                         retries=2, verbose=0):
            return True
        sx = int(phone.specs['width'] // 2 )
        sy = int(phone.specs['max_y'] * 0.9)
        phone.scroll(0, int(phone.specs['max_y'] * -0.8), 
                     start_x=sx, start_y=sy, scale=False)
        sleep(3)
         
        
    return False
    
            
def do_change_trainer(port, trainer):
    ret = None
    gog = None
    choose = []

    if phone.screen.get_current_screen() != 'home':
        ret = phone.buttons.t_returning_player.search(retries=1)
        gog = phone.buttons.t_login_google.search(retries=1)
        choose = phone.buttons.t_login_choose.search(retries=1)

    if ret == None \
        and gog == None \
        and choose == []:
        try:
            phone.screen_go_to_home()
            sleep(1)
            phone.buttons.i_pokeball.press()
            sleep(1)
            t = phone.buttons.t_setting.press(retries=5, verbose=0)

            t = phone.buttons.text_only.search('SETTINGS', \
                                               ye=phone.rel_y(0.3), \
                                               retries=5)
            sleep(2)
            sx = 1
            sy = int(phone.specs['max_y'] * 0.9)
            for t in range(3):
                phone.scroll(0, int(phone.specs['max_y'] * -0.8), 
                             start_x=sx, start_y=sy, scale=False)
                sleep(0.5)
                t = phone.buttons.text_only.press('.*Sign.*', \
                                                  xs=phone.rel_x(0.05), xe=phone.rel_x(0.5), \
                                                  retries=3, verbose=0)
                sleep(0.5)
                if t:
                    t = phone.buttons.b_yes.press(retries=3, verbose=0)
                    break
            else:
                print("Not idea where we are, cannot change trainer")
                return False

        except Exception as e:
            print(f"Exceptionf {e}")
            pass
        if phone.buttons.t_returning_player.search(retries=60) == None:
            return False
        ret = True

    if ret:
        phone.buttons.t_returning_player.press(retries=3)
        gog = True
    if gog:
        gog = phone.buttons.t_login_google.press(retries=3, delay=2)
    
    if trainer != "out":
        select_trainer(trainer)

    while phone.screen.get_current_screen != 'home':
        if phone.buttons.i_pokeball.press():
            sleep(1)
            if phone.buttons.text_only.search('.*SETTINGS.*', 
                                              ye=phone.rel_y(0.25)):
                phone.screen.go_home()
                return True

        
def change_trainer(port, trainer, check=False):
    print("Change trainers on port {}", port)
    global phone
    phone = TouchScreen(port)
    print(f"change_trainer{trainer}")
    regex = trainer_regex(trainer)

    if not check:
        do_change_trainer(port, trainer)
    else:
        while phone.ocr_wait_text((280, 1100), (440, 75), "RETURNING", pause=2, to_ms=1) \
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
