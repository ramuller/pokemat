#!/bin/env python

from pokelib import TouchScreen as ts
import math
from time import sleep
p = ts(3001, "s7")

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
end = 440
step = 12
radius = 180 
off_x = 500
off_y = 1350

def run_code(right = True):
    start = -60
    end = 460
    step = 8
    radius = 250 
    off_x = 500
    off_y = 1250
    off_y = 900
    x = getX(start, radius, off_x) 
    y = getY(start, radius, off_y)
    p.tapDown(x, y)
    a  = start + step
    b = 0.0
    while a < end + step:
        a = a + step + int(a / 60)
        b = b + 0.2
        t = radius + int(b)
        radius = t
         # for a in range(start + step, end + step, step):
        sx = x
        sy = y
        
        if right:
            x = off_x + getX(a, radius)
        else:  
            x = off_x - getX(a, radius)
        y = getY(a, radius, off_y) # - a * 2
        # print("x = {}".format(x))
        p.moveCursor(int(sx), int(sy), int(x), int(y))
        # canvas.create_line(sx, sy, x, y)
        # canvas.update()
        sleep(0.015)

    y1 = y
    for y2 in range(int(y) - 10 , int(y) - 100, -10):
        p.moveCursor(int(x), int(y1), int(x), int(y2))
        y1 = y2
    
    p.tapUp(x, y)

run_code(right = False)    

# checkColor()
# p.typeString("\\azxy   openshift")
# p.selectAll()
# p.swipe(150, 700, 800, 1750)
# p.attack()
# p.catchPokemon()
# p.scroll(0, -350)
# p.scroll(0, -350)
# p.scroll(0, -350)
