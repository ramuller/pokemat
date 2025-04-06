#!/bin/env python
import argparse
import time
from time import sleep
import os

import logging
from pokelib import PixelVector
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from catch import catch 

import json
import sys
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpmath.tests.test_compatibility import xs



def read_text(port, phone_model):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
                
    print("Read text on \"{}\" on port {}", phone_model, port)
    global p
    p = TouchScreen(port, phone_model)
    p.read_text()
    
    
def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    read_text(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
