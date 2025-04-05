#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal

import json
import sys
from datetime import datetime

def action(port, phone, text):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start testing on  \"{}\" on port {}", port, phone, text)
    p = TouchScreen(port, phone)
    p.tap_screen(510, 375)
    sleep(0.5)
    p.typeString(text)
    
def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=False, default="NA", \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("text", type=str, help="text to send")
    global args
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
