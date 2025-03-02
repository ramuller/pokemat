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
    pv = PixelVector(p, 10, 956, 900, 900, sy, "test")
    # pv.plot_start()
    # Create figure and axis
    # fig = plt.figure()
    # plt.ion()
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
    def plotter2(forever = True):    
        while forever:
            i = 0
            x, rgb = pc.rgb()
            for x in len(x-1):
                p1 = p.getRGB(xs, y)
                p2 = p.getRGB(xs, y + sy)
                dr = p2[0] - p1[0]
                dg = p2[1] - p1[1]
                db = p2[2] - p1[2]
                # xr_data[i] = y
                if False:
                    yr_data[i] = dr
                    yg_data[i] = dg
                    yb_data[i] = db
                else:
                    yr_data[i] = p1[0]
                    yg_data[i] = p1[1]
                    yb_data[i] = p1[2]
                
                i += 1
            # lr.set_xdata(xr_data)
            lr.set_ydata(yr_data)
            lg.set_ydata(yg_data)
            lb.set_ydata(yb_data)
            # ax.relim()  # Adjust limits if needed
            ax.autoscale_view()
            print("Thread")
            fig.canvas.draw()
            time.sleep(0.1)
            # plt.pause(1)

    def plotter(forever = True):
        while True:
            mx, my, b = p.get_mouse()
            print("Color under mouse {}".format(p.getRGB(mx, my)))

            print("mx {}, my {}".format(mx, my))
            
            if mx < 200:
                mx = 200
            elif mx > p.maxX - 200:
                mx = p.maxX - 201


            if mx < 200:
                my = 200
            elif my > p.maxY:
                my = p.maxY - 1
            
            print("mx {}, my {}".format(mx, my))
            # pv.x_set(mx - 200, mx + 200)
            pv.y_set(my, my)

            pv.update()
            rgbt = np.array(pv.rgb()[1])
            print(len(rgbt))
            rgbd = np.diff(rgbt, axis=0)
            ldr.set_ydata(rgbd[:,0])
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
            # plt.draw()
            # plt.pause(1)
            time.sleep(0.002)
            # print("Is pokestop {}".format(p.screen_is_pokestop()))
            # print("Mouse {}".format(p.get_mouse()))
    # plt.show()
    # plotter()
    
    bench = 10
    print("start update {} times".format(bench))
    for i in range(0, bench):
                print(bench)
                pv.update()
    print("end update {} times".format(bench))
    if True:
        print("Start threadding")
        import threading
        t = threading.Thread(target=plotter, daemon=True)
        t.start()
    else:
        # from matplotlib.animation import FuncAnimation
        # ani = FuncAnimation(fig, plotter, frames=100, interval=500, blit=True)
        #plt.ion()
        #plt.show()

        # plt.show()
        plotter(True)  # Start the thread
    # t.join()   # Wait for it to finish
    # while True:
    #     i = 0
    #     for y in range(ys, ye, sy):
    #         p1 = p.getRGB(xs, y)
    #         p2 = p.getRGB(xs, y + sy)
    #         delta = p2[0] - p1[0]
    #         x_data[i] = y
    #         y_data[i] = delta
    #         i += 1
    #     ax.clear()
    #     ax.plot(x_data, y_data)    
    #     plt.pause(1)
    # while True:
    #     i = 0
    #     for y in range(ys, ye, sy):
    #         p1 = p.getRGB(xs, y)
    #         p2 = p.getRGB(xs, y + sy)
    #         # delta = abs(p2[0] - p1[0])
    #         delta = p2[0] - p1[0]
    #         # print("Delta {}, Index {}".format(delta, (y-ys)/sy))
    #         # x_data = np.append(x_data, y)
    #         # y_data = np.append(y_data, delta)
    #         # y_data = np.append(y_data, 0)
    #         x_data[i] = y
    #         y_data[i] = delta
    #         i += 1
    #         # line.set_xdata(x_data)
    #         # line.set_ydata(y_data)
    #     ax.clear()
    #     ax.plot(x_data, y_data)    
    #     plt.pause(1)
        # ax.clear()
    # ani = animation.FuncAnimation(fig, animate, interval=500)
    # plt.ioff()
    # plt.ion()
    # plt.show()    
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
