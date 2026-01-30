#!/bin/env python
import math
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

# import pytesseract
# import easyocr
from time import sleep
import json
import sys
from datetime import datetime


def action(port, arg = None):
        
    print("Start fakegps port {}",port)
    global p
    phones = []
    f = int(args.range.split('-')[0])
    l = int(args.range.split('-')[1])
    for i in range(f, l):
        try:
            p = TouchScreen(3000 + i)
            phones.append(p)
        except:
            print(f'No phone {p} exit!')

    print('Start App')
    for p in phones:
        p.buttons.i_fake_app.press()

    sleep(1)
    print('Press 3dot')
    for p in phones:
        p.buttons.i_fake_3dot.press()

    sleep(1)

    print('Press routes')
    for p in phones:
        p.buttons.text_only.press('Routes', xs=p.rel_x(0.5), ye=p.rel_y(0.5))

    sleep(1)

    print(f'Select route {args.route}')
    for p in phones:
        b = p.buttons.text_only.press(f'.*{args.route}.*', 
                                      process=True)


    startTime = datetime.now()
    
    
def main():

    parser = PokeArgs()
    parser.add_argument('--route', action='store', required=False, default='nuksio', \
                        help='route start.')
    parser.add_argument('--range', action='store', required=False, default='1-10', \
                        help='route start.')
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
