#!/bin/env python

from pokelib import TouchScreen as ts
import math
from time import sleep
p = ts(3003, "s7")

xs = 200
ys = 1625

def checkColor():
    for y in range(ys, ys + 100, 4):
        print("{}:".format(y), end='')
        for x in range(xs, xs +1):
            print(p.getRGB(x, y), end='')
            
        print()

def doubleClick():
    p.tapScreen(25, 1100)
    p.tapScreen(25, 1100)

def getX(d, r, offset=0):
    return math.sin(math.radians(d)) * float(r) + float(offset)

def getY(d, r, offset=0):
    return math.cos(math.radians(d)) * float(r) + offset

def multiRet(for_ret = False):
    return for_ret, 1, 2
start = 0
end = 460
step = 8
radius = 200 
off_x = 500
off_y = 1350

def run_code():
    start = 0
    end = 460
    step = 8
    radius = 200 
    off_x = 500
    off_y = 1350
    x = getX(start, radius, off_x) 
    y = getY(start, radius, off_y)
    p.tapDown(x, y)
    a  = start + step
    b = 0.0
    while a < end + step:
        a = a + step # + int(b)
        b = b + 0.2
        t = radius + int(b)
        radius = t
         # for a in range(start + step, end + step, step):
        sx = x
        sy = y
        
        x = getX(a, radius, off_x) 
        y = getY(a, radius, off_y)
        print("x = {}".format(x))
        p.moveCursor(int(sx), int(sy), int(x), int(y))
        # canvas.create_line(sx, sy, x, y)
        # canvas.update()
        sleep(0.008)
    p.tapUp(x, y)
run_code()    

# checkColor()
# p.typeString("\\azxy   openshift")
# p.selectAll()
# p.swipe(150, 700, 800, 1750)
# p.attack()
# p.catchPokemon()
# p.scroll(0, -350)
# p.scroll(0, -350)
# p.scroll(0, -350)
