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


def action(port, arg = None):
        
    print("Start testing port {}",port)
    global p
    p = TouchScreen(port)
    startTime = datetime.now()
    # t, npa = p.pocr.find_regex('.*RETURING.*', verbose=0)
    t, npa = p.pocr.find_button('RETURNING', verbose=0)
    if t:
        p.tap_screen(t['center'], scale=False)
    t, npa = p.pocr.find_button('Google', verbose=0)
    if t:
        p.tap_screen(t['center'], scale=False)
    t, npa = p.pocr.find_regex('Aphex', verbose=0)
    if t:
        p.tap_screen(t['center'], scale=False)
    endTime = datetime.now()
    delta = endTime - startTime
    print(f"Duration: {delta.total_seconds()} seconds")

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
