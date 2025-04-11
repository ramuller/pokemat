#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal

import json
import sys
from datetime import datetime

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract
import mysql.connector
import re

def action(port, phone, distance = 15, right = True, berry = "g"):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("screen read on  \"{}\" on port {}", phone, port)
    p = TouchScreen(port, phone)

    conn = mysql.connector.connect(
        host='leo',       # or your host
        user='pokemat',
        password='pokemat123',
        database='pokemat'
    )
    
    hist_size=5
    hist_idx = 0
    hist_names = []
    for i in range(0, hist_size):
        hist_names.append(str(i))
    
    print(hist_names)
    
    cursor = conn.cursor()
    # SQL statement to insert a record
    sql = "INSERT INTO friends (name, trainer, days_to_go, friend_level) VALUES (%s, %s, %s, %s)"
    # sql = "INSERT INTO friends (name, trainer) VALUES (%s, %s)"
    
    my_name = p.my_name()
    print("My name = {}".format(my_name))
    p.friendScreen()
    p.selectFirstFriend()
    
    # for i in range(0,5):
    while len(set(hist_names)) > 1:
        if p.hasGift():
            p.tap_screenBack()
            sleep(1.5)
        p.tap_screen(270, 360)
        sleep(1.5)
        # Friend level
        text, image = p.read_text(360, 650, 280, 50)
        friend_level = text.replace("\n", "")
        print(text)               
        p.tap_screen(750, 880)
        sleep(1.5)
        # jbuf = p.screen_capture_bw(290, 530, 400, 90)
        # Name
        text, image = p.read_text(290, 530, 400, 90)
        name = text.replace("\n", "")
        print(text)               
        # days to play
        try:
            text, image = p.read_text(400, 1080, 50, 50)
            text = text.replace("\n", "")
            tl = re.findall(r'\d+\.?\d*', text)
            days_to_go = int(tl[0])
        except:
            days_to_go = 0
        print("Days to go : {}".format(days_to_go))
        values = (name, my_name, days_to_go, friend_level)
        # values = (name, "Aphex Twin")
        try:
            cursor.execute(sql, values)
            conn.commit()
        except mysql.connector.errors.IntegrityError as e:
            print("Duplicate entry...ignoring {}".format(values))
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

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=False, default=3005, \
                        help="TCP port for the connection.")
    parser.add_argument("-d", "--distance", action="store", default=15, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    
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
