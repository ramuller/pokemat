#!/bin/env python

import argparse
from pokelib import TouchScreen as ts
import math
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--location", action="store", required=True, default="s7", \
                        help="Name os the phone model. Check phones.json.")
args = parser.parse_args()

for ph in range(2,6):
    p = ts(3000 + ph, "s7")
    p.tapScreen(690,140)
    sleep(1)
    p.tapScreen(430, 1029)
    sleep(1)
    p.typeString(args.location)
    sleep(1)
    p.tapScreen(822, 798)

