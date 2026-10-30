#!/bin/env python
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import ExPokeNoHomeError
from pokelib import PokeArgs
from pokelib import PokeLogger
from pokelib import GPSControl
from pokelib.class_buttons import CButtGymMyTeam

import defeat_gym

import json
import sys
from datetime import datetime
from catch import catch
from heal import heal
from reconnect import connect

gps_speed = 0.0
def search_target(phone):

    if args.defeat_gym:
        gps_speed = GPSControl().get_speed()

    while True:
        # for y in range(1300, 600, -50):
        sy = phone.rel_y(0.65)
        ey = phone.rel_y(0.3)
        dy = phone.max_y() // 40 * -1
        for y in range(sy, ey, dy):
        # for y in range(1300, 800, -50):
        # for y in range(1300, 1049, -50):
            # phone.color_show(500, y)           
            phone.tap_screen(phone.rel_x(0.5), y, scale=False)
            sleep(0.17)
            if phone.screen.get_current_screen() != 'home':
                print("Not home")
                sleep(3)
                print("check egg")
                if phone.egg_handle():
                    print("Egg handled")
                    # return "egg"
                elif phone.screen_is_catch_pokemon():
                    print("Pokemon screen")
                    # phone.screen_go_to_home()
                    return "pokemon",y
                elif phone.screen.is_in_pokestop():                    
                    print("Found pokestop")
                    return "pokestop",y
                elif phone.screen.is_in_gym():
                    print("Found gym to defeat")
                    return "gym-defeat",y
                else:
                    print("Something else go home")
                    phone.screen.go_home()
                    print("Unknown screen, go home and rotate")
                    phone.rotate()
        sleep(0.75)
        print("Nothing found, rotate")
        phone.rotate()
    return "nothing", y
            


def auto_catch(phone):
    action_count = 0
    spins_after_egg  = 0
    spins_after_poke = 0
    while True:
        not_home = True
        # phone.screen_go_to_home()
        phone.screen_go_to_home()
        if args.autoconnect:
            connect(phone)
        target,y_coord = search_target(phone)
        if target == "egg":
            spins_after_egg += 1
        elif target == "pokestop" and spins_after_egg > 0:
            print(f"After egg spin disk {spins_after_egg} times")
            phone.spin_disk()
            spins_after_egg -= 1
            phone.screen_go_to_home()
            sleep(0.5)
        elif target == "pokemon":
            print('Found pokemon')
            action_count += 1                
            if args.no_catch:
                print('No catch today')
                phone.screen.go_home()
            else:
               catch(phone, distance = 5, berry = args.berry, max_tries = 7, span = 2)
            phone.rotate()
            spins_after_poke += 1
        elif target == "gym-defeat":
            print("Handle gym")
            if args.defeat_gym:
                running = GPSControl().get_running()
                GPSControl().stop()
                action_count += 1
                if defeat_gym.defeat_gym(args.port, phone=phone, y_coord=y_coord):
                    defeat_gym.add_pokemon_to_gym(phone, max_cp=2000, min_cp=1000)
                if running:
                    GPSControl().start()
                phone.heal_all()
            else:
                if CButtGymMyTeam(phone).search(retries=1):
                    defeat_gym.add_pokemon_to_gym(phone, max_cp=2000, min_cp=1000)
            phone.screen.go_home()
            phone.rotate()

        elif target == "pokestop":
            if args.spin:
                action_count += 1
                phone.spin_disk()
            phone.screen.go_home()
            phone.rotate()
        elif target == "egg":
            pass
        else:
            phone.rotate()
        if args.once and action_count > 0:
            phone.screen_go_to_home()
            return

def auto_hatch(phone):
    print("Hatch mode")
    spins = 2
    phone.screen.go_home()
    while True:
        target = search_target(phone)
        if target == "egg":
            spins = 2
        elif target == "pokestop" and spins > 0:
            print(f"After egge spin disk {spins} times")
            phone.spin_disk()
            spins -= 1
        phone.screen_go_to_home()
        
def action(port):
    print("Change trainers on port {}", port)

    phone = TouchScreen(port)
    
    if args.mode == "catch":
        auto_catch(phone)
    elif args.mode == "hatch":
        auto_hatch(phone)
    
def main():

    parser = PokeArgs()
    parser.add_argument("-b", "--berry", action="store", required=False, default="a", \
                        help="Name os the phone model. Check phones.json.")
    parser.add_argument("-a", "--autoconnect", action='store_true', required=False, default=False, \
                        help="Connnect to autocatch.")
    parser.add_argument("-r", "--range", action="store", required=False, default=0, \
                        help="Vary distance by range.")
    parser.add_argument("-n", "--no-catch", action='store_true', required=False, default=False, \
                        help="Do NOT catch pokemon")    
    parser.add_argument("-D", "--deafeat", action='store_true', required=False, default=False, \
                        help="Defeat gyms")    
    parser.add_argument("-m", "--mode", action='store', required=False, default="catch", \
                        help="Mode catch or only hatch eggs (hatch")    
    parser.add_argument("-s", "--spin", action='store_true', required=False, default=False, \
                        help="Spin pokestops")    
    parser.add_argument("-o", "--once", action='store_true', required=False, default=False, \
                        help="ONCE do it only once")
    parser.add_argument("-d", "--defeat-gym", action='store_true', required=False, default=False, \
                        help="Defeat gyms")
    parser.add_argument("-L", "--leave-in-gym", action='store_true', required=False, default=False, \
                        help="Leave pokemon in gym after defeat givea number for MAX CP")
        
    global args
    args = parser.parse_args()
    
    global log 
    
    logger = PokeLogger("autocatch")
    log = logger.get_logger()
    logger.set_level(level=args.loglevel)
    # logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    while True:
        try:
            action(args.port)

        except ExPokeNoHomeError as e:
            print("Problems to find home...")
            pass
        
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
