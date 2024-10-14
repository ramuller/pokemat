#!/bin/env python

from pokelib import TouchScreen as ts
p = ts(3002, "s7")

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

# checkColor()
# p.typeString("\\azxy   openshift")
# p.selectAll()
# p.swipe(150, 700, 800, 1750)
# p.attack()
p.catchPokemon()