#!/bin/env python

from pokelib import TouchScreen as ts
from pokelib import WatchDog as wd
import math
from time import sleep

def callback():
    print("Callback")

ps = {}
for p in range(3003,3006):
    ps[p] = ts(p)
    ps[p].doBattle()
sys.exit(0)
p.screen_home()
p.healAll()
sys.exit(0)
a=wd(time_out = 1, _callback = callback)
sleep(3)
a.reset()
sleep(3)
sleep(3)
a.stop()

353
363
