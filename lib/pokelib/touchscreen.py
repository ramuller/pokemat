import requests
import logging
import threading
import time
import sys
import os
import signal
from datetime import datetime
from time import sleep
import random
import math
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import re

log = logging.getLogger("pokelib")
from .pixelvector import PixelVector
from .ocr import Ocr
from .database import Database as db_p
from pokelib import ExPokeLibError, ExPokeNoHomeError, ExPokeLibFatal

import signal
import functools
from pprint import pprint
import inspect

'''
Timeout decorator return from what ever funtion after timeout
Decorated function needs a paramter to_ms=<float> to define timeout
'''
class ExPokeTimeoutHandler(Exception):
    pass


def timeout(seconds):
    def decorator(func):
        # def _handle_timeout(signum, frame):
        #    raise ExPokeTimeoutHandler(f"Function '{func.__name__}' timed out after {seconds} seconds")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Set the signal handler and a timer
            # signal.signal(signal.SIGALRM, _handle_timeout)
            # signal.alarm(seconds)
#            try:
                return func(*args, **kwargs)
#            finally:
#                signal.alarm(0)  # Disable the alarm
        return wrapper
    return decorator

def poke_timeout(to_ms=10000):
    def decorator(func):
        # def _handle_timeout(signum, frame):
        #     raise ExPokeTimeoutHandler(f"Function '{func.__name__}' timed out after {seconds} seconds")

        def wrapper(*args, **kwargs):
            # Set the signal handler and a timer
            try:
                to_ms = kwargs["to_ms"]
            except KeyError as e:
                to_ms = 0
                
            print("args {}".format(args))
            pprint("kwargs {}".format(kwargs))
            startTime = datetime.now()
            ret = False
            # try:
            while ret == False:
                ret = func(*args, **kwargs)
                # self.log.debug("DT {}".format((datetime.now() - startTime).total_seconds() * 1000))
                if ((datetime.now() - startTime).total_seconds() * 1000) > to_ms:
                    return ret
            if ret == False:
                raise ExPokeTimeoutHandler(f"Function '{func.__name__}' timed out after {to_ms} ms")
            #    pass
        return wrapper
        
    return decorator

class TouchScreen:
    maxX = 0
    maxY = 0
    def __init__(self, tcpPort, name = "unknown", scaleX = 0.576, scaleY = 0.512):
        self.log = logging.getLogger(name)
        self.log.info("Pokemat phone : {}".format(tcpPort))
        self.url = "http://localhost:{}/v1".format(tcpPort)
        self.my_name = None
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.httpErrorCount = 0
        self.maxX = 1000
        self.maxY = 2000
        self.vector_left_right = PixelVector(self, 850, 850 + 201, 1850, 1850, 3, "left_right")
        self.vector_top_down = PixelVector(self, 50, 50, 100, 100 + 201, 3, "top_down")
        self.vector = PixelVector(self, 50, 50, 100, 100 + 201, 3, "top_down")
        self.reader = None
        for self.min_width in range(1,100):
            tb = self.screen_capture_bw((100,100), (self.min_width, 100))
            if tb["width"] == 1:
                break
        for self.min_hight in range(1,100):
            tb = self.screen_capture_bw((100,100), (100, self.min_hight))
            if tb["hight"] == 1:
                break
        pass

    def get_vector_object_left_right(self):
        return self.vector_left_right
    
    def scaleXY(self, x, y):
        x = x * self.scaleX
        y = y * self.scaleY
        return int(x), int(y)
        
    def write_to_phone(self, cmd):
        self.log.debug("Send CMD - {}".format(cmd))
        # print("Send CMD - {} url {}".format(cmd, self.url))
        try:
            return requests.get("{}/{}".format(self.url, cmd))
        except Exception as e:
            raise ExPokeLibFatal("No connection")
            # self.log.fatal("No connection")
        
    def tap_screen(self, x, y, button = 1, duration = 30):
        self.log.debug("tap {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tap_screen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.write_to_phone("click:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
    
    def tap_down(self, x, y, button = 1, duration = 0):
        self.log.debug("tap_down {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tap_screen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.write_to_phone("button_down:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
    
    def tap_up(self, x, y, button = 1, duration = 50):
        self.log.debug("tap_up {},{},{},{}".format(x,y,button, duration))
        x, y = self.scaleXY(x, y)
        # response = requests.get("{}/tap_screen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.write_to_phone("button_up:{},{},{},{}".format(x,y,button, duration))
        self.log.debug("Response : {}".format(response))
        time.sleep(0.001 * duration)
        
    def moveCursor(self, x, y, dx, dy):
        self.log.debug("move {},{}".format(x,y))
        x, y = self.scaleXY(x, y)
        dx, dy = self.scaleXY(dx, dy)
        # response = requests.get("{}/tap_screen:{},{},{},{}".format(self.url, x, x, button, duration)
        response = self.write_to_phone("move:{},{},{},{}".format(x,y,dx,dy))
        self.log.debug("Response : {}".format(response))
        # time.sleep(0.1)
    
    def egg_handle(self):

        if self.screen_is_egg():
            print("Egg detected")
            try:
                # Open egg
                self.tap_screen(500, 1000)
                # exit pokemon scree
                self.color_match_wait_click(493, 1826, 28, 135, 149, time_out_ms=20000)
                sleep(5)
                # Select egg
                self.tap_screen(190, 544)
                # Tap incubate
                self.color_match_wait_click(493, 1425, 119, 215, 155)
                sleep(2)
                # Select incubator
                self.tap_screen(140, 1470)
                sleep(1)
                self.tap_screen(100, 100, button = 3)
                return True
            except:
                self.screen_go_to_home()
                return False
        else:
            return False
        
    
    def get_rgb(self, x, y):
        x, y = self.scaleXY(x, y)
        response = self.write_to_phone("color:{},{}".format(x,y))           
        self.write_to_phone("color:{},{}\n".format(x,y))
        self.log.debug("Response : {}".format(response.status_code))
        self.log.debug("Response : {}".format(response.json()))
        rgb = response.json()
        return int(rgb["red"]), int(rgb["green"]), int(rgb["blue"])
    
    def get_mouse(self):
        response = self.write_to_phone("mouse_get")          
        m = response.json()
        # print("mouse {}".format(m))
        print("mouse {}".format(m))
        return int(m["x"] / self.scaleX), int(m["y"] /self.scaleY)
    
    def color_match(self, x, y, r, g, b, threashold=10, debug=False, excep = True):
        rr, gg, bb = self.get_rgb(x, y)
        if debug:
            self.log.info("color_match x{},y{},r{},g{},b{},t{}".format(x, y, r, g, b,threashold))
            self.log.info("color_match x{},y{},r{},g{},b{},t{}".format(x, y, rr, gg, bb, threashold))
        if gg > (g + threashold) or gg < (g - threashold):
            log.debug("color_match : False")
        if      rr > (r + threashold) or rr < (r - threashold) or \
                gg > (g + threashold) or gg < (g - threashold) or \
                bb > (b + threashold) or bb < (b - threashold):
            if debug:
                log.debug("color_match : False")           
            return False
        if debug:
            log.debug("color_match : True")           
        return True
    
    def color_match_wait(self, x, y, r, g, b, threashold=10, time_out_ms=10000, 
                       freq_in_s = 1, same=True,
                       debug=False, ex=True):

        self.log.info("color_match_wait x{},y{},r{},g{},b{},t{},to{},f{},m{}".format(x, y, r, g, b, threashold, time_out_ms, freq_in_s, same))
        startTime = datetime.now()
        while True:
            if self.color_match(x, y, r, g, b, threashold=threashold, debug=debug) == same:
                return True
                
            if ((datetime.now() - startTime).total_seconds() * 1000) > time_out_ms:
                self.log.warn("Timeout waiting {}ms for x:{},y{} r{},g{},b{}".format(time_out_ms, x, y, r, g, b))
                r, g, b = self.get_rgb(x, y)
                if ex:
                    raise ExPokeLibError("Timeout waiting {}ms for x:{},y{} r{},g{},b{}".format(time_out_ms, x, y, r, g, b))
                else:
                    return False
            time.sleep(freq_in_s)
    
    def color_match_wait_click(self, x, y, r, g, b, threashold=10, time_out_ms=10000, 
                               freq_in_s = 1, same=True, delay=0.8,
                               debug=False, ex=True):
        self.log.info("color_match_wait_click x{},y{},r{},g{},b{},t{},to{},f{},m{}".format(x, y, r, g, b, threashold, time_out_ms, freq_in_s, same))
        time.sleep(delay)
        if self.color_match_wait(x, y, r, g, b, threashold, time_out_ms, freq_in_s, 
                            same=same, debug=debug, ex=ex):
            self.tap_screen(x, y)
            return True
        return False
    
    def tap_screenBack(self):
        self.log.info("Tap Screen back")
        # self.color_match_wait_click(501, 1826, 30, 134, 149)
        self.tap_screen(501, 1800)
        
    def tap_exit_mode(self):
        self.tap_screen(85,190)
        
    def tap_confirm(self):
        self.tap_screen(357, 1005)
        
    def tapAvatar(self):
        self.tap_screen(121, 1800)
        
    def tapOK(self):
        self.color_match(623,1062,83,212,162)
        self.tap_screen(623,1062)
        return True
    
    def tapYES(self):
        try:
            self.color_match_wait_click(366, 1103, 149, 216, 150, time_out_ms=1000)
        except:
            pass
        return True

    def tapSearch(self):
        self.color_match_wait(626, 457, 78, 208, 175,time_out_ms=2000)
        self.tap_screen(626, 457)
        # Wait for light grey fromkeyboard
        # self.color_match_wait(46, 1480, 37, 50, 55)
        self.color_match_wait(46, 1480, 255,255,255, same=False)
    
    def screen_get_type(self):
        return("unknow")

    def button_is_back(self):
        m = self.get_maxima_horizontal((410, 1855), 240)
        if m > 6:
            return True
        return False
    
    def get_maxima_horizontal(self, start, len, threshold=40, debug=False):
        jbuf = self.screen_capture_bw(start, (200, self.min_hight))
        npa = np.array(jbuf["gray"], dtype=np.uint8)
        delta = np.diff(npa.astype(np.int16))
        maxima = (np.abs(delta) > threshold).sum()
        return maxima
    
    def screen_gym_has_place(self):
        for y in range(1638, 1648, 2):
            maxima = self.get_maxima_horizontal((780, 1648), 200, threshold=30)
        print(f"Is defeated m {maxima}")
        if maxima <= 15:
            return True
        return False

    def screen_gym_need_defeat(self):
        maxima = self.get_maxima_horizontal((780, 1648), 200, threshold=30)
        print(f"Is defeat m {maxima}")
        if maxima > 15:
            return True
        return False

    def screen_go_to_gym(self):
        for i in range(0, 3):
            if self.screen_is_in_gym():
                return True
            self.tap_screen(500, 700)
            self.tap_screen(500, 700)
            self.tap_screen(500, 700)
            sleep(3)
        return False

    def screen_go_to_gifts(self):
        for i in range(0, 3):
            if self.screen_is_in_gym():
                return True
            self.tap_screen(500, 700)
            self.tap_screen(500, 700)
            self.tap_screen(500, 700)
            sleep(3)
        return False

    def screen_is_in_gym(self):
        maxima = self.get_maxima_horizontal((790, 1880), 180, threshold=40)
        print(f"Is in gym m {maxima}")
        if maxima >= 5 and maxima < 10:
            for i in range(5):
                maxima = self.get_maxima_horizontal((790, 1880), 180, threshold=40)
                print(f"Is verfy in gym {maxima}")
                if maxima < 5:
                    return False
                sleep(0.1)
            return True
        return False
    
    def screen_my_poke_in_gym(self):
        if not self.screen_is_in_gym():
            return False
        maxima = self.get_maxima_horizontal((780, 1650), 200, threshold=40)
        print(f"Is defeated m {maxima}")
        if maxima < 2:
            return True
        return False
    
        
    def park(self):
        v = PixelVector(self, 780, 980, 1627, 1627, 3 , "defeat")
        delta = np.diff(v.red()[1])
        maxima = (np.abs(delta) > 80).sum()
        print("screen_is_deafeat_gym maxima {}".format(maxima))
        if maxima > 6:
            return True
        return False

    def screen_is_catch_pokemon(self):
        y = 1792
        y = 1791
        delta_max = delta_min = 0
        for x in range(854,904,2):
            r,_,_ = self.get_rgb(x,y)
            r2,_,_ = self.get_rgb(x + 2,y)
            d = r2 -r
            if d < delta_min:
                delta_min = d
            if d > delta_max:
                delta_max = d
        # return True
        return (delta_max - delta_min) > 150
    
    def screen_is_pokestop(self):
        m = self.get_maxima_horizontal((27, 1931), 200, threshold = 1)
        if m == 0:
            r,g,b = self.get_rgb(27, 1931)
            if b > 200 and r < 50:
                return "stop_and_spin"
        return "stop_no"
    
    def screen_is_egg(self):
        if not self.color_match(364, 1091, 233, 255, 225):
            return False
        t, _ = self.pocr_read_and_image_center((480, 408), (100,100))
        t =  "".join(t)
        # ad from ready...
        return "Oh" in t or "ad" in t

    def screen_capture_bw(self, start, size, scale=True):
        x, y = start
        w, h = size
        if x < 0 or (x + w) >= self.maxX \
           or y < 0 or (y + h) >= self.maxY:
            self.log.error("clip out of range x{}, y{}, width{}, hight{}", x, y, w, h)
            return None
        if scale:
            x, y = self.scaleXY(x, y)
            w, h = self.scaleXY(w, h)
    
        response = self.write_to_phone("snip_gray:{},{},{},{}".format(x ,y ,w, h))           
        return response.json()
        
    def pocr_read_line_center(self, start, size):
        cs = (start[0] - size[0]/2, start[1] - size[1]/2,)
        t = self.pocr_read(cs, size)
        return "".join(t)        

    def pocr_read_and_image_center(self, start, size):
        cs = (start[0] - size[0]/2, start[1] - size[1]/2,)
        return self.pocr_read_and_image(cs, size)

    def pocr_read_line(self, start, size):
        t = self.pocr_read(start, size)
        # self.log.debug(f"pocr_read_line {"".join(t)}")
        return "".join(t)

    def clip_boundaries(self, start, size):
        ret = True
        if (start[0] - size[0] / 2) < 0:
            start[0] = 0 + size[0] / 2
        if (start[0] + size[0] / 2) >= self.maxX:
            start[0] = self.maxX < size[0] / 2

    def pocr_read(self, start, size):
        if not self.reader:
            self.reader = Ocr(self)
        try:
            # if check_boundaries(start, size):
            #    return self.reader.pocr_read(start, size)
            return self.reader.pocr_read(start, size)
        except:
            print("No good")
            sleep(1)
            return [""]

    def pocr_read_and_image(self, start, size):
        if not self.reader:
            self.reader = Ocr(self)
        try:
            # if check_boundaries(start, size):
            #    return self.reader.pocr_read(start, size)
            return self.reader.pocr_read_and_image(start, size)
        except:
            print("No good")
            sleep(1)
            return [""]
    
    @poke_timeout()
    def pocr_wait_text(self, start, size, text, pause=0,  to_ms=0, debug=False):
        t = self.pocr_read_line(start, size)
        self.log.debug("read {}".format(t))
        if text in t:
            return t
        sleep(pause)
        return False
    
    def pocr_wait_text_center(self, start, size, text, pause=0.99,  to_ms=5.5, debug=False):
        cs = (start[0] - size[0]/2, start[1] - size[1]/2,)
        while to_ms > 0:
            if self.pocr_wait_text(cs, size, text, pause, to_ms, debug) != False:
                return True
            sleep(pause)
            to_ms -= pause
        return False

    def scroll(self, dx, dy, start_x = 100, start_y = 1000, tap_time = 0.1, stop_to = 0.6):
        # self.log.info("Scroll")
        # x = maxX / 2
        x = float(start_x)
        y = float(start_y)
        sx = float(dx / 20.0)
        sy = float(dy / 20.0)
        self.tap_down(int(x), int(y), tap_time)
        for s in range(0,20):
            x = x + sx
            y = y + sy
            self.moveCursor(int(x), int(y), int(sx), int(sy))
            # print("sy={}".format(int(sy)))
            # self.moveCursor(int(sx), int(sy))
            time.sleep(0.02)
            # self.tap_down(int(x), int(y), int(sx), int(sy))
        time.sleep(stop_to)
        self.tap_up(int(x + dx), int(y + dy))

    def tap_open_gift(self):
        self.log.debug("tap_open_gift")
        # time.sleep(1)
        # self.color_match_wait_click(406, 1654, 137, 218, 154)
        to = 50
        while to > 0:
            text = self.pocr_read((400, 1620), (200, 76))
            print(text)
            if "OPEN" in ''.join(text):
                break
            sleep(0.2)
            to -= 1
        if to == 0:
            print("Problem to open gift")
            return True
        # Pin
        if 1 == 1:
            print("Postit")
            time.sleep(0.5)
            self.tap_screen(876, 1652, duration = 10)
            time.sleep(0.5)
            self.tap_screen(876, 1652, duration = 10)
            time.sleep(1)
        while self.color_match(406, 1600, 137, 218, 154):
            print("tap_open_gift")
            self.tap_screen(406, 1654)
            time.sleep(0.2)
                
    def tap_back(self):
        self.tap_screen(498, 1855)
        
    def tap_me(self):
        for timeout in reversed(range(0,100)):
            if not self.color_match(151, 820, 255, 255, 255, debug=True):
                print("tap me")
                time.sleep(0.2)
                self.tap_screen(269, 173)
                return True
            time.sleep(0.2)
        return False


    def tap_add_friend(self):
        return self.tap_screen(387, 480)

    def get_my_name(self):
        if self.my_name != None:
            return self.my_name
        self.screen_go_to_home()
        self.screen_friend()
        sleep(1)
        self.tap_add_friend()
        sleep(2)
        for i in range(5):
            mn = self.pocr_read_line_center((500, 575),(420, 70))
            for i in range(2, len(mn)):
                print(mn[:i])
                ret = db_p().get_trainer(mn[:i])
                if len(ret) == 1:
                    self.my_name = ret[0][1]
                    print(f"My name from DB {self.my_name}")
                    self.screen_go_to_home()
                    return self.my_name                    
        self.screen_go_to_home()
       # print("MYNAME {}".format(text[0]))
        
        return None
    
    def tapFriends(self):
        self.log.debug("tapFriends")
        for timeout in reversed(range(0,100)):
            if self.screen_is_friend() == True:
                break
            print("TAP")
            self.tap_screen(493, 193)
            time.sleep(0.2)

    def tapPokeBall(self):
        self.color_match_wait_click(500, 1798, 255, 57, 69)
        
    def tapPokeSearch(self):
        self.color_match_wait_click(187, 371, 233, 243, 223)
        
    def menuPokemon(self):
        self.color_match_wait_click(180, 1599, 241, 255, 242)
        
    def tapTextOK(self):
        # self.color_match_wait_click(871, 1082, 34, 34, 34)
        time.sleep(1)
        # self.color_match_wait_click(871, 1152, 34, 34, 34)
        self.tap_screen(871, 1152)
        
    def friend_select_first(self):
        time.sleep(0.2)
        try:
            self.color_match_wait_click(147, 808, 255, 255,255, same=False, time_out_ms=4000)
        except:
            return False
        return True
        
    def pokemon_select_first(self):
        found_poke = False
        time.sleep(0.2)
        self.color_match_wait(79, 179, 255, 255, 255)
        for i in range(0,15):
            time.sleep(0.1)
            if self.color_match(184, 777, 251, 254, 249) and \
                self.color_match(184, 750, 255, 255, 255) and \
                self.color_match(178, 730, 255, 255, 255) and \
                self.color_match(184, 710,255, 255, 255):
                print(f"No more pokemons with this filter round{i}")
            else:
                found_poke = True
                break
        if not found_poke:
            return False
        print("Tap 177, 751")
        self.tap_screen(177, 751)
        return True
    
    def color_show(self, x, y):
            r, g, b = self.get_rgb(x, y)
            print("Pixel color {},{},{},{},{}".format(x, y, r, g ,b))
       
    def evolvePokemon(self):
        self.color_match_wait(135, 1001, 255, 255, 255)
        time.sleep(1.5)
        # self.scroll(0, 200)
        # sys.exit(0)
        print("Scroll up")
        self.scroll(0,-350, start_y = 1500, tap_time = 0.3, stop_to = 0.5)
        # self.scroll(0,-330)
        # Search and tap evolve
        for y in range(self.maxY - 2, self.maxY - 600, -10):
            self.log.debug("Search in {}".format(y))
            if self.color_match(116, y, 163, 220, 148):
                print("Match at {}".format(y))
                self.tap_screen(130, y -10)
                break
        time.sleep(1.2)
         # Search and tap yes
        found = False
        for i in range(0, 4):
            print("Wait for yes")
            for y in range(1200, 1400, 10):
                if self.color_match(319, y, 151, 218, 147):
                    self.tap_screen(319, y)
                    time.sleep(0.1)
                    self.tap_screen(319, y)
                    found = True
                    break
        if found == False:
            text, image = self.pocr_read((350, 1650), (300, 76))
            self.tap_screen(100, 100, button = 3)
            time.sleep(1)
            if "POWER" in ''.join(text):
                print("Power up")
                self.tap_screen(500,975)
                self.text_line_ok("\\anovolve")
                sleep(0.2)
                self.tapTextOK()
                sleep(0.2)
                self.tap_screen(500,1100)
                sleep(0.2)
            # 2 screens back
            self.tap_screen(100, 100, button = 3)
            time.sleep(0.8)
            return
        time.sleep(3)
        # 72, 476, 255, 255, 255
        print("Wait for evolve ready")
        self.color_match_wait(505, 1832, 28, 135, 149, time_out_ms=20000)
        # self.color_match_wait(72, 476, 255, 255, 255, time_out_ms=20000)
        # self.color_match_wait(135, 1388, 255, 255, 255, time_out_ms=20000)
        # self.color_match_wait(135, 1388, 255, 255, 255, time_out_ms=20000)
        print("Evolve ready")
        time.sleep(0.8)
        self.tap_screenBack()
        
    def tapBattle(self):
        self.color_match_wait_click(496, 1681, 95, 166, 83, delay=3)
    
    def tap_trade(self):
        self.log.info("Tap Trade")
        for i in range(0,20):
            for y in range(1970, 1950, -2):
                if self.color_match(427, y, 60, 60, 60, threashold=20, debug=True):
                    print(f"TAP {y}") 
                    self.tap_screen(427, y)
                    return
            print("Wait for trade button")
            time.sleep(1)
        raise
        
    def tap_battle(self):
        self.log.info("Tap battle")
        for i in range(0,20):
            if self.color_match(802, 1923, 103, 174, 89, threashold=20, debug=False):
                self.tap_screen(800, 1923)
                return
            print("Wait for battle button")
            time.sleep(1)
        raise
        
    def text_line_ok(self, text):
        time.sleep(0.1)
        # self.log.debug("type string {}".format(text))
        i = 0
        
        while i < len(text):
            c = text[i]
            i += 1
            if c == "&":
                c = "\\&"
            elif c == "\\":
                # print("RALF : backslash {}".format(text))
                # print("RALF : backslash {}".format(text[i]))
                c = "\\" + text[i]
                i += 1
            # print("RALF string '{}'".format(c))
            # print(c)
            self.write_to_phone("key:{}".format(c))
            # time.sleep(0.0035)
            time.sleep(0.013)

    def selectAll(self):
        self.text_line_ok("\\a")
    
    def getTimeNow(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def is_home(self):
        # self.log.debug(f"screen_si_home{self.color_show(501,1802)}")
        return self.color_match(501,1802,255,55,72,10)
    
    def button_has_exit(self):
        for y in range(1835,1880,4):
            self.color_show(500,y)
        if self.color_match(500, 1835, 235, 245, 242, threashold=15, debug=False) \
            and self.color_match(500, 1875, 235, 245, 246, threashold=15, debug=False):
            return True
        return False
    
    def button_tap_exit(self):
        self.tap_screen(500,1850)
    
    def screen_is_friend(self):
        
        # text, image = self.pocr_read_line((400, 125), (200, 70))
        # if "FRIENDS" in text:
        #    return True
        # return False
    
        if self.color_match(319, 843, 0, 0, 0) \
            and self.color_match(319, 1246, 0, 0, 0) \
            and self.color_match(678, 843, 0, 0, 0):
            self.tap_back()
            time.sleep(0.5)
        return self.color_match(32, 91, 255, 255, 255)

    def spin_disk(self, to = 2):
        while to > 0:
            
            
            # if self.color_match(152, 1921, 183, 116, 248, debug=True):
            if self.color_match(152, 1921, 137, 98, 227, debug=False):
            # if not self.screen_is_pokestop():
                return True
            print("Spin disk {}".format(to))
            self.scroll(600, 0, start_x = 150, start_y = 1000)
            sleep(1)
            to -= 1
        return False
    
    def screen_go_to_home(self):
        self.log.info("Go to homescreen")
        print("Go Home")
        MAX_TRYS = 10 
        count = 0 # Try count time

        # sys.exit()
        # Try left button as long als possible!
        while self.is_home() == False:
            # self.color_show(300, 1803)
            # OK on green in the middle
            log.debug(f"Go home atempt {count}")
            if self.color_match(300, 1805, 150, 218, 151, debug=False):
                self.tap_screen(500, 1800)
            elif self.color_match(300, 1705, 150, 218, 151, debug=False):
                self.tap_screen(500, 1800)            
            elif self.color_match(500, 1828, 28, 135, 151, debug=False):
                self.tap_screen(500, 1828)            
            elif self.color_match(57, 365, 28, 135, 149, debug=False):
                self.tap_screen(57, 365)
            elif self.color_match(357, 1005, 150, 218, 151, debug=False):
                # Not exit pokemon
                if not "GO" in self.pocr_read_line_center((790, 800), (100, 70)):
                    self.tap_confirm()
                else:
                    self.tap_screen(100, 100, button = 3)
            else:
                self.tap_screen(100, 100, button = 3)
            count += 1
            if count > MAX_TRYS:
                log.warn("No homescreen after {MAX_TRYS} atempts")
                print("Try egg")
                if self.egg_handle():
                    break
                for y in range(100, self.maxY - 100, 25):
                    if self.color_match(500, y, 116, 214, 156):
                        print(f"Something green at {y}")
                        b_text = self.pocr_read_line_center((500, y + 50), (100, 100))
                        print(f"Button text {b_text}")
                        if re.match(b_text, ".*OK.*"):
                            print("Found OK")
                            self.tap_screen(500, y)
                            break
                count = 0
            sleep(1)

        if count == 0:
            log.info("No homescreen found!")
            return False
        log.info("Now we are on the home screen {}".format(self.is_home()))
        return True
    
    def screen_go_home_old(self):    
        while self.is_home() == False and count > 0:
            self.log.warning("Wrong color")
            if self.color_match(501, 1826, 30, 134, 149):
                self.tap_screenBack()                
            # Upper left exit
            # elif self.color_match(500, 1822, 246, 245, 245, threashold=15):
            #    self.log.debug("light green press?")
            #     self.tap_screenBack()
            elif self.color_match(498, 1832, 231, 235, 227):
                self.log.debug("Almost white?")
                print("AlmostWhite")
                self.tap_screenBack()
            elif self.color_match(500, 1832, 240, 242, 230):
                self.log.debug("whith like gym press?")
                self.tap_screenBack()
            elif self.color_match(86, 187, 27, 134, 148):
                self.tap_exit_mode()
            elif self.color_match(357, 1005, 150, 218, 151):
                self.tap_confirm()
            elif self.color_match(357, 1138, 150, 218, 151):
                self.tap_screen(357, 1138)
            elif self.color_match(357, 1000, 143, 215, 150):
                self.tap_screen(357, 1000)                
            elif self.color_match(847, 1849, 27, 134, 150):
                self.tap_screen(847, 1849)
            elif self.color_match(109, 185, 234, 247, 240) or \
                 self.color_match(97, 166, 250, 250, 250):
                print("Tap somthing")
                self.tap_screen(109, 185)
                self.tapYES()
                count = count -1 
            else:
                count = count -1
                if self.color_match(64, 156, 255, 255, 255):
                    self.tap_screen(64, 156)
                elif self.color_match(57, 361, 28, 135, 149):
                    self.tap_screen(57, 361)
                elif count == 6:
                    for y in [1750, 1850]:
                        self.tap_screen(500,y)                    
                    self.tap_screen(100, 100, button = 3)
                else:
                    print("Not found")
                    if count == 0:
                        raise ExPokeNoHomeError("Cant find home")
            print("count = {}".format(count))
            if count == 4:
                self.tap_screen(100, 100, button = 3)
            time.sleep(1)
        log.info("Now we are on the home screen {}".format(self.is_home()))

    def selectLeague(self, league):
        if league == "great":
            self.log.info("Great League selected")
            y = 951
        elif league == "ultra":
            self.log.info("Ultra League selected")
            y = 1301
        elif league == "master":
            self.log.info("Master League selected")
            y = 1650
        else:
            raise ExPokeLibError("Uknow leage {}".format(league))
        
        self.color_match_wait(350, y, 255, 255, 255)
        time.sleep(3)
        self.tap_screen(350, y)
        # Lets battle
        self.color_match_wait_click(305, 1230, 161, 221, 148)
        
    def screen_friend(self):
        self.screen_go_to_home()
        self.tapAvatar()
        sleep(3)
        self.tapFriends()
        self.color_match_wait(878, 1562, 255, 255, 255, time_out_ms=30000)

    def screen_me(self):
        self.screen_go_to_home()
        time.sleep(1)
        self.tapAvatar()
        time.sleep(1)
        self.tap_me()

    def pokeScreen(self):
        self.screen_go_to_home()
        self.tapPokeBall()
        self.menuPokemon()
        
    def selectPokemon(self, filter):
        self.pokeScreen()
        self.tapPokeSearch()
        self.color_match_wait(121, 1154, 255, 255, 255)
        time.sleep(0.4)
        self.text_line_ok(filter)
        time.sleep(1)        
        self.tapTextOK()
        
    def friend_search(self, name):
        self.tapSearch()
        print("done")
        self.text_line_ok(name)
        self.tapTextOK()

    def pokemon_search(self, filter):
        self.color_match_wait_click(500, 345, 233, 233, 223, threashold=14, time_out_ms=30000,debug=False)
        time.sleep(1)
        self.selectAll()
        time.sleep(0.2)
        self.text_line_ok(filter)
        self.tapTextOK()
    
    def swipe(self, x1, y1, x2, y2):
        steps = 5
        sx = float(x1)
        sy = float(y1)
        dx = (float(x2) - float(x1)) / float(steps)
        dy = (float(y2) - float(y1)) / float(steps)
        self.tap_down(x1, y1, duration = 0)
        for s in range(0, steps):
            self.moveCursor(int(sx), int(sy), int(sx + dx), int(sy + dy))
            sx = sx + dx
            sy = sy + dy
            # print("sx={},sy={}".format(int(sx),int(sy)))
            # self.moveCursor(int(sx), int(sy))
            # time.sleep(0.005)
        self.tap_up(int(sx), int(sy))
    
    def catchPokemon(self):
        print("Try to catch pokemon")
        while self.color_match(881, 1742, 238, 56, 56) or \
                self.color_match(881, 1742, 255, 255, 255):
            v = random.randint(0,300)
            print("Throug {}".format(v))
            self.swipe(506, 1820, 506, 950 + v)
            try:
                self.color_match_wait(364, 1326, 146, 216, 149, time_out_ms = 20000)
                self.tap_screen(364, 1326)
            except:
                pass
    
    def collectRewards(self):
        for i in range(0,5):
            try:
                print("Collect award {}".format(i))
                for x in range( 100,800,20):
                    # self.color_show(x, 1630)
                    if self.color_match(x, 1630, 254, 183, 86):
                        
                    # if not self.color_match(x, 1630, 254, 250, 250):
                        self.tap_screen(x, 1630)
                        time.sleep(5)
                        try:
                            print("Check if pokemon")
                            # time.sleep(1.5)
                            if not self.color_match(166, 1171, 250, 251, 246):
                                print("Try to catch pokemon")
                                self.catch_pokemon(distance = 7)
                                self.color_match_wait_click(418, 1365, 137, 218, 154, time_out_ms=3500)
                                self.color_match_wait_click(508, 1869, 26, 136, 151, time_out_ms=3500)
                        except:
                            sys.exit(0)
                            pass
            except:
                pass
        if self.color_match(187, 1919, 255, 180, 82):
            self.tap_screen(187, 1919)
        
    def screen_item(self):
        self.screen_go_to_home()
        print("wait")
        self.tapPokeBall()
        self.color_match_wait_click(795, 1542, 240, 254, 238)
        try:
            self.color_match_wait(824, 1855, 245, 245, 242, threashold=14, time_out_ms=3000)
        except:
            return False
        return True
               
    def screen_battle(self):
        print("Tap pokeball")
        self.tapPokeBall()
        self.color_match_wait_click(734, 1041, 240, 252, 239)
        
    def heal_all(self):
        print("Heal all")
        self.screen_item()
        sleep(1)
        # Revive
        revived = False
        for y in [960, 550]:
            # for x in [750, 455, 150]           
            for x in range(800,100, -20):
                # self.log.debug(f"search revive {self.color_show(x, y)}")
                if self.color_match(x, y, 220, 215, 110, threashold=35):
                    print("Found revive at {},{}".format(x,y))
                    self.tap_screen(x, y)
                    time.sleep(0.5)
                    if not self.color_match_wait_click(350, 1650, 159, 218, 148, ex=False, time_out_ms=1000):
                        revived = True
                    self.color_match_wait_click(525, 1850, 28, 135, 149, ex=False)
                if revived:
                    break
            if revived:
                break
                            
        time.sleep(1)
        # Potion
        healed = False
        for i in range(0, 3):
            # upper left potion
            self.tap_screen(250, 550)
            if not self.color_match_wait_click(350, 1650, 159, 218, 148, ex=False, time_out_ms=1000):
                healed = True
            self.color_match_wait_click(525, 1850, 28, 135, 149, ex=False)
            if healed:
                break
            time.sleep(1)
        self.screen_go_to_home()

    
    def battle_league(self):
        time.sleep(3)
        self.color_show(200, 1900)
        if self.color_match(200, 1900, 255, 180, 82):
            print("Claim rewards")
            self.tap_screen(200, 1900)
            time.sleep(1)
            return

        count = 10
        while not self.color_match(366, 1939, 154, 218, 149) and \
                not self.color_match(361, 1878, 229, 246, 227):
            count = count -1
            print("Scroll")
            if count == 0:
                return
            if self.is_home():
                return
            self.scroll(0, -60)
            time.sleep(0.5)
        time.sleep(0.5)
        if self.color_match(361, 1878, 229, 246, 227):
            self.collectRewards()
            # time.sleep(30)
        if self.color_match(312, 1835, 149, 217, 148):
            self.tap_screen(312, 1835)
            return
        self.color_match_wait_click(366, 1939, 154, 218, 149)
        next_battle = True
        while next_battle:
            for to in range(1,10):
                if self.color_match(288, 1806, 151, 217, 147):
                    self.tap_screen(288, 1806)
                if self.color_match(328, 939, 255, 255, 255):
                    self.tap_screen(328, 939)
                    break
                if self.color_match(347, 1812, 144, 218, 152):
                    self.tap_screen(347, 1812)
                time.sleep(1)
            self.color_match_wait_click(322, 1781, 163, 220, 148)
            try:
                time.sleep(1)
                self.color_match_wait(81, 998, 255, 254, 255, same=False, time_out_ms=20000)
            except:
                pass
            self.doBattle()
            try:
                next_battle = self.color_match_wait_click(315, 1535, 153, 219, 149, time_out_ms=20000)
                next_battle = True
                time.sleep(1)
                # next_battle = self.color_match_wait(690, 1539, 72, 209, 163)
            except:
                next_battle = False
                
    def battle_friend(self, league):
            # Press battle
            sleep(4)
            if league == "great":
                self.color_match_wait_click(506, 1044, 255, 255, 255)
            elif league == "ultra":
                self.color_match_wait_click(505, 1388, 255, 255, 255)
            elif league == "master":
                self.color_match_wait(505, 1757, 255, 255, 255)     
            sleep(1)
            self.color_match_wait_click(468, 1281, 123, 215, 154)  
        
    def battleTrainer(self, trainer, league):
        for i in range(0,6):
            print("Scroll step {}".format(i))
            self.scroll(0,-1000, start_y = 1500, tap_time = 0.3, stop_to = 0.3)
            sleep(0.5)
            
        time.sleep(1)
        
        cont = True
        while cont:
            self.tap_screen(250 + ((trainer - 1) * 250), 1634)
            # Press battle
            self.color_match_wait_click(362, 1552, 149, 217, 148)
            if league == "great":
                self.color_match_wait_click(338, 850, 255, 255, 255)
            elif league == "ultra":
                self.color_match_wait_click(333, 1300, 255, 255, 255)
            elif league == "master":
                self.color_match_wait(345, 1640, 255, 255, 255)
            else:
                self.log.error("Unknow trainer league {}".format(league))
                
            self.color_match_wait_click(501, 1742, 113, 213, 157)
            self.doBattle()
            self.color_match_wait_click(500, 1826, 28, 135, 149)
            time.sleep(0.5)
        
    def attack(self, time_out_ms = 12000):
        startTime = datetime.now()
        # while ((datetime.now() - startTime).total_seconds() * 1000) < time_out_ms:
            # and \
        step = 100
        self.tap_down(10, 800, duration = 0)
        x = self.maxX / 2
        y = self.maxY / 2
        while   ((datetime.now() - startTime).total_seconds() * 1000) < time_out_ms and \
                not self.color_match(164, 222, 246, 14, 29) and \
                not self.color_match(100, 100, 10, 10, 10) and \
                not self.color_match(500, 1826, 28, 135, 149):
                # and self.color_match(213, 177, 255, 255, 255) \
                # and self.color_match(722, 177, 255, 255, 255):
            
            self.tap_up(498, 1500, duration = 0)
            time.sleep(0.05)
            # Tap shield
            self.tap_screen(498, 1500)
            self.tap_down(498, 1500, duration = 0)

            # self.swipe(150, 700, 800, 1750)
            # self.swipe(800, 700, 150, 1750)
            # for x in range(50,990, 120):
            #    self.swipe(x, 700, 900 - x, 1950)
            # Use shield for what ever
            # self.tap_screen(498, 1500)
            if False:
                for y in range(800, 1900, 100):
                    self.swipe(10, y, self.maxX - 200, y)

            if False:
                for y in range(0, 100, 25):
                    for ya in range(800, 1900, 100):
                        self.swipe(10, y + ya, self.maxX - 200, y + ya)
                    
                    
            if False:
                self.swipe(10, 800, self.maxX - 10, self.maxY - 10)
                self.swipe(self.maxX - 10, 800, 10, self.maxY - 10)
    
                self.swipe(self.maxX / 4, self.maxY - 10, self.maxX - ( self.maxX / 4), 800)
                self.swipe(self.maxX - ( self.maxX / 4), self.maxY - 10, self.maxX / 4, 800)
              
            if False:  
                cx = self.maxX / 2
                cy = 800 + self.maxX / 2
                for a in range(0, 180,10):
                    dx = int(math.sin(math.radians(a)) * (self.maxX / 2 - 2))
                    dy = int(math.cos(math.radians(a)) * 698) # (self.maxX / 2 - 2))
                    log.debug("x1 {}, y1 {}, x2 {}, y2 {}".format(cx + dx, cy + dy, cx - dx, cy - dy))
                    # self.swipe(cx + dx, cy + dy, cx - dx, cy - dy)
                    # self.swipe(cx - dx, cy + dy, cx + dx, cy - dy)
                    self.moveCursor(cx + dx, cy + dy, cx - dx, cy - dy)
                    self.moveCursor(cx - dx, cy - dy, cx + dx, cy + dy)
                    
            if False:
                # self.tap_down(10, 800, duration = 0)
                for y in range(800, 1800, step):
                    self.moveCursor(10, y, self.maxX - 200, y)
                    time.sleep(0.01)
                    self.moveCursor(self.maxX - 200, y ,10 , y + step)
                    time.sleep(0.01)
                   
                for x in range(10, self.maxX - 200, step):
                    self.moveCursor(x, 800, x, 1900)
                    time.sleep(0.01)
                    self.moveCursor(x, 800, x + step, 1900)
                    time.sleep(0.01)

            if False:
                xn = random.randint(10, self.maxX - 200)
                yn = random.randint(800, 1900)
                self.moveCursor(x, y, xn, yn)
                x = xn
                y = yn
                
            if True:
                x = ox = 200
                y = oy = 1300
                t = 0.05
                step = 30
                max_degrees = 180
                t = 0.03
                step = 45
                max_degrees = 360
                for a in range(0,max_degrees, step):
                    dx = ox + ( a * ( 600.0 / max_degrees))
                    dy = oy + (int(math.sin(math.radians(a)) * 350))
                    self.moveCursor(x, y, dx, dy)
                    x = dx
                    y = dy
                    time.sleep(t)
                for a in range(max_degrees,0, -step):
                    dx = ox + ( a * ( 600.0 / max_degrees))
                    dy = oy + (int(math.sin(math.radians(a)) * 350)) 
                    self.moveCursor(x, y, dx, dy)
                    x = dx
                    y = dy
                    time.sleep(t)           
        self.tap_up(x, y + step, duration = 0)
                
    def catch_pokemon(self, distance = 6, right = True, berry = "a"):
        while not self.color_match(90, 1414, 245, 254, 242):
            try:
                self.color_match_wait(420, 1923, 220, 220, 220, threashold = 35)
            except:
              print("Catch over")
              break
            print("Catch distance {}".format(distance))
            self.tap_screen(114, 1757)
            time.sleep(1)
            no_berry = True
            if berry == "a":
                if self.color_match(814, 1373, 236, 227, 19):
                    self.tap_screen(815, 1375)
                    sleep(0.5)
                    self.tap_screen(486, 1748)
                    sleep(1)
                    no_berry = False
                elif self.color_match(772, 1767, 248, 246, 76):
                    self.tap_screen(772, 1767)
                    sleep(0.5)
                    self.tap_screen(486, 1748)
                    sleep(1)
                    no_berry = False
                elif self.color_match(182, 1718, 238, 232, 27):
                    self.tap_screen(182, 1718)
                    sleep(0.5)
                    self.tap_screen(486, 1748)
                    sleep(1)
                    no_berry = False
            elif berry == "g":
                self.scroll(600,0, start_y = 1750, tap_time = 1)
                time.sleep(0.5)
                if self.color_match(454, 1732, 255, 143, 9):
                    self.tap_screen(454, 1718)
                    sleep(0.5)
                    self.tap_screen(486, 1748)
                    sleep(1)
                    no_berry = False
            if no_berry:
                time.sleep(1)
                print("Remove screen")
                self.tap_screen(795, 191)
                sleep(2)
            sleep(0.5)
            d = distance + random.randint(-4, 4)
            print("distance {}".format(d))
            self.catch_move(distance = d)
            sleep(5)
       
        
    
#     def catch_move(self, right = True, start = -90, end = 60, off_y = 900, radius = 250, delay = 0.012, step = 5, distance = 15):
    def catch_move(self, right = True, start = -180, end = 90 + 720, off_x = 500, off_y = 1300, \
                   radius = [80, 250], delay = 0.015, step = 5, distance = 5, tilt = -1.0):
        def getX(d, r, offset=0, tilt = 0.0):
            return math.sin(math.radians(d)) * float(r) + float(offset) + float(tilt)
        
        def getY(d, r, offset=0, tilt = 0.0):
            return math.cos(math.radians(d)) * float(r) + float(offset) + float(tilt)
        
        attempt = 1 
        # off_x = 500
        # off_y = 1250
        # off_y = 900
        y = getY(start, radius[1])
        x = getX(start, radius[0], tilt = y * tilt) 
        self.tap_down(x + off_x, y + off_y)
        top = 10
        while top < 0:
            for probe in range(750,900,2):
                if self.color_match(500, probe, 240,240,240):
                    top = probe
        button = -1
        while top < 0:
            for probe in range(750,850,-2):
                if self.color_match(500, probe, 240,240,240):
                    top = probe
        # print("Top = {}".format(top))
        # return
        a  = start + step
        b = 0.0
        if attempt % 2:
            right = False
        else:
            right = True
            
        while a < end + step:
            a = a + step + int(a / 60)
            b = b + 0.2
            # t = radius + int(b)
            # radius = t
            # for a in range(start + step, end + step, step):
            sx = x
            sy = y
            
            y = getY(a, radius[1]) # - a * 2
            x = getX(a, radius[0] , tilt = y * tilt)
            attempt = attempt + 1
            # print("radius {}".format(radius))
            # print("XY {} {}".format(x, y))
            # print("x = {}".format(x))
            self.moveCursor(int(sx) + off_x, int(sy) + off_y, int(x) + off_x, int(y) + off_y)
            # dx = x - sx
            # dy = y - sy
            # d = math.sqrt(dx * dx + dy * dy)
            # print("Delta {}".format(d))
            # canvas.create_line(sx, sy, x, y)
            # canvas.update()
            time.sleep(delay)
        ys = int(y)
        xs = x
        dx = x - sx
        dy = y - sy
        d = math.sqrt(dx * dx + dy * dy)
        print("Delta {}".format(d))
        accel=0.0
        #for y2 in range(int(y) - 10 , int(y) - 100, -10):
        for i in range(distance):        
            accel = accel + 5.0
            ye = ys - ( d + accel)
            xe = xs + dx # distance - i
            self.moveCursor(int(xs) + off_x, int(ys) + off_y, int(xe) + off_x, int(ye) + off_y)
            xs = xe
            ys = ye
            time.sleep(delay)
        # return
        self.tap_up(x, y)
        # 750

    def black_screen(self):
        for xy in range(100, 600, 100):
            if not self.color_match(xy, xy, 1, 1, 1, threashold=1):
                return False
        return True
            
    #
    # Parameter:
    # in_battle - If true is in battle already dont's wait
    def doBattle(self, in_battle = False, opponent = None):
            def still_in_battle():
                in_battle = False
                if not self.color_match(100, 100, 10, 10, 10) and \
                        not self.color_match(500, 1826, 28, 135, 149):
                    print("Found trainer screen")
                    # return False
                # Check black screen    
                        
               # Check white screen
                if not in_battle:
                    for d in range(0, 320, 80):
                        if not self.color_match(200 + d, 1150 + d, 241, 241, 241, threashold=15):
                        # if not self.color_match(200 + d, 1250, 241, 241, 241, threashold=15):
                            print("no white screen")
                            in_battle = True
                            break
                
                return in_battle
            
            # while not self.color_match(79, 357, 212, 227, 217) \
            #     and not self.color_match(76, 360, 240, 240, 240):
            #     time.sleep(0.1)
            def balls_visible():
                if not self.color_match(164, 222, 246, 14, 29) \
                    and not self.color_match(161, 218, 240, 38, 20):
                    return False
                return True

            
            if not in_battle:
                print("Wait for trainer")
                time_out_s = 90
                start_time = datetime.now()
                while not balls_visible():
                    # print("Wait for trainer")
                    if ((datetime.now() - start_time).total_seconds()) > time_out_s:
                        print("Battle did not start in time")                        
                        return
                    sleep(0.001)

            time_out_s = 5 * 60

            start_time = datetime.now()
            
            print("Start battle")
            
            while still_in_battle():
                if ((datetime.now() - start_time).total_seconds()) > time_out_s:
                    print("Battle timed out after {}s".format(time_out_s))                        
                    return
                for x in [270, 500, 730]:
                    # print("tap_screen : {},{}".format(x,1850))
                    
                    # Check for attack and use shield
                    if self.color_match(545, 195, 108, 121, 126, threashold=20) and False:
                    # if self.color_match(498, 1500, 237, 122, 241):
                        print("Use shield")
                        self.tap_screen(498, 1500)
                        # time.sleep(1)
                    if False:
                        print("")
                        for i in range(0, 80,2):
                            xx = 400 + i
                            yy = 660 + i
                            r,g,b =self.get_rgb(xx, yy)
                            print("{},{},{},{},{}".format(xx, yy, r, g, b))
                    time.sleep(0.01)
                    self.tap_screen(x, 1780)
                    time.sleep(0.01)
                    self.tap_screen(x, 1790)
                    time.sleep(0.01)
                    self.tap_screen(x, 1800)
                    # self.tap_screen(x, 1810)
                    # wait for ready of last red ball disappear
                    if self.black_screen():
                       return
                    # for x in range(400, 420, 4):
                    #    print("DEBUG X({}):{}".format(x,self.get_rgb(x, 665)))
                    # if self.color_match(405, 665, 220, 220, 220, threashold=20) \
                    #    or self.color_match(48, 670, 220, 220, 220, threashold=20):
                    # if self.color_match(394, 630, 252, 255, 255):
                    # if self.color_match(505, 660, 245, 245, 245) and \
                    # for xx in range(0,8,2):
                    #     for yy in range(0,8,2):
                    #         self.color_show(158 + xx,216 + yy)
                if not balls_visible():
                    self.attack()
                        # print("Exit")
                        # sys.exit(0)
                        
                # self.tap_screen(498, 1500)
                time.sleep(0.01)
                self.tap_screen(498, 1500)
                if opponent:
                    opponent.tap_screen(309, 1681)
         
    def hasGift(self):
        xs = 402
        ys = 1144
        # self.color_match_wait(76, 1970, 240, 240, 240, threashold = 14, debug=True)
        startTime = datetime.now()
        while ((datetime.now() - startTime).total_seconds() * 1000) < 1500:
            for x in range(xs, xs + 40, 4):
                # print("Check if gift {},{}".format(x, ys))
                if self.color_match(x, ys, 223, 15, 206, debug=False):
                    print("Friend has gift to open")
                    print("Found after {}ms".format(((datetime.now() - startTime).total_seconds() * 1000)))
                    return True
                time.sleep(0.1)
        print("Friend has no gift yet.")
        return False
    
        
    '''
    Return name, friendship level amd time to become best friend
    Must start from the friend screen
    '''
    def friend_get_info(self):
        # Open 4th heart under friend name
        self.tap_screen(270, 360)
        sleep(1.5)
        friend_level = self.pocr_read_line((360, 650), (280, 50)) # Tap the last heart for details
        self.tap_screen(750, 880)
        sleep(1)
        name = self.pocr_read_line((290, 530), (400, 90)) # Best friends do not open so bit care
        try:
            text = self.pocr_read_line_center((400, 1100), (100, 60))
            tl = re.findall(r'\d+\.?\d*', text)
            days_to_go = int(tl[0])
        except:
            days_to_go = 64
        self.tap_screen(500, 1850)
        sleep(0.5)
        return name, days_to_go, friend_level

    '''
    Set nickname of a friend
    must be on the friends screen!!
    '''
    def friend_set_nickname(self, nick):
        self.scroll(0, -1800, start_x=50, start_y=1900)
        sleep(1)
        text = self.pocr_read_line_center((515, 1404), (300, 70))
        if "NICKNAME" in text:
            self.tap_screen(515, 1404)
            sleep(1)
            self.text_line_ok(f"\a{nick}\\n")
        self.color_match_wait_click(392, 1101, 134, 217, 153, time_out_ms=1500, ex=False)
    '''
    Update friend level
    '''
    def friend_update_db(self, name, days_to_go, friend_level, opened=False, sent=False):
        if self.my_name == None:
            self.my_name = self.get_my_name()
        ret = db_p().add_friend(name, self.my_name, days_to_go, friend_level)
        print(ret.gen)
        if ret.gen:
            return False
        else:
            db_p().update_friend(name, self.my_name, days_to_go, friend_level, opened, sent)

    def friend_change_nick(self, nick):
        print(f"Change nick to {nick}")
        sleep(1)
        self.scroll(0, -1700, start_x = 50, start_y = 1750, tap_time = 0.3, stop_to = 0.5)
        print("Sroll up to nickname and wait")
        sleep(1)
        retries = 0
        text = ""
        while not "SET" in text:
            self.scroll(0, -1700, start_x = 50, start_y = 1750, tap_time = 0.3, stop_to = 0.5)
            sleep(1)
            text, _ = self.pocr_read_line((400, 1355), (300, 70))
            if retries > 30:
                return False
        # Tap set nickname
        self.tap_screen(500,1400)   
        sleep(1)
        self.text_line_ok(nick)
        self.tapTextOK()
        # nail it down
        sleep(0.5)
        self.tap_screen(286, 1105)

    def gift_open(self):
        opened = True
        self.log.info("tap gift")
        try:
            self.color_match_wait(496, 1000, 230, 51, 198, time_out_ms = 4000, threashold=50)
        except:
            pass
        time.sleep(0.5)
        self.tap_screen(500, 1000)
        # time.sleep(0.1)
        # self.tap_screen(500, 1000)
        self.log.info("gift_open")
        self.tap_open_gift()
        while self.color_match(85, 1960, 255, 255, 255) == False:
            # if ping_limit:
            #     return False
            if self.color_match(376, 1630, 144, 217, 149):
                print("Daily limit reached")
                self.tap_screen(500, 1850)
                opened = False
            else:
                self.tap_screen(85, 1960)
                time.sleep(0.5)
        name, days_to_go, level = self.friend_get_info()
        self.friend_update_db(name, days_to_go, level, opened=opened)
        if days_to_go <= 2 or days_to_go == 62 or days_to_go == 61:
            self.friend_set_nickname("ff pokemat")
        return opened
    
    def gift_send(self, has_gift = False):
        print("Send gift")
        # if self.hasGift():
        #    self.tap_screen(500, 1850)
        time.sleep(2)
        if has_gift:
            self.tap_screen(500, 1850)
        # if self.color_match(175, 1919, 243, 243, 243, threashold=13):
        # if self.color_match(237, 1900, 172, 172, 172):
        #     print("Friend has a gift")
        #     return False
        timeout = 50
        # while self.color_match(800, 857, 255, 255, 255,threashold=1) == False:
        # Check for post card
        name, days_to_go, level = self.friend_get_info()
        self.friend_update_db(name, days_to_go, level)
        if days_to_go <= 2 or days_to_go == 62 or days_to_go == 61:
            self.friend_set_nickname("ff pokemat")
            sleep(1)
        while self.color_match(700, 857, 255, 255, 255,threashold=1) == False \
                and self.color_match(750, 1110, 255, 255, 255,threashold=1) == False:
            
            time.sleep(0.2)
            self.tap_screen(170, 1919)
            timeout = timeout - 1
            # Timout or send already
            if timeout == 0 or \
                self.color_match(95, 1000, 232, 128, 181):
                return False
        time.sleep(1)
        self.tap_screen(750, 857)
        try:
            self.color_match_wait_click(407, 1638, 140, 216, 152)
        except:
            print("Gift not sent !?!?")
        sleep(0.5)
        if self.color_match(105, 1000, 232, 128, 181):
            print("No gifts")   
        # self.color_match_wait_click(503, 1820, 30, 134, 149)
        return True
    
    def gift_send2(self):
        if self.color_match(195, 1630, 222, 60, 190):
            self.log.debug("Click send")
            # sys.exit(0)
            self.tap_screen(204, 1703)
            return True
        return False

    def inviteFriend(self, name, league):
        self.log.warning("Invite friend")
        self.friend_search(name)
        time.sleep(1)
        if self.hasGift():
            self.tap_screenBack()
        self.tapBattle()
        self.selectLeague(league)
        
    def acceptBattleInvite(self):
        self.color_match_wait_click(309, 1275, 157, 218, 150)
        
    def useThisParty(self):
        print("useThisParty start")
        self.color_match_wait_click(329, 1775, 163, 220, 148, threashold=20,time_out_ms=10000)
        print("useThisParty end")
    
    def sort_receive_gift(self, hasGift = True):
        self.color_match_wait_click(857, 1798, 28, 135, 149)
        if hasGift == True:
            self.color_match_wait_click(796, 1431, 44, 113, 119)
        else:
            self.color_match_wait_click(913, 1644, 41, 105, 120)

    def sort_has_gift(self, noGift = False):
        self.screen_friend()
        self.sort_receive_gift()
        self.color_match_wait(838, 220, 255, 255, 255)
        # for x in range(912, 935, 2):
        #    r, g, b = self.get_rgb(x, 1860)
        #    print("X {},{},{},{}".format(x, r, g ,b))
        # sys.exit(0)
        while self.color_match(929, 1860, 170, 245, 205, threashold=20) == noGift:            
            self.sort_receive_gift()
            self.color_match_wait(838, 220, 255, 255, 255)
        else:
            print("Order is OK")
            
    def friendSortCanReceive(self, noGift = False):
        self.screen_friend()
        self.sort_receive_gift(hasGift = False)
        self.color_match_wait(838, 220, 255, 255, 255)
        # for x in range(912, 935, 2):
        #    r, g, b = self.get_rgb(x, 1860)
        #    print("X {},{},{},{}".format(x, r, g ,b))
        # sys.exit(0)
        while self.color_match(929, 1860, 170, 245, 205, threashold=20) == noGift:            
            self.sort_receive_gift(hasGift = False)
            self.color_match_wait(838, 220, 255, 255, 255)
        else:
            print("Order is OK")
            

