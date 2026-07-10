#!/bin/env python
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

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
    
    
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port)
    print("end")
if __name__ == "__main__":
    main()
