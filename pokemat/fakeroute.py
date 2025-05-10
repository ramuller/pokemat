#!/bin/env python

import argparse
from pokelib import TouchScreen as ts
import math
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--location", action="store", required=True, default="s7", \
                        help="Name os the phone model. Check phones.json.")
args = parser.parse_args()

for ph in range(1,7):
    try:
        p = ts(3000 + ph, "s7")
        # p.tap_screen(450,140)
        p.tap_screen(690,140)
        sleep(0.5)
        p.tap_screen(430, 1029)
        sleep(0.5)
        p.text_line_ok(args.location)
        sleep(0.5)
        p.tap_screen(822, 798)
        sleep(1)
        # p.tap_screen(116, 1738)
        # sleep(1)
        # p.tap_screen(116, 1738)
    except:
        pass

