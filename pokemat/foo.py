#!/bin/env python
import easyocr
import argparse
import time
from time import sleep
import os
import sys
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# import pytesseract

import json
import sys
from datetime import datetime

'''
Capture a range of regions and show
'''
def cap_and_show():
    # upper circle in gym
    # for y in range(1636,1670,2):
    #     jbuf = p.screen_capture_bw((780, y), (200, 2))
    dd = {}
    # xr=(1880,1890,2)
    xr = (1646,1652,2)
    for port in [3003, 3004]:
        p = TouchScreen(port)
        dd.update({port:[]})
        # print(dd)
        s,e,o = xr
        for y in range(s,e,o): 
            jbuf = TouchScreen(port).screen_capture_bw((790, y), (180, 2))
            jbuf = p.screen_capture_bw((790, y), (180, 2))
            npa = np.array(jbuf["gray"], dtype=np.uint8)
            dd[port]. append(np.diff(npa.astype(np.int16)))
            
    
    # for th in range(40,41,5):
    #     print(f"Y = {y} - TH {th} max {(np.abs(delta) >= th).sum()}")
    y = xr[0]
    for i in range(len(dd[3003])):
        for th in range(30,31,5):
            m1 = (np.abs(dd[3003][i]) >= th).sum()
            m2 = (np.abs(dd[3004][i]) >= th).sum()
            print(f"Y = {y} - TH {th} max1 {m1} max2 {m2}") 
        y += xr[2]
    #print(dd[3003])
    pixel_array = np.array(jbuf["gray"], dtype=np.uint8)
    pixel_array = pixel_array.reshape((jbuf["hight"], jbuf["width"]))
    image = Image.fromarray(pixel_array, mode='L')    
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.title(f'Grayscale Bitmap')
    plt.axis('off')
    plt.show()Bipolar-ICs
def ocr_test(p):
    print("Start ocr testing")
    reader = easyocr.Reader(['en'])
    jbuf = p.screen_capture_bw((0,0), (575, 1023), scale=False)
    for i in range(0, 300):
        # print(f"Round {i}")
        t1 = datetime.now()
        pixel_array = np.array(jbuf["gray"], dtype=np.uint8)
        pixel_array = pixel_array.reshape((jbuf["hight"], jbuf["width"]))
        image = Image.fromarray(pixel_array, mode='L')
        
        text = reader.readtext(pixel_array)
        t2 = datetime.now()
        # print("Elapsed time {}s".format((t2-t1).total_seconds()))
    for t in text:
       print(t)
    return
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.title(f'Grayscale Bitmap')
    plt.axis('off')
    plt.show()    
    
def action(port, arg = None):
        
    print("Start testing port {}",port)
    # global p
    p = TouchScreen(port)
    startTime = datetime.now()
    ocr_test(p)

    return
    while True:
        print("Wating for an egg")
        print(p.egg_handle())
        time.sleep(1)
    
    p.screen_go_to_home()
    
    sys.exit(0)
    p.friend_set_nickname("test")
    
    
    for y in range(100, 1900,20):
        text, image = p.pocr_read_line((200, y),(300, 50))
        if text != '':
            print(f"Read at {y} text : {text.lower()}")
    
    for i in range(0,2):
        print("Scroll up")
        p.scroll(0, -1800, start_x=900, start_y=1900)
        sleep(1)        

    for y in range(100, 1900,20):
        text, image = p.pocr_read_line((200, y),(300, 50))
        if text != '':
            print(f"Read at {y} text : {text.lower()}")
    
    for i in range(0,2):
        print("Scroll up")
        p.scroll(0, 1800, start_x=900, start_y=100)
        sleep(1)        
    sys.exit(0)
    
    # for name in ["eagal-", "88","test3"]:
    for name in range(65, 72):
        n2 = "dummy-{}".format(name)
        p.friend_change_nick(f"new_{n2}")
  
    # p.friend_change_nick("new_98")
    
    sys.exit(1)
    # reader = easyocr.Reader(['en'])
    t1 = datetime.now()
    for i in range(0, 10):
        # import easyocr
        # reader = easyocr.Reader(['en'])
        # jbuf = p.screen_capture_bw(100, 120, 200, 70)
        # jbuf = p.screen_capture_bw(550, 550, 230, 70)
        # jbuf = p.screen_capture_bw(10, 10, 980, 1980)
        # jbuf = p.screen_capture_bw(10, 550, 980, 70)
        # jbuf = p.screen_capture_bw(360, 650, 280, 76)
        jbuf = p.screen_capture_bw(360, 350, 280, 376)
        pixel_array = np.array(jbuf["gray"], dtype=np.uint8)
        pixel_array = pixel_array.reshape((jbuf["hight"], jbuf["width"]))
        image = Image.fromarray(pixel_array, mode='L')
        # print(image.tell())
        if False:
            # text = reader.readtext(pixel_array)
            # text = p.read_text(550, 550, 230, 70)
            text, image = p.pocr_read(350, 1650, 300, 76)
            for t in text:
                print("Read with easyocr {}".format(t))
        # print("Read with easyocr {}".format(text))
        if True:
            text, image = p.pocr_read(350, 1650, 300, 76)
            print("Read with tessertact {}".format(text))
        # _, image = p.read_text(290, 530, 400, 90)
    t2 = datetime.now()
    print("Elapsed time {}s".format((t2-t1).total_seconds()))
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.title(f'Grayscale Bitmap')
    plt.axis('off')
    plt.show()
    print("Is pokemon : {}".format(p.screen_is_catch_pokemon()))
    
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    # action(args.port)
    action(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
