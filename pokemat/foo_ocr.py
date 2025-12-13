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
from pokelib import Ocr

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
    rounds = 1
    p = TouchScreen(port)
    # startTime = datetime.now()
    #
    # rounds = 1
    # p.pocr_read((0, 0), (10,10), scale=False)
    #
    # t1 = datetime.now()
    # for i in range(rounds):
    #     text = p.pocr_read((0, 0), (p.specs['w'], p.specs['h']), scale=False)
    # t2 = datetime.now()
    # print("Elapsed time {}s".format((t2-t1).total_seconds()))
    # print(text)

    
    
    t1 = datetime.now()
    for i in range(rounds):
        # text = p.pocr.easyocr_read_center((0, 0), (p.specs['w'], p.specs['h']), scale=False)
        text, _ = p.pocr.read_rec_lines((0, 0), (p.specs['w'], p.specs['h']), scale=False, verbose=0)
        pass
    t2 = datetime.now()
    print("Elapsed time {}s".format((t2-t1).total_seconds()))
    
    '''
    t1 = datetime.now()
    for i in range(rounds):
        # text = p.pocr.easyocr_read_center((0, 0), (p.specs['w'], p.specs['h']), scale=False)
        text, _ = p.pocr.read_rec_lines((0, 0), (p.specs['w'], p.specs['h']), scale=False, verbose=-1)
    t2 = datetime.now()
    '''
    print("Elapsed time {}s".format((t2-t1).total_seconds()))
        # print(text)
    print('No dict')
    # text = p.pocr.pocr_read_and_image((0, 0), (p.specs['w'], p.specs['h']), scale=False, output_type='dict')
    # print(text)
    for t in text:
        print(t)

    
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
