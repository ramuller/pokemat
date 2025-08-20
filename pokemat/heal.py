#!/bin/env python
import time
from time import sleep
import os
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
import logging

import json
import sys
from datetime import datetime


def heal(port):

    print("Change trainers on port {}", port)
    global phone
    phone = TouchScreen(port)
    phone.screen_go_to_home()
    phone.heal_all()
    
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    # global args
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    heal(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
