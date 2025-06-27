#!/bin/env python
import time
from time import sleep
import os
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
from pokelib import Database

import json
import sys
from datetime import datetime
from mercurial.hgweb.common import continuereader
from random import randrange
import change_trainer
from defeat_gym import  defeat_gym
from heal import heal

def change_gym_color():
    if args.color in "red":
        args.color = "red"
    elif args.color in "yellow":
        args.color = "yellow"
    elif args.color in "blue":
        args.color = "blue"
    else:
        print("ERROR : unknow color {}".format(args.color))
        sys.exit(1)

    # p = TouchScreen(args.port, args.phone)
    db = Database()
    
    print("Start change color of gym to \"{}\"".format(args.color))    
    
    print(db.get_trainer_in_team(args.color))
    
    for t in db.get_trainer_in_team(args.color):
        print(t)
        my_name = None
        while my_name == None:
            try:
                p = TouchScreen(args.port)
                mn = p.get_my_name()
                for i in range(2, len(mn)):
                    print(mn[:i])
                    ret = db.get_trainer(mn[:i])
                    if len(ret) == 1:
                        my_name = ret[0][1]
                        print(f"My name from DB {my_name}")
                        break                    
            except:
                print("Invalid name")
                sleep(1)
                
            
            
        if t.lower() != my_name.lower():
            change_trainer.change_trainer(args.port, t)
            print("Let stabilize")
            sleep(10)
            heal(args.port)
        defeated = False
        max_tries = 10
        while defeated == False:
            max_tries -= 1
            if max_tries <=0:
                print("Useless to continue")
                sys.exit(1)
            try:
                try:
                    defeated = defeat_gym(args.port)
                except:
                    pass
                heal(args.port)
                if defeated == False:
                    print("Defeat failed. Try again")
                    
                elif defeated == "give-up":
                    print("Defeat give-up. By bye")
                    return False
            except:
                pass
            
    change_trainer.change_trainer(args.port,  "no-trainer")
            
def main():

    global args
    parser = PokeArgs()
    parser.add_argument("color", type=str, help="new color for the gym")    
    args = parser.parse_args()

    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    change_gym_color()
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
