#!/bin/env python
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
# import easyocr

import json
import sys
from datetime import datetime


def login():
        
    print("Start login")
    # t, npa = p.ocr.find_regex('.*RETURING.*', verbose=0)
    t, npa = p.ocr.find_button('RETURNING', verbose=0)
    if t:
        p.tap_screen(t['center'], scale=False)
        sleep(2)
    t, npa = p.ocr.find_button('Google', verbose=0)
    if t:
        p.tap_screen(t['center'], scale=False)
        sleep(2)
    t = None
    while not t:
        t, npa = p.ocr.find_regex('Plastic.*', verbose=10)
        if t:
            p.tap_screen(t['center'], scale=False)

def no_exit():
    p.screen_go_to_home()

def test_regex():   
    button, npa = p.ocr.regex('.*paused.*', verbose=0)
    if button:
        p.tap_screen(button['center'], scale=False)
        sleep(2)
    button, npa = p.ocr.regex('.*Nuuksio.*', verbose=10)
    if button:
        p.tap_screen(button['center'], scale=False)
        sleep(2)

def test_button():
    p.buttons.ocr.mode = 'line'
    button = p.buttons.dark('.*Sign.*', action='check', verbose=10)
    button = p.buttons.white('.*Sign.*', action='check', verbose=0)
    if not button:
        print("Failed to find POWER button")
    else:
        print("Pressed POWER button")


def pure_read():
    # text, _ = p.ocr.read_rec_lines(start=(0,30), scale=False, verbose=10, mode='symbol')
    # p.ocr.mode = 'line'
    # p.ocr.starty = int(p.specs['max_y'] * 0.9)
    text, _ = p.ocr.read()
    print("OCR Text:")
    for t in text:
        print("   {}".format(t))

def test_egg():
    p.egg_handle()


def action(port, arg = None):
    global p
    p = TouchScreen(port)
    t1 = datetime.now()
    # no_exit()
    # login()
    # test_regex()
    # pure_read()
    # test_egg()
    test_button()
    t2 = datetime.now()
    print("Elapsed time {}s".format((t2-t1).total_seconds()))

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
