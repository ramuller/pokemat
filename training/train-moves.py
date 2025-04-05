#!/usr/bin/env python

import tkinter
import requests
import math
import json
import sys
from tkinter.constants import *
from time import sleep

from pokelib import TouchScreen as ts

# p = ts(3005, "s7")

def getX(d, r, offset=0):
    return math.cos(math.radians(d)) * float(r) + float(offset)

def getY(d, r, offset=0):
    return math.sin(math.radians(d)) * float(r) + offset

def run_code():
    start = 0
    end = 180
    step = 5
    radius = 100 
    off_x = 250
    off_y = 700 
    x = getX(start, radius, off_x) 
    y = getY(start, radius, off_x)
    for a in range(start + step, end + step, step):
        sx = x
        sy = y
        
        x = getX(a, radius, off_x) 
        x = a
        y = getY(a * 2, radius, off_x)
        print("x = {}".format(x))
        canvas.create_line(sx, sy, x, y)
        canvas.update()
        sleep(0.001)
    for a in range(end - step, start - step, -step):
        sx = x
        sy = y
        
        x = getX(a, radius, off_x) 
        x = a
        y = getY((a + 90) * 2, radius, off_x)
        print("x = {}".format(x))
        canvas.create_line(sx, sy, x, y)
        canvas.update()
        sleep(0.001)
    # eclipse
    # Parameters for the ellipse
    start = 0
    end = 360
    step = 10
    h, k = 300, 600  # Center of the ellipse
    a, b = 50,150  # Semi-major and semi-minor axes
    
    sx = h + a * math.cos(math.radians(start))
    sy = k + b * math.sin(math.radians(start))
    sx = getX(start, a)
    sy = getY(start, b)
    for aa in range(start + step, end + step, step):
        y = getY(aa, b)
        x = getX(aa, a) + y /2
        canvas.create_line(sx + h, sy + k, x + h, y + k)
        sx = x
        sy = y
        canvas.update()
        sleep(0.01)

    return
    for o in range(100,450,20):
        r = requests.get('http://localhost:3005/v1/snip:{},400,28,28'.format(o,o))
        snip = r.json()
        for y in range(0, snip["hight"]):
            for x in range(0, snip["width"]):
                c = snip["pixels"][snip["width"] * y + x]
                color = "#%02x%02x%02x" % (c,c,c)  # Light blue colo
                # print("Color {}",format(color))
                canvas.create_line(200 + x,600 + y, 201 + x, 600 + y, fill=color)
        canvas.update()
        sleep(0.1)
    sys.exit(0)
    start = 0
    end = 210
    step = 5
    radius = 100 
    off_x = 250
    off_y = 700 
    x = getX(start, radius, off_x) 
    y = getY(start, radius, off_x)
    for a in range(start + step, end + step, step):
        sx = x
        sy = y
        
        x = getX(a, a, off_x) 
        #x = a
        y = getY(a , radius, off_x)
        print("x = {}".format(x))
        canvas.create_line(sx, sy, x, y)
        canvas.update()
        sleep(0.01)
    
    


tk = tkinter.Tk()
frame = tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)

tk.geometry('600x1200+1+900')
tk.title('Canvas Demo')

canvas = tkinter.Canvas(tk, width=584, height=1024, bg='white')
canvas.pack(anchor=tkinter.CENTER, expand=True)
label = tkinter.Label(frame, text="Hello, World")
label.pack(fill=X, expand=1)
button = tkinter.Button(frame,text="Exit",command=tk.destroy)
button.pack(side=BOTTOM)

tk.after(1000, run_code)

points = (
    (50, 150),
    (200, 350),
)

# r = requests.get('http://localhost:3005/v1/snip:100,720,50,50')
# snip = r.json()
# print("width {}, heigth {}".format(snip["width"],snip["hight"]))

# canvas.create_oval(*points, fill='purple')
tk.mainloop()
