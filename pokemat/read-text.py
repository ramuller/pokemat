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

                
def read_text(port, tx, ty, tw, th):

            
    print("Start catching on  port {}",port)
    
    p = TouchScreen(port)
    
    
    text = p.pocr_read_line_center((tx, ty), (tw, th))
    
    print(text)
    
    return
        
            
    for i in range (0,100):
        print(f"{p.get_mouse():}")
        pos = p.get_mouse()
        text = p.pocr_read_line_center(pos, (tw, th))

        

def main():

    global args
    parser = PokeArgs()
    
    parser.add_argument("tx", type=int, help="Text x")
    parser.add_argument("ty", type=int, help="Text y")
    parser.add_argument("tw", type=int, help="Text widht")
    parser.add_argument("th", type=int, help="Text high")
    
    args = parser.parse_args()

    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    read_text(args.port, args.tx, args.ty, args.tw, args.th)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
