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
from mpmath.tests.test_compatibility import xs



def scan_line(port, phone_model):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Change trainers \"{}\" on port {}", phone_model, port)
    global p

    xs = 870
    ys = 1500
    ye = 1900
    sy = 4
    def print_step():
        print("Step {}".format(sy))
    print_step()
    p = TouchScreen(port, phone_model)
    plt.ion()

    pv =PixelVector(p, 870, 870, 1500, 1900, 4, "test")
    pv.plot_start()
    # Create figure and axis
    fig, ax = plt.subplots()
    # x_data = np.array([])
    # y_data = np.array([])
    x_data, y_data = [], []

    # Plot an initial empty line
    line, = ax.plot([], [], 'r.-', label='Live Data')
    # line, = ax.plot(x_data, y_data,  marker='o', linestyle='-', color='b', label='Live Data')
    ax.set_xlim(0, ye - ys)
    ax.set_xlim(ys, ye)
    # .set_xlim(0, 10000)
    ax.set_ylim(-255, 255)
    # ax.set_xlabel('X-axis')
    # ax.set_ylabel('color delta')
    # ax.legend()
    ax.grid()
    # plt.gca().autoscale(axis='x')
    x_data, y_data = [], []
    for y in range(ys, ye, sy):
            x_data.append(y)
            y_data.append(0)
    while True:
        i = 0
        for y in range(ys, ye, sy):
            p1 = p.getRGB(xs, y)
            p2 = p.getRGB(xs, y + sy)
            # delta = abs(p2[0] - p1[0])
            delta = p2[0] - p1[0]
            # print("Delta {}, Index {}".format(delta, (y-ys)/sy))
            # x_data = np.append(x_data, y)
            # y_data = np.append(y_data, delta)
            # y_data = np.append(y_data, 0)
            x_data[i] = y
            y_data[i] = delta
            i += 1
            line.set_xdata(x_data)
            line.set_ydata(y_data)
            # ax.relim()  # Recompute limits
            # ax.autoscale_view()  # Adjust view
    
            plt.draw()
            # plt.pause(0.002)  # Pause for visibility
        print("Screen {}".format(p.screen_get_type()))
        plt.pause(1)
        # ax.clear()
    plt.ioff()
    plt.show()    
    
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
