#!/bin/env python
#
# Got the al friends and up-date the status
# Plan is provide alist 
#
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

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract
import re

def action(port, phone, distance = 15, right = True, berry = "g"):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("screen read on  \"{}\" on port {}", phone, port)
    p = TouchScreen(port, phone)
    db = Database()
    
    hist_size=5
    hist_idx = 0
    hist_names = []
    for i in range(0, hist_size):
        hist_names.append(str(i))
    
    print(hist_names)
    
    # SQL statement to insert a record
    # sql = "INSERT INTO friends (name, trainer) VALUES (%s, %s)"
    
    my_name = p.my_name()
    print("My name = '{}'".format(my_name))
    # print("From DB {}".format(db.get_trainer(my_name)[0][1]))
    my_len = len(my_name)
    for rest in range(my_len -3, my_len):
        if len(db.get_trainer(my_name[:(my_len-rest)])) == 1:
            my_name = db.get_trainer(my_name[:my_len-rest])
            print("Myname {}".format(my_name))
            break
    my_name = db.get_trainer(my_name)[0][1]
    print("My name = '{}'".format(my_name))
    p.screen_friend()
    # p.friend_search("lucky")
    p.selectFirstFriend()
    sleep(1)
    # for i in range(0,5):
    while len(set(hist_names)) > 1:
        if p.hasGift():
            p.tap_screenBack()
            print("Has gift")
            sleep(0.5)
        p.tap_screen(270, 360)
        sleep(1.5)
        # Friend level
        friend_level = p.read_text(360, 650, 280, 50)[0]
        print("Friend level '{}'".format(friend_level))               
        p.tap_screen(750, 880)
        sleep(1.5)
        # jbuf = p.screen_capture_bw(290, 530, 400, 90)
        # Name
        name = p.read_text(290, 530, 400, 90)[0]
        print("Name '{}'".format(name))               
        # days to play
        try:
            text = p.read_text(400, 1080, 50, 50)[0]
            tl = re.findall(r'\d+\.?\d*', text)
            days_to_go = int(tl[0])
        except:
            days_to_go = 0
        print("Days to go : {}".format(days_to_go))
        print(db.add_friend(name, my_name, days_to_go, friend_level))
        p.tap_screen(100, 100, button = 3)   
        p.scroll(-600, 0, 900, 1600)
        hist_names[hist_idx % hist_size] = name
        hist_idx += 1
        print("Last names : {}".format(set(hist_names)))
        sleep(5)
    
    if False:
        text, image = p.read_text(200, 350, 400, 400)
        print("Pokename : {}".format(text))

    print(text)    #cursor.close()
    conn.close()    
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.title(f'Grayscale Bitmap')
    plt.axis('off')
    plt.show()
    
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
