#!/bin/env python

from pokelib import TouchScreen as ts
p = ts(3002, "s7")

xs = 200
ys = 1625

for y in range(ys, ys + 10):
    print("{}:".format(y), end='')
    for x in range(xs, xs + 10):
        print(p.getRGB(x, y), end='')

    print()
