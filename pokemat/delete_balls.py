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

def delete_red_balls(p):
    p.screen_go_to_home()
    p.tap_screen(500, 1802)
    p.color_match_wait_click(729, 1574, 240, 254, 238)
    sleep(1.4)
    text = p.pocr_read_line_center((171, 1700), (200, 160))
    print(f"Read {text}")
    if not "Poké Ball" in text\
       and not "Poke Ball" in text:
        p.scroll(0, -700, start_x=900, start_y=1900)
    text = p.pocr_read_line_center((171, 1700), (200, 160))
    if "Poké Ball" in text\
       or "Poke Ball" in text:
        # p.scroll(0, -700, start_x=900, start_y=1900)
        print("Found normal balls")
        p.tap_screen(280, 1420)
        # Minus
        p.color_match_wait_click(255, 857, 255, 255, 255, threashold=0, time_out_ms=3000)
        # Plus
        # p.color_match_wait_click(750, 857, 255, 255, 255, threashold=0, time_out_ms=3000)
        sleep(0.5)
        p.color_match_wait_click(385, 1128, 144, 217, 149, time_out_ms=3000, ex=False)
    else:
        print("No balls found")
    p.screen_go_to_home()

def action(port, arg = None):
        
    print("Start testing port {}",port)
    global p
    p = TouchScreen(port)
    startTime = datetime.now()
    delete_red_balls(p)
    p.screen_go_to_home()
    
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
