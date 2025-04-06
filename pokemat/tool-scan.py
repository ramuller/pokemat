#!/bin/env python
import argparse
import time
from time import sleep
import os

import logging
from pokelib import PixelVector
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from catch import catch 

import json
import sys
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpmath.tests.test_compatibility import xs



def scan_line(port, phone_model):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    
        
    print("Change trainers \"{}\" on port {}", phone_model, port)
    global p

    xs = 870
    xe =1
    ys = 1500
    ye = 1900
    sy = 4
    def print_step():
        print("Step {}".format(sy))
    print_step()
    p = TouchScreen(port, phone_model)

    # pv = PixelVector(p, 770, 956, 1850, 1850, 3 , "test")
    #pv = PixelVector(p, 10, 990, 900, 900, sy, "test")
    pv = p.get_vector_object_left_right()
    pv.x_set(10, 990)
    pv.update()
    # pv.plot_start()
    # Create figure and axis
    # fig = plt.figure()
    plt.ion()
    fig,ax = plt.subplots(figsize=(16, 6))
    rgb = np.column_stack((pv.rgb()[0], pv.rgb()[1]))
    rgbt = np.array(pv.rgb()[1])
    print(len(rgbt))
    rgbd = np.diff(rgbt, axis=0)
    print(len(np.diff(rgbt, axis=0)))
    
    ldr, = ax.plot(rgb[:, 0][:-1], rgbd[:,0], 'y-', label='Red')
    lr, = ax.plot(pv.rgb()[0], pv.red()[1], 'r-', label='Red')
    lg, = ax.plot(pv.rgb()[0], pv.green()[1], 'g-', label='Green')
    lb, = ax.plot(pv.rgb()[0], pv.blue()[1], 'b-', label='Blue')
    # plt.show()
    plt.autoscale(axis='x') # ax.set_xlim(ys, ye)
    ax.set_ylim(-255, 255)
    ax.grid()
    def plotter(forever = True):
        while True:
            mx, my = p.get_mouse()
            print(p.screen_is_defeat_gym())

            if mx < 200:
                mx = 200
            elif mx > p.maxX - 200:
                mx = p.maxX - 201

            pv.x_set(mx, mx + 140)

            if mx < 200:
                my = 200
            elif my > p.maxY:
                my = p.maxY - 1
            
            # pv.x_set(mx - 200, mx + 200)
            pv.y_set(my, my)

            pv.update()
            print("mx {}, my {}, len {}".format(mx, my, pv.len))            
            # all channels
            if False:
                rgbt = np.array(pv.rgb()[1])
                print("rgbt len {}".format(len(rgbt)))
                delta = np.diff(rgbt, axis=0)
                ldr.set_ydata(delta[:,0])
            else:
                delta = np.diff(pv.red()[1])
                ldr.set_ydata(delta)
            print((np.abs(delta) > 80).sum())
            ldr.set_xdata(pv.red()[0][:-1])
            # ldr.set_xdata(range(mx - 200, mx + 199, 3))
            #     ldr.set_xdata(pv.rgb()[1].pop(0))

            lr.set_ydata(pv.red()[1])
            lr.set_xdata(pv.red()[0])
            lg.set_ydata(pv.green()[1])
            lg.set_xdata(pv.green()[0])
            lb.set_ydata(pv.blue()[1])
            lb.set_xdata(pv.blue()[0])
            # lg.set_ydata(pv.green()[1])
            # lb.set_ydata(pv.blue()[1])
            # ax.autoscale_view()
            plt.autoscale(axis='x') # ax.set_xlim(ys, ye)
            fig.canvas.draw()
            #ax.grid()
            plt.draw()
            plt.pause(0.9)
            # time.sleep(0.1)
            # print("Is pokestop {}".format(p.screen_is_pokestop()))
            # print("Mouse {}".format(p.get_mouse()))
    # plt.show()
    plotter()
    
    bench = 2
    print("start update {} times".format(bench))
    for i in range(0, bench):
                print(bench)
                pv.update()
    print("end update {} times".format(bench))
    print("Start threadding")
    import threading
    t = threading.Thread(target=plotter, daemon=True)
    t.start()
    plt.show()
    while False:
        print("Hello")
        time.sleep(1)
        # plt.draw()    
    
    
def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", required=True, \
                        help="TCP port for the connection.")
    parser.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                        help="Name os the phone model. Check phones.json.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    scan_line(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
