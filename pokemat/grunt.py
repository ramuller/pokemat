#!/bin/env python
import argparse
import threading
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import WatchDog
from catch import catch 

import json
import sys
from sys import exit
from datetime import datetime

def is_grunt_in_gym(p):
    if True \
        and p.color_match(861, 1917, 61, 64, 63) \
        and p.color_match(67, 1925, 61, 64, 63):
        return True
    if True \
        and p.color_match(902, 1949, 147, 100, 232) \
        and p.color_match(450, 1949, 147, 100, 232) \
        and p.color_match(100, 1949, 147, 100, 232):
        return True
    if p.color_match(585, 826, 211, 90, 49) \
            and p.color_match(659, 830, 209, 88, 47) \
            and p.color_match(614, 876, 205, 88, 50) \
            and p.color_match(555, 871, 205, 88, 50):
        return True
    if True \
            and p.color_match(468, 804, 212, 91, 50) \
            and p.color_match(529, 855, 206, 90, 49) \
            and p.color_match(463, 871, 203, 89, 50):
        return True
    if True \
            and p.color_match(404, 857, 206, 90, 49) \
            and p.color_match(418, 814, 211, 90, 49):
        return True
    
    if True \
            and p.color_match(404, 857, 206, 90, 49) \
            and p.color_match(418, 814, 211, 90, 49):
        return True
    if True \
            and p.color_match(390, 814, 206, 90, 49) \
            and p.color_match(390, 857, 206, 90, 49) \
            and p.color_match(390, 900, 205, 80, 49)\
            :
        return True
    
    # print("No grunt")
    return False

def is_red_in_the_sky(p):
    if p.color_match(465, 394, 155, 64, 61):
        print("bingo")
        sys.exit(0)
      
def rotate(phone):
    phone.scroll(0, 800, start_y=200, start_x = 980, stop_to=0.1)
    phone.scroll(0, 800, start_y=200, start_x = 980, stop_to=0.1)
    # phone.scroll(0, 800, start_y=200, start_x = 980, stop_to=0.1)


def scan_sky(phone, print, no_grunt):
    gy = 500
    while gy < 880 and no_grunt:
        x = 100
        while x < 900 and no_grunt:
        # if phone.color_match(x, gy, 73, 73, 75):
            if phone.color_match(x, gy, 166, 73, 66) \
                    or phone.color_match(x, gy, 152, 60, 60) \
                    or phone.color_match(x, gy, 180, 90, 70) \
                    or phone.color_match(x, gy, 225, 130, 115):
                print("Grunt R found")
                phone.tap_screen(x, gy + 250)
                time.sleep(2)
            if is_grunt_in_gym(phone) \
                    or phone.color_match(868, 197, 241, 247, 240) \
                    or phone.color_match(506, 849, 206, 92, 51):
                print("In stop")
                no_grunt = False
            x = x + 35
        print("Search grunt {}, {}".format(x, gy))
        watch_dog.reset()
        gy = gy + 20
    
    return no_grunt

def grunt(port, phone):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Looking for grunt \"{}\" on port {}", phone, port)
    phone = TouchScreen(port, phone)
    try:
        phone.goHome()
    except:
        pass
    # phone.dno_gruntoBattle()
    no_grunt = False
    no_grunt = True
    while no_grunt:
        # rotate(phone)
        # if is_red_in_the_sky(phone):
        #     no_grunt = False     
        no_grunt = scan_sky(phone, print, no_grunt)
        if not no_grunt:
            time.sleep(1) 
            if is_grunt_in_gym(phone):
                no_grunt = False
        else:
            phone.goHome()
            rotate(phone)
   
    try:
        phone.waitMatchColorAndClick(463, 855, 203, 79, 41, time_out_ms = 1500)
    except:
        pass
    time.sleep(1)
    oponent = False
    try:
        i = 20
        no_grunt = True
        go_out = 2
        while i > 0:
            i = i -1
            print("Wait opponent and spin{}".format(i))       
                
            phone.spinDisk()
            if phone.color_match(506, 849, 206, 92, 51, threashold = 20) or \
                   phone.color_match(506, 880, 206, 92, 51, threashold = 20) or \
                   phone.color_match(611, 880, 206, 92, 51, threashold = 20) or \
                   phone.color_match(620, 880, 206, 92, 51, threashold = 20):
                phone.tap_screen(506, 849)
                oponent = True
                i = 0
                break
            if phone.color_match(498, 1824, 235, 242, 242):
                phone.tap_screen(498, 1824)
            if phone.isHome():
                i = 0
            sleep(1)
        print("oponent {}".format(oponent))
        if not oponent:
            print("No opponent found")
            watch_dog.kill()
    except Exception as e:
        print(e)
        pass
    print("Wait battle")
    
    i = 10
    while i > 0:
        try:    
            phone.waitMatchColorAndClick(348, 1554, 151, 217, 149, threashold=20, time_out_ms = 1000)
            print("Wait for ?")
            i = 0
        except:
            phone.tap_screen(348, 1000)
            i = i -1
    time.sleep(2)
    phone.tap_screen(388, 1552)
    time.sleep(1)
    phone.tap_screen(388, 1552)
    
    phone.waitMatchColor(350, 1771, 155, 222, 146)
    time.sleep(5)
    print("Select other party")    
    phone.tap_screen(970, 1452)
    time.sleep(2)
    print("Wait go battle")
    phone.tap_screen(500, 1800)
    
    # try:
    #     phone.waitMatchColorAndClick(338, 1779, 162, 220, 148, threashold=20, time_out_ms = 15500)
    # except:
    #     pass
    watch_dog.reset()
    
    startTime = datetime.now()
    while not phone.black_screen():
        if ((datetime.now() - startTime).total_seconds() * 1000) > 10000:
            break
        print("Wait black screen")
        time.sleep(0.05)
    while phone.black_screen():
        if ((datetime.now() - startTime).total_seconds() * 1000) > 3000:
            break
        print("Wait black screen")
        time.sleep(0.05)
    print("do battle")
    phone.doBattle()
    
    # Wait for trainer
    for i in range(1,10):
        try:
            phone.waitMatchColorAndClick(305, 1773, 137, 216, 153, time_out_ms = 2000)
            break
        except:
            phone.tap_screen(305, 1773)
        pass
    phone.tap_screen(512, 873) 

    sleep(6)
    print("Try to catch")
    watch_dog.reset()
    catch(port, phone, berry = "g")     
    print("Try to catch")
    phone.goHome()  
    phone.goHome()
    phone.healAll()  

def wd_callback():
    print("Watchdog timeout strike just exit {}".format(threading.main_thread().native_id))
    watch_dog.kill()
       
def main():
    global watch_dog 
    watch_dog = WatchDog(time_out = 240, _callback = wd_callback)
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
    try:
        grunt(args.port, args.phone)
    except Exception as e:
            print("Upps something went wrong but who cares?: {}", e)    # ts.click(200,200)
    print("end")
    watch_dog.kill()
    # ts.click(200,y)
if __name__ == "__main__":
    main()
