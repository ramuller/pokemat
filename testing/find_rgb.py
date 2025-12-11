#!/bin/env python
import argparse
import time
from time import sleep
import os
import sys
import logging
import math
import cv2
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
    rounds = 1
    p = TouchScreen(port)

    t1 = datetime.now()
    
    img = p.sc.scan_image()
    ir = p.sc.scan_image(channel="red")    
    ig = p.sc.scan_image(channel="green")
    ib = p.sc.scan_image(channel="blue")
    
    p.sc.schow_image(img)
    p.sc.schow_image(ir)
    p.sc.schow_image(ig)
    p.sc.schow_image(ib)
    
    
    t2 = datetime.now()
    print("Elapsed time {}s".format((t2-t1).total_seconds()))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
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
