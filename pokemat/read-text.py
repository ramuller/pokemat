#!/usr/bin/python


#!/bin/env python
import time
from time import sleep
import os
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

import json
import sys
from datetime import datetime
from mercurial.hgweb.common import continuereader
from random import randrange
import matplotlib.pyplot as plt

                
def read_text(port, xs, xe, ys, ye):

            
    print("Start reading on  port {}",port)
    if xs != 0:
        p.ocr.startx = xs

    p = TouchScreen(port)
    text,image = p.ocr.read()
    for t in text:
        print(t)
    if args.show:
        plt.imshow(image, cmap='gray', vmin=0, vmax=255)
        plt.title(f'Grayscale Bitmap')
        plt.axis('off')
        plt.show()

    return
        
            
    for i in range (0,100):
        print(f"{p.get_mouse():}")
        pos = p.get_mouse()
        text = p.ocr_read_line_center(pos, (tw, th))

        

def main():

    global args
    parser = PokeArgs()
    parser.add_argument("-s", "--show", action="store_true", required=False, default=0, \
                        help="Vary distance by span.") 
    parser.add_argument("--xs", default=0, action="store_true", required=False, help="Text x start")
    parser.add_argument("--ys", default=0, action="store_true", required=False, help="Text y start")
    parser.add_argument("--xe", default=0, action="store_true", required=False, help="Text x end")
    parser.add_argument("--ye", default=0, action="store_true", required=False, help="Text y end")
    
    args = parser.parse_args()
    print(args.show)
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    read_text(args.port, args.xs, args.ys, args.xe, args.ye)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
