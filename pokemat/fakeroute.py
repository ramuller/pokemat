#!/bin/env python

from pokelib import TouchScreen as ts
import math
from time import sleep

for ph in range(2,3):
    p = ts(3000 + ph, "s7")
    p.tapScreen(690,140)
    sleep(1)
    p.tapScreen(430, 1029)
    sleep(1)
    p.typeString("60.169434684107365,24.933319464325905")
    sleep(1)
    p.tapScreen(822, 798)
