#!/bin/env python
import argparse
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

def action(port, phone, text):
      
    print("Start sending text on  \"{}\" on port {} '{}'".format(port, phone, text))
    p = TouchScreen(port, phone)
    if args.select:
        p.tap_screen(510, 375)
    sleep(0.5)
    p.text_line_ok(text)
    
def main():

    parser = PokeArgs()
    global args
    parser.add_argument("text", type=str, help="text to send")
    parser.add_argument("-s", "--select", action='store_true', help='select pokemon')    
    args = parser.parse_args()
    global log 
    if args.port != "NA":
        phone_port = args.port
    else:
        phone_port = os.getenv("PHONE_PORT")
    if phone_port == "NA" or phone_port == "":
        print("Mssing phone port, use flag -p/--phone or define environment variable PHONE_PORT")
        os.exit(1)
    log = logging.getLogger("foo")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    print("TEXT {}".format(args.text))
    action(phone_port, args.phone, args.text)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
