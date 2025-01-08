#!/bin/env python

from pokelib import TouchScreen as ts
from pokelib import WatchDog as wd
import math
from time import sleep

def callback():
    print("Callback")

a=wd(time_out = 1, _callback = callback)
sleep(3)
a.reset()
sleep(3)
sleep(3)
a.stop()

353
363
