import re
from turtle import st
# import numpy as np
# from PIL import Image
# import easyocr
# import pytesseract
import cv2
# from pytesseract import Output
# from tesserocr import PyTessBaseAPI, RIL, iterate_level, PSM
# import pandas as pd
from time import sleep
import re

from .ocr import Ocr
from .image import PokeImage
from .structs import ScreenRegion
from pokelib import ExPokeLibFatal
from hybrid_icon_detector import IconDetector
import numpy as np
from dataclasses import dataclass

# from hybrid_icon_detector import IconDetector


TESSDATA_PATH = '/usr/share/tesseract/tessdata/'

ICONS_PATH = {
    'mag_glass': {
        'mag_glass_1' : 'mag_glass_1.png',
        'mag_glass_2' : 'mag_glass_2.png',
    },
    'evolve': {
        'evolve' : 'evolve.png',
    },
    'menu_battle': {
        'menu_battle': 'menu_battle.png',
    },
    'exits': {
        'exit_bright': 'exit_bright.png',
        'exit_dark': 'exit_dark.png',
        'exit_check_dark': 'exit_check_dark.png',
    },
    'exit_man': {
        'exit_man': 'exit_man.png',
        'exit_man_2': 'exit_man_2.png',
        'exit_man_3': 'exit_man_3.png',
    },
    'menu_items': {
        'menu_items': 'menu_items.png',
    },
    'pokeball': {
        'home_pokeball': 'home_pokeball.png'
    },
    'poke_stop_check': {
        'poke_stop_check': 'poke_stop_lure.png'
    },
    'friends_a_z': {
        'a_z': 'friends_az.png',
    },
    'sort': {
        'down': 'sort_down.png',
        'up': 'sort_up.png',
    },
    'change_sort': {
        'change_sort': 'change_sort.png',
    },
    'has_gift': {
        'has_gift': 'has_gift.png',
    },
    'sort_has_gift': {
        'sort_has_gift': 'has_gift.png',
    },
    'can_receive_gift': {
        'has_gift': 'can_receive_gift.png',
    },
    'sort_can_receive_gift': {
        'has_gift': 'can_receive_gift.png',
    },
    'friends_gift': {
        'friends_gift': 'friends_gift.png',
        'friends_gift': 'friends_gift_2.png',
    },
    'friend_has_gift': {
        'friend_gift': 'friend_has_gift.png',
    },
    'gym_photo_disk': {
        'friend_gift': 'gym-photo-disk.png',
    },
    'gym_defeat': {
        'friend_gift': 'gym-defeat.png',
    },
    'gym_defeat_in_battle': {
        'gym_defeat_in_battle': 'gym_defeat_in_battle.png',
    },
    'gym_mine': {
        'gym_mine': 'gym_mine.png',
    },
    'friends_search': {
        'friends_search': 'friends_search.png',
    },
    'route_started': {
        'route_started': 'route_started.png',
    },
    'route_end': {
        'route_end': 'route_end.png',
    },
    'route_pause': {
        'route_pause': 'route_pause.png',
    },
    'go_out_bright': {
        'go_out_bright': 'go_out_bright.png'
    },
    'raid_battle': {
        'go_out_bright': 'raid_battle.png'
    },
    'catch_ball': {
        'red-ball-0.png': 'red-ball-0.png',
        'red-ball-1.png': 'red-ball-1.png',
        'red-ball-2.png': 'red-ball-2.png',
        'red-ball-3.png': 'red-ball-3.png',
        'red-ball-4.png': 'red-ball-4.png',
        'red-ball-5.png': 'red-ball-5.png',
        'red-ball-6.png': 'red-ball-6.png',
        'red-ball-7.png': 'red-ball-7.png',
        'red-ball-8.png': 'red-ball-8.png',
        'red-ball-9.png': 'red-ball-9.png',
        'blue-ball-0.png': 'blue-ball-0.png',
        'blue-ball-1.png': 'blue-ball-1.png',
        'blue-ball-2.png': 'blue-ball-2.png',
        'blue-ball-3.png': 'blue-ball-3.png',
        'blue-ball-4.png': 'blue-ball-4.png',
        'blue-ball-5.png': 'blue-ball-5.png',
        'blue-ball-6.png': 'blue-ball-6.png',
        'blue-ball-7.png': 'blue-ball-7.png',
        'blue-ball-8.png': 'blue-ball-8.png',
        'blue-ball-9.png': 'blue-ball-9.png',
        'black-ball-0.png': 'black-ball-0.png',
        'black-ball-1.png': 'black-ball-1.png',
        'black-ball-2.png': 'black-ball-2.png',
        'black-ball-3.png': 'black-ball-3.png',
        'black-ball-4.png': 'black-ball-4.png',
        'black-ball-5.png': 'black-ball-5.png',
        'black-ball-6.png': 'black-ball-6.png',
        'black-ball-7.png': 'black-ball-7.png',
        'black-ball-8.png': 'black-ball-8.png',
        'black-ball-9.png': 'black-ball-9.png',
        'raid-ball-50.png': 'raid-ball-50.png',
        'raid-ball-51.png': 'raid-ball-51.png',
        'raid-ball-52.png': 'raid-ball-52.png',
        'raid-ball-53.png': 'raid-ball-53.png',
        'raid-ball-54.png': 'raid-ball-54.png',
        'raid-ball-55.png': 'raid-ball-55.png',
        'raid-ball-56.png': 'raid-ball-56.png',
        'raid-ball-57.png': 'raid-ball-57.png',
        'raid-ball-58.png': 'raid-ball-58.png',
        'raid-ball-59.png': 'raid-ball-59.png',
        'raid-ball-5.png': 'raid-ball-5.png',
        'raid-ball-70.png': 'raid-ball-70.png',
        'raid-ball-71.png': 'raid-ball-71.png',
        'raid-ball-72.png': 'raid-ball-72.png',
        'raid-ball-73.png': 'raid-ball-73.png',
        'raid-ball-74.png': 'raid-ball-74.png',
        'raid-ball-75.png': 'raid-ball-75.png',
        'raid-ball-76.png': 'raid-ball-76.png',
        'raid-ball-77.png': 'raid-ball-77.png',
        'raid-ball-78.png': 'raid-ball-78.png',
        'raid-ball-79.png': 'raid-ball-79.png',
        'raid-ball-7.png': 'raid-ball-7.png',
        'raid-ball-90.png': 'raid-ball-90.png',
        'raid-ball-91.png': 'raid-ball-91.png',
        'raid-ball-92.png': 'raid-ball-92.png',
        'raid-ball-93.png': 'raid-ball-93.png',
        'raid-ball-94.png': 'raid-ball-94.png',
        'raid-ball-95.png': 'raid-ball-95.png',
        'raid-ball-96.png': 'raid-ball-96.png',
        'raid-ball-97.png': 'raid-ball-97.png',
        'raid-ball-98.png': 'raid-ball-98.png',
        'raid-ball-99.png': 'raid-ball-99.png',
        'raid-ball-9.png': 'raid-ball-9.png'

    },
    'catch_berry': {
        'catch_berry': 'catch_berry.png',
    },
    'buttons': {
        'ok': 'button-ok.png',
    },
    'fake_3dot': {
        'fake_3dot': 'fake_3dot.png',
    },
    'fake_app': {
        'fake_app': 'fake_app.png',
        'fake_app_2': 'fake_app_2.png',
    },
    'fake_map': {
        'fake_map': 'fake_map.png',
    },
    'fake_search': {
        'fake_search': 'fake_search.png',
    },
    'test_button': {
        'test_button': 'screen-shots/test_button.png',
    },
    'grunt_r': {
        'grunt_r_1': 'grunt-r-1.png',
        'grunt_r_2': 'grunt-r-2.png',
        'grunt_r_3': 'grunt-r-3.png',
        'grunt_r_4': 'grunt-r-4.png',
        'grunt_r_9': 'grunt-r-9.png',
        'grunt_r_10': 'grunt-r-10.png',
        'grunt_r_11': 'grunt-r-11.png',
    },
    'grunt_more_r': {
        'grunt_r_5': 'grunt-r-5.png',
        'grunt_r_6': 'grunt-r-6.png',
        'grunt_r_7': 'grunt-r-7.png',
        'grunt_r_8': 'grunt-r-8.png',
    },
    'egg_select': {
        'egg_2km': 'egg_2km.png',
        'egg_5km': 'egg_5km.png',
        'egg_7km': 'egg_7km.png',
        'egg_10km': 'egg_10km.png',
    },
    'egg_incubator_8': {
        'egg_incubator_8': 'egg_incubator_8.png',
        'egg_incubator_8_sym': 'egg_incubator_8_sym.png',
    },
    'x_clear_text': {
        'x_clear_button': 'x_clear_text.png',
    }
}

'''
Some buttons need an special test in a call back
'''
def _cb_pokeball(ts, det):
    print('Call back for pokeball')
    x = (det.quad[0][0] + det.quad[1][0]) // 2
    y = det.quad[3][1]
    if ts.color_match(x, y , 254, 254, 254, threashold=1, scale=False):
        # print('Return det')
        return det
    # print("Not home")
    return None
   

class ButtonNotFoundError(Exception):
    pass

class ButtonParameter:
    def __init__(self, reg: ScreenRegion, \
                 confidence=25.0, delay= 0.01, \
                 search_callback=None, 
                 press_callback=None, \
                 verbose=0):
        self.reg = reg
        self.ts = reg.ts
        self.search_callback = search_callback
        self.press_callback = press_callback
        self.delay = delay
        self.verbose = verbose

 
    def __del__(self):
        pass

    def press(self, *args, **kwargs):
        b = self.search(*args, **kwargs)
        if b:
            if 'delay' in kwargs:
                sleep(kwargs['delay'])
            else:
                sleep(self.delay)
            # self.ts.tap_screen(b['center'][0], b['center'][1], scale=False)
            x,y = b['center']
            if 'where' in kwargs:
                where = kwargs['where']
                if where == 'under':
                    y = b['top'] + 2 * b['height']
            self.ts.tap_screen(x, y, scale=False)
        return b
    
    def search(self, *args, **kwargs):
        return None

    def correct_button_positon(self, reg, b):
        b['left'] += reg.xs
        b['top'] += reg.ys
        b['center'] = (b['center'][0] + reg.xs,
                       b['center'][1] + reg.ys)

class Coordinates(ButtonParameter):
    def __init__(self, reg):
        super.__init__(reg)

'''
class ScanText()
Hovers of the region with a step and search for the text
Paramters are relative
.0,.0 upper left corner
1.0.10 lower right corner
'''
class ScanText(ButtonParameter):
    def __init__(self, reg):
        super.__init__(reg)

    def search(self, reg, text, **kw):
        p = self.ts
        # Calculate steps and windows based on region info
        if reg.scan_dir == 'vertical':
            start = reg
            end = reg.ye
        else:
            start = reg.xs
            end = reg.xe
        # The last scan start one step before end
        offset = (end - start) // reg.scan_step
        scan_reg = ScreenRegion(p, 
                                xs=reg.xs, xe=reg.xe, ys=reg.ys, ye=reg.ye, invert=reg.invert, process=reg.process)

'''
Text only
'''
class TextOnly(ButtonParameter):
    def __init__(self, reg):
        super().__init__(reg)
        sb = StdButtons


    def search(self, text,
                xs=0, xe=0, ys=0, ye=0,               
                threshold=0,
                mode='word',
                delay=0.01,
                retries=1,
                invert=False,
                pause=1,
                process=False,
                verbose=0):
        reg = ScreenRegion(self.ts, 
                           xs=xs, xe=xe, 
                           ys=ys, ye=ye,
                           invert=invert,
                           process=process,
                           threshold=threshold,
                           mode=mode)

        b = self.ts.ocr.regex(text,
                                reg,
                                retries=retries,
                                verbose=verbose)
        if self.search_callback:
            self.search_callback(self.ts, b)
        return b
        

    def press(self, *args, **kwargs):
        b = self.search(*args, **kwargs)
        if b:
            if 'delay' in kwargs:
                sleep(kwargs['delay'])
            else:
                sleep(self.delay)
            # self.ts.tap_screen(b['center'][0], b['center'][1], scale=False)
            self.ts.tap_screen(b['center'], scale=False)
        return b

'''
hover the area with a step and search for the text
'''
class TextScan(ButtonParameter):
    def __init__(self, reg, dir='v'):
        super().__init__(reg)
        self.dir = dir


    def search(self,
               text, 
               dir=None,
               start_rel=0.0, end_rel=1.0, steps=20,
               window_factor=2,**kwargs):
        if dir is None:
            dir = self.dir
        if dir == 'v':
            start = self.ts.rel_y(start_rel)
            end = self.ts.rel_y(end_rel)
            full_range = self.ts.rel_y(1)
        elif dir == 'h':
            start = self.ts.rel_x(start_rel)
            end = self.ts.rel_x(end_rel)
            full_range = self.ts.rel_x(1)
        else:
            raise ValueError("dir must be 'v' or 'h'")
        step = max(1, full_range // steps)
         # correct direction
        end = end - step - 3 if start < end else end
        step = -step if start > end else step

        for coord in range(start, end, step):
            s = coord if start <= end else coord + window_factor * step
            e = coord + window_factor * step if start <= end else coord
            if dir == 'v':
                e = min(e, self.ts.specs['max_y'])
                b = self.ts.buttons.text_only.search(text, ys=s, ye=e, **kwargs)
            else:
                e = min(e, self.ts.specs['max_x'])
                s = max(s, 0)
                print(f'start {s} end {e}')
                b = self.ts.buttons.text_only.search(text, xs=s, xe=e, **kwargs)
            if b:
                return b
        return None

'''
Text only now extra surrounding
'''
class TextFlat(ButtonParameter):
    def __init__(self, reg, text="" , **kwargs):
        super().__init__(reg, **kwargs)
        self.reg = reg
        self.ocr = Ocr(reg.ts)
        self.text = text
        self.updated = False

    def search(self, 
               retries=1, 
               pause=1, 
               delay=0.1,
               where='center',
               retry_callback=None,
               press_callback=None,
               verbose=0):
        if verbose > 1:
            print(f'SEARCH {self.text}')
        b = self.ocr.regex(self.text,
                            self.reg, 
                            retries=retries,
                            pause=pause,
                            retry_callback=retry_callback,
                            verbose=verbose)   
        return b 

'''
Button shape with text
'''
class TextButton(ButtonParameter):
    def __init__(self, reg, text):
        super().__init__(reg)
        self.reg = reg
        self.text = text
        self.updated = False
        self.b = StdButtons(self.reg)

    def search(self,
                threshold=0.8,
                delay=0.01,
                retries=1, 
                call_back=None,
                where='center',
                verbose=0):

        if self.reg.invert:
            return self.b.dark(
                self.text,
                reg=self.reg,
                action='check',
                delay=delay,
                retries=retries, 
                verbose=verbose)
        else:
            return self.b.white(
                self.text,
                reg=self.reg,
                action='check',
                delay=delay,
                retries=retries, 
                verbose=verbose)

        

class IconButton(ButtonParameter):
    def __init__(self, reg, icons, **kwargs):
        ts = reg.ts
        # kwargs['reg'] = reg
        super().__init__(reg, **kwargs)
        self._init_icons(icons)
        self.pi = PokeImage(ts)
        self.updated = False
        self.detector = IconDetector(self.icons, offset=(self.reg.xs, self.reg.ys))     

    def _init_icons(self, icons):
        self.icons = {}
        for name, path in ICONS_PATH[icons].items():
            full_path = f'{self.ts.config_path}/icons/{path}'
            self.icons[name] = cv2.imread(f'{full_path}', cv2.IMREAD_GRAYSCALE)
            if self.icons[name] is None:
                raise FileNotFoundError(f"Icon file not found: {full_path}")

    # def press(self, verbose=0, *args, **kwargs):
    def press(self, verbose=0, *args, **kwargs):
        det = self.search(verbose=verbose, *args, **kwargs)
        if det:
            if kwargs.get('verbose', 0) > 2:
                print(f"Pressing icon button '{det.icon_name}' at {det.center}")
            sleep(kwargs.get('delay', 0.01))
            self.ts.tap_screen(det.center, scale=False)
            return det
        else:
            if verbose > 1:
                self.ts.log.debug("Icon button not found.") 
        
    def search(self,
                # cust_reg=None,
                threshold=0.8,
                retries=3,
                pause=1,
                delay=0.01,
                no_scan=False,
                call_back=None,
                verbose=0):
        if verbose > 1:
            print("Searching for icon button...")
        
        tries = 0
        while True:
            tries += 1
            if not no_scan:
                self.reg.npa = self.pi.scan_region(self.reg)

            if verbose > 5:
                self.ts.image.show_image(self.reg.npa, wait=1000, title='button-area')
            dets = self.detector.detect(self.reg.npa)
            # highest score and det with highest score
            hs = -1
            hdet = None
            for det in dets:
                if det.score >= threshold:
                    if det.score > hs:
                        hs = det.score
                        hdet = det
                    if verbose > 1:
                        print(f"Found icon button with score {det.score} at {det.center}")
            if hs > 0.0:
                if self.search_callback:
                    hdet = self.search_callback(self.ts, hdet)
                return hdet
            if verbose > 1:
                print(f'Icon button not found. retry({tries})')
            if tries >= retries:
                return None
            sleep(pause)
        return None
            
        
    def update_area(self, det):
        if self.updated:
            return
        print(det)
        print(det.quad)
        self.startx = int(det.quad[0][0]) - 5
        self.endx = int(det.quad[2][0]) + 5
        self.starty = int(det.quad[0][1]) - 5
        self.endy = int(det.quad[3][1]) + 5
        self.updated = True


class Buttons(ButtonParameter):
    def __init__(self, reg):
        super().__init__(reg)
        self.image = reg.ts.image
        self.text_only = TextOnly(reg)
        self.scan_vertical = TextScan(reg, dir='v')
        self.scan_horizontal = TextScan(reg, dir='h')
        ts = reg.ts
        self.i_pokeball = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.38),
                                        xe=int(ts.specs['max_x'] * 0.62),
                                        ys=int(ts.specs['max_y'] * 0.85),
                                        ye=int(ts.specs['max_y'] * 0.97)),
                                    'pokeball',
                                    search_callback=_cb_pokeball)
        self.i_exits = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.38),
                                        xe=int(ts.specs['max_x'] * 0.62),
                                        ys=int(ts.specs['max_y'] * 0.85),
                                        ye=int(ts.specs['max_y'] * 0.97)),
                                    'exits')
        self.i_exit_man = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.01),
                                        xe=int(ts.specs['max_x'] * 0.2),
                                        ys=int(ts.specs['max_y'] * 0.03),
                                        ye=int(ts.specs['max_y'] * 0.25)),
                                    'exit_man')
        self.i_poke_stop_check = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.38),
                                        xe=int(ts.specs['max_x'] * 0.62),
                                        ys=int(ts.specs['max_y'] * 0.17),
                                        ye=int(ts.specs['max_y'] * 0.35)),
                                    'poke_stop_check')
        self.i_has_gift = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.70),
                                        xe=int(ts.specs['max_x'] * 0.98),
                                        ys=int(ts.specs['max_y'] * 0.84),
                                        ye=int(ts.specs['max_y'] * 0.99)),
                                    'has_gift')
        self.i_sort_has_gift = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.75),
                                        xe=int(ts.specs['max_x'] * 0.98),
                                        ys=int(ts.specs['max_y'] * 0.60),
                                        ye=int(ts.specs['max_y'] * 0.85)),
                                    'has_gift')
        self.i_can_receive_gift = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.70),
                                        xe=int(ts.specs['max_x'] * 0.98),
                                        ys=int(ts.specs['max_y'] * 0.84),
                                        ye=int(ts.specs['max_y'] * 0.99)),
                                    'can_receive_gift')
        self.i_sort_can_receive_gift = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.75),
                                        xe=int(ts.specs['max_x'] * 0.98),
                                        ys=int(ts.specs['max_y'] * 0.70),
                                        ye=int(ts.specs['max_y'] * 0.95)),
                                    'can_receive_gift')
        self.i_sort = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.70),
                                        xe=int(ts.specs['max_x'] * 0.98),
                                        ys=int(ts.specs['max_y'] * 0.80),
                                        ye=int(ts.specs['max_y'] * 0.99)),
                                    'sort')
        self.i_change_sort = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.60),
                                        xe=int(ts.specs['max_x'] * 0.98),
                                        ys=int(ts.specs['max_y'] * 0.80),
                                        ye=int(ts.specs['max_y'] * 0.99)),
                                    'change_sort')
        self.i_friends_gift = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.20),
                                        xe=int(ts.specs['max_x'] * 0.43),
                                        ys=int(ts.specs['max_y'] * 0.32),
                                        ye=int(ts.specs['max_y'] * 0.50)),
                                    'friends_gift')
        self.i_friend_has_gift = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.38),
                                        xe=int(ts.specs['max_x'] * 0.62),
                                        ys=int(ts.specs['max_y'] * 0.38),
                                        ye=int(ts.specs['max_y'] * 0.57)),
                                    'friend_has_gift')
        self.i_test_button = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.38),
                                        xe=int(ts.specs['max_x'] * 0.62),
                                        ys=int(ts.specs['max_y'] * 0.38),
                                        ye=int(ts.specs['max_y'] * 0.57)),
                                    'test_button')
        self.i_gym_photo_disk = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.8),
                                        xe=int(ts.specs['max_x']),
                                        ys=int(ts.specs['max_y'] * 0.85),
                                        ye=int(ts.specs['max_y'])),
                                    'gym_photo_disk')
        self.i_gym_defeat = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.8),
                                        xe=int(ts.specs['max_x']),
                                        ys=int(ts.specs['max_y'] * 0.75),
                                        ye=int(ts.specs['max_y'] * 0.90)),
                                    'gym_defeat')
        tb=0.02
        self.i_catch_ball = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * (0.43 - tb)),
                                        xe=int(ts.specs['max_x'] * (0.58 + tb)),
                                        ys=int(ts.specs['max_y'] * (0.85 - tb)),
                                        ye=int(ts.specs['max_y'] * (0.98 + tb))),
                                    'catch_ball')
        
        self.i_catch_berry = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.05),
                                        xe=int(ts.specs['max_x'] * 0.20),
                                        ys=int(ts.specs['max_y'] * 0.80),
                                        ye=int(ts.specs['max_y'] * 0.96)),
                                    'catch_berry')
        
        self.i_gym_defeat_in_battle = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.8),
                                        xe=int(ts.specs['max_x']),
                                        ys=int(ts.specs['max_y'] * 0.85),
                                        ye=int(ts.specs['max_y'] * 0.95)),
                                    'gym_defeat_in_battle')
        self.t_pokestop_battle = TextButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.2),
                                        xe=int(ts.specs['max_x'] * 0.8),
                                        ys=int(ts.specs['max_y'] * 0.50),
                                        ye=int(ts.specs['max_y'] * 0.90),
                                        invert=True,
                                        process=True),                                       
                                        'BATTLE')
        self.t_grunt_party = TextButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.2),
                                        xe=int(ts.specs['max_x'] * 0.8),
                                        ys=int(ts.specs['max_y'] * 0.60),
                                        ye=int(ts.specs['max_y'] * 0.97),
                                        invert=True,
                                        process=True),                                       
                                        'PARTY')
        self.b_grunt_rescue = TextButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.0),
                                        xe=int(ts.specs['max_x'] * 1),
                                        ys=int(ts.specs['max_y'] * 0.7),
                                        ye=int(ts.specs['max_y'] * 1),
                                        invert=True,
                                        process=True),                                       
                                        'RESCUE')
        self.b_grunt_rematch = TextButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.2),
                                        xe=int(ts.specs['max_x'] * 0.8),
                                        ys=int(ts.specs['max_y'] * 0.7),
                                        ye=int(ts.specs['max_y'] * 0.9),
                                        invert=True,
                                        process=True),                                       
                                        'REMATCH')
        self.t_grunt_ready = TextFlat(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.0),
                                        xe=int(ts.specs['max_x'] * 0.3),
                                        ys=int(ts.specs['max_y'] * 0.1),
                                        ye=int(ts.specs['max_y'] * 0.35),
                                        invert=False,
                                        process=True),                                       
                                        'Grunt')
        self.i_gym_mine = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.8),
                                        xe=int(ts.specs['max_x']),
                                        ys=int(ts.specs['max_y'] * 0.70),
                                        ye=int(ts.specs['max_y'] * 0.90)),
                                        'gym_mine')
        self.i_friends_search = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.5),
                                        xe=int(ts.specs['max_x'] * 0.8),
                                        ys=int(ts.specs['max_y'] * 0.10),
                                        ye=int(ts.specs['max_y'] * 0.40)),
                                        'friends_search')
        self.i_route_started = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.8),
                                        xe=int(ts.specs['max_x']),
                                        ys=int(ts.specs['max_y'] * 0.60),
                                        ye=int(ts.specs['max_y'] * 0.90)),
                                    'route_started')
        self.i_route_end = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.8),
                                        xe=int(ts.specs['max_x']),
                                        ys=int(ts.specs['max_y'] * 0.70),
                                        ye=int(ts.specs['max_y'] * 0.90)),
                                    'route_end')
        self.i_route_pause = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.8),
                                        xe=int(ts.specs['max_x']),
                                        ys=int(ts.specs['max_y'] * 0.70),
                                        ye=int(ts.specs['max_y'] * 0.90)),
                                    'route_pause')
        self.i_button_ok = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.4),
                                        xe=int(ts.specs['max_x'] * 0.6),
                                        ys=int(ts.specs['max_y'] * 0.5),
                                        ye=int(ts.specs['max_y'] * 0.8)),
                                    'buttons')
        self.i_go_out_bright = IconButton(ScreenRegion(ts,
                                        xs=int(ts.specs['max_x'] * 0.02),
                                        xe=int(ts.specs['max_x'] * 0.16),
                                        ys=int(ts.specs['max_y'] * 0.12),
                                        ye=int(ts.specs['max_y'] * 0.25)),
                                    'go_out_bright')
        self.i_x_clear_text = IconButton(ScreenRegion(ts,
                                            xs=ts.rel_x(0.75),
                                            xe=ts.rel_x(0.99),
                                            ys=ts.rel_y(0.20),
                                            ye=ts.rel_y(0.50)),
                                        'x_clear_text')
        self.i_fake_app = IconButton(ScreenRegion(ts), 'fake_app')
        self.i_grunt_r = IconButton(ScreenRegion(ts), 'grunt_r')
        self.i_fake_3dot = IconButton(ScreenRegion(ts, ye=int(ts.specs['max_y'] * 0.2)), 'fake_3dot')
        self.i_fake_map = IconButton(ScreenRegion(ts, ye=int(ts.specs['max_y'] * 0.2)), 'fake_map')
        self.i_fake_search = IconButton(ScreenRegion(ts, ye=int(ts.specs['max_y'] * 0.2)), 'fake_search')
        self.i_raid_battle = IconButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.2),
                                    xe=ts.rel_x(0.8),
                                    ys=ts.rel_y(0.5),
                                    ye=ts.rel_y(0.8)),
                                    'raid_battle')
        self.b_passenger_fast = TextButton(ScreenRegion(ts,
                                    invert=True,
                                    xs=ts.rel_x(0.45),
                                    xe=ts.rel_x(0.55),
                                    ys=ts.rel_y(0.50),
                                    ye=ts.rel_y(0.72)),
                                    'SS')    # IN PASSANGER
        self.b_passenger = TextButton(ScreenRegion(ts,
                                    invert=True,
                                    xs=ts.rel_x(0.0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.50),
                                    ye=ts.rel_y(0.80),
                                    process=True),
                                    'PASSENGER')    # IN PASSANGER
        self.b_catch_berry = TextButton(ScreenRegion(ts,
                                    invert=True,
                                    process=True,
                                    ys=int(ts.specs['max_y'] * 0.40),
                                    ye=int(ts.specs['max_y'] * 0.72)), 
                                    'Berry')
        self.t_catch_caught = TextFlat(ScreenRegion(ts,
                                    xe=ts.rel_x(0.50),
                                    ys=int(ts.specs['max_y'] * 0.25),
                                    ye=int(ts.specs['max_y'] * 0.50)), 
                                    'CAUGHT')
        self.b_catched_OK = TextButton(ScreenRegion(ts,
                                    invert=True,
                                    process=True,
                                    ys=int(ts.specs['max_y'] * 0.40),
                                    ye=int(ts.specs['max_y'] * 0.80)), 
                                    'OK')
        self.b_open_gift = TextButton(ScreenRegion(ts,
                                    invert=True,
                                    process=True, 
                                    xs=int(ts.specs['max_x'] * 0.20),
                                    xe=int(ts.specs['max_x'] * 0.80),
                                    ys=int(ts.specs['max_y'] * 0.70),
                                    ye=int(ts.specs['max_y'] * 0.95)),
                                    'OPEN')
        self.b_yes = TextButton(ScreenRegion(ts,
                                    invert=True,
                                    process=True,
                                    blur=3,
                                    xs=ts.rel_x(0.10),
                                    xe=ts.rel_x(0.90),
                                    ys=ts.rel_y(0.50),
                                    ye=ts.rel_y(0.80)),
                                    'YES')
        self.b_send_gift = TextButton(ScreenRegion(ts,
                                    invert=True, 
                                    process=True, 
                                    xs=int(ts.specs['max_x'] * 0.20),
                                    xe=int(ts.specs['max_x'] * 0.80),
                                    ys=int(ts.specs['max_y'] * 0.70),
                                    ye=int(ts.specs['max_y'] * 0.95)), 
                                    'SEND')
        self.b_limit = TextButton(ScreenRegion(ts,
                                    invert=True,
                                    process=True, 
                                    xs=int(ts.specs['max_x'] * 0.10),
                                    xe=int(ts.specs['max_x'] * 0.45),
                                    ys=int(ts.specs['max_y'] * 0.35),
                                    ye=int(ts.specs['max_y'] * 0.65)), 
                                    'limit')
        self.t_friends = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.4),
                                    xe=ts.rel_x(0.6),
                                    ys=ts.rel_y(0.05),
                                    ye=ts.rel_y(0.15)),
                                    'IENDS')
        self.t_sign_out = TextFlat(ScreenRegion(ts,
                                    process=True, 
                                    xs=ts.rel_x(0.0),
                                    xe=ts.rel_x(.3),
                                    ys=ts.rel_y(0.05),
                                    ye=ts.rel_y(1)),
                                    'Sign')
        self.t_passenger = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.25),
                                    xe=ts.rel_x(0.75),
                                    ys=ts.rel_y(0.50),
                                    ye=ts.rel_y(0.75),
                                    invert=True,
                                    process=False),
                                    'PASSENGER')
        self.t_cancel = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.4),
                                    xe=ts.rel_x(0.6),
                                    ys=ts.rel_y(0.05),
                                    ye=ts.rel_y(0.15)),
                                    'CANCEL')
        self.t_friends_search = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.5),
                                    xe=ts.rel_x(0.75),
                                    ys=ts.rel_y(0.2),
                                    ye=ts.rel_y(0.4)),
                                    'SEARCH')
        self.t_input_ok = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.8),
                                    xe=ts.rel_x(0.95),
                                    ys=ts.rel_y(0.0),
                                    ye=ts.rel_y(0.65),
                                    invert=True),
                                    'OK')
        self.t_go_battle_gym = TextFlat(ScreenRegion(ts,
                                    process=True,
                                    xs=ts.rel_x(0.2),
                                    xe=ts.rel_x(0.8),
                                    ys=ts.rel_y(0.20),
                                    ye=ts.rel_y(0.50),
                                    invert=True),
                                    'BATTLE')
        self.t_send_gift = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.05),
                                    xe=ts.rel_x(0.30),
                                    ys=ts.rel_y(0.75),
                                    ye=ts.rel_y(1),
                                    color='gray'),
                                    'SEND')
        self.t_returning_player = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.05),
                                    xe=ts.rel_x(0.9),
                                    ys=ts.rel_y(0.1),
                                    ye=ts.rel_y(0.5),
                                    invert=True,
                                    color='blue'),  

                                    'RETURNING')
        self.t_login_google = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.05),
                                    xe=ts.rel_x(0.9),
                                    ys=ts.rel_y(0.3),
                                    ye=ts.rel_y(0.6)),  
                                    'Google')
        self.t_login_choose = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.2),
                                    xe=ts.rel_x(0.9),
                                    ys=ts.rel_y(0.1),
                                    ye=ts.rel_y(1),
                                    invert=True),  
                                    'Choose')
        self.t_setting = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.5),
                                    xe=ts.rel_x(0.9),
                                    ys=ts.rel_y(0.05),
                                    ye=ts.rel_y(0.2),
                                    invert=False),  
                                    'SETTINGS')
        self.t_raid_summary = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.2),
                                    xe=ts.rel_x(0.7),
                                    ys=ts.rel_y(0.3),
                                    ye=ts.rel_y(0.9),
                                    invert=True),  
                                    'SUMMARY')
        self.t_overview_route = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.70),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.1),
                                    ye=ts.rel_y(0.2),
                                    invert=False),  
                                    'ROUTE')
        self.b_route_nearby = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.4),
                                    ye=ts.rel_y(0.8),
                                    invert=False),  
                                    'NEARBY')
        self.b_route_follow = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.4),
                                    ye=ts.rel_y(0.8),
                                    invert=True),  
                                    'FOLLOW')
        self.b_route_complete = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.5),
                                    ye=ts.rel_y(0.9),
                                    invert=True),  
                                    'COMPLETE')
        self.b_route_quit = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.4),
                                    ye=ts.rel_y(0.8),
                                    invert=False),  
                                    'QUIT')
        self.b_lucky_egg = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.5),
                                    ye=ts.rel_y(0.95),
                                    invert=True),  
                                    'LUCKY')
        self.b_egg_incubate = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.4),
                                    ye=ts.rel_y(0.8),
                                    invert=True),  
                                    'INCUBATE')
        self.b_me_egg = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.25),
                                    xe=ts.rel_x(0.75),
                                    ys=ts.rel_y(0),
                                    ye=ts.rel_y(1),
                                    invert=True,
                                    process=True),  
                                    'EGGS')
        self.b_raid_rejoin = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.1),
                                    xe=ts.rel_x(0.9),
                                    ys=ts.rel_y(0.3),
                                    ye=ts.rel_y(0.7),
                                    invert=True,
                                    process=True),  
                                    'REJOIN')
        self.i_egg_select = IconButton(ScreenRegion(ts,
                                        ys=ts.rel_y(0.10),
                                        ye=ts.rel_y(0.80)
                                        ),
                                        'egg_select')
        self.i_egg_incubator_8 = IconButton(ScreenRegion(ts,
                                        xe=ts.rel_x(0.40),
                                        ys=ts.rel_y(0.40),
                                        ye=ts.rel_y(0.90)
                                        ),
                                        'egg_incubator_8')
        self.t_route_known = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.4),
                                    ye=ts.rel_y(0.8),
                                    invert=False),  
                                    'KNOWN')
        self.b_pomon_purify = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.3),
                                    ye=ts.rel_y(1),
                                    invert=True),  
                                    'PURIFY')
        self.b_heal_all = TextButton(ScreenRegion(ts,
                                    process=True,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.5),
                                    ye=ts.rel_y(1),
                                    invert=True),  
                                    'HEAL')
        self.b_revive_all = TextButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(1),
                                    ys=ts.rel_y(0.5),
                                    ye=ts.rel_y(1),
                                    invert=True),  
                                    'REVIVE')
        self.b_trade_next = TextButton(ScreenRegion(ts,
                                        invert=True,
                                        process=True,
                                        xs=ts.rel_x(0),
                                        xe=ts.rel_x(1),
                                        ys=ts.rel_y(0.5),
                                        ye=ts.rel_y(1)),
                                        'NEXT')
        self.t_trade_confirm = TextFlat(ScreenRegion(ts,
                                        invert=True,
                                        xs=ts.rel_x(0.0),
                                        xe=ts.rel_x(.5),
                                        ys=ts.rel_y(0.2),
                                        ye=ts.rel_y(0.8),
                                        ),  
                                        'CONFIRM')
        self.i_evolve = IconButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0),
                                    xe=ts.rel_x(0.5),
                                    ys=ts.rel_y(0.4),
                                    ye=ts.rel_y(1),
                                    ),
                                    'evolve')
        self.i_menu_battle = IconButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.5),
                                    xe=ts.rel_x(.95),
                                    ys=ts.rel_y(0.3),
                                    ye=ts.rel_y(0.65),
                                    ),  
                                    'menu_battle')
        self.t_friend_trade = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.05),
                                    xe=ts.rel_x(.5),
                                    ys=ts.rel_y(0.8),
                                    ye=ts.rel_y(1),
                                    ),  
                                    'LOCAL')
        self.t_menu_pokemon = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.05),
                                    xe=ts.rel_x(.5),
                                    ys=ts.rel_y(0.5),
                                    ye=ts.rel_y(0.90),
                                    ),  
                                    'POK.MON')
        self.t_pokemon_pokemon = TextFlat(ScreenRegion(ts,
                                    xs=ts.rel_x(0.00),
                                    xe=ts.rel_x(1.00),
                                    ys=ts.rel_y(0.00),
                                    ye=ts.rel_y(0.10),
                                    process=True),
                                    'POK.MON')
        self.i_pokemon_search = IconButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.00),
                                    xe=ts.rel_x(1.00),
                                    ys=ts.rel_y(0.00),
                                    ye=ts.rel_y(0.30)),
                                    'mag_glass')
        self.i_menu_items = IconButton(ScreenRegion(ts,
                                    xs=ts.rel_x(0.5),
                                    xe=ts.rel_x(.95),
                                    ys=ts.rel_y(0.5),
                                    ye=ts.rel_y(0.9),
                                    ),  
                                    'menu_items')
        
    def t_gift(self, *args, **kwargs):
        self.startx = self.ocr.startx = int(0.6 * self.ts.specs['max_x'])
        self.endx = self.ocr.endx = int(0.8 * self.ts.specs['max_x'])
        self.starty = self.ocr.starty = int(0.6 * self.ts.specs['max_y'])
        self.endy = self.ocr.endy = int(0.8 * self.ts.specs['max_y'])
        return self.white_on_black('GIFT.*')
    
    def c_avatar(self):
        x = int(0.15 * self.ts.specs['max_x'])
        y = int(0.90 * self.ts.specs['max_y'])
        self.ts.tap_screen(x, y, scale=False)


    def __del__(self):
        pass

class StdButtons(ButtonParameter):
    def __init__(self, reg):
        super().__init__(reg)
        self.ocr = Ocr(reg.ts)

    def _button(self, name, reg : ScreenRegion=None, 
                verbose=0):
        reg = reg or ScreenRegion(self.ts)
        if reg.npa is None:
            reg.npa = self.ts.image.scan_region(reg)

        if reg.blur > 0:
            reg.npa = cv2.blur(reg.npa, (reg.blur, reg.blur))
    
        boxes = self.ts.image.boxes_get(reg, verbose=verbose)            

        for box in boxes:
            box = self.ts.image.process_array(box, verbose=verbose)
            
            if verbose > 5:
                self.ts.image.show_image(box.npa, wait=1500, title='button-candidate-preprocessed')
            if box.npa is None:
                continue

            words = self.ocr._tesserocr_from_array(box)
            # texts = self._concat_tesserocr_results(words)
            for w in words:
                if verbose > 2:
                    print("Found word: {}".format(w['text']))
                if re.search(f'{name}', w['text']):
                    # self.ts.sc.show_image(roi, wait=000, title='button-candidate-preprocessed')
                    # w['left'] += box['x'] + w['left'] + self.ocr.startx
                    # Add region offset to box offset
                    w['left'] = reg.xs + w['left']
                    w['top']  = reg.ys + w['top']
                    w['center'] = (reg.xs + w['center'][0], \
                                   reg.ys + w['center'][1]) 
                    return w, reg

        return None, reg

    def flat_text_button(self, text, reg=None, 
                         delay=0.1, pause=1, retries=1, 
                         invert=False, process=False, verbose=0):
        button = self.ocr.regex(text, 
                                reg=reg, 
                                retries=retries,
                                invert=invert, process=process,
                                pause=pause,
                                verbose=verbose)
 
        # if button is not None and len(button) > 0:
        #     self.correct_button_positon(self.reg, button)
        return button, reg

    def _generic_button(self, 
                        method,
                        text, 
                        reg : ScreenRegion=None,
                        action='press',
                        retries=1,
                        delay=0.01,
                        call_back=None,
                        verbose=0):
        reg = reg or ScreenRegion(self.ts)
        ret = None
        while retries > 0:
            reg.npa = None
            # print(f'Retry - {retries}')
            button, _ = method(text, reg,
                               verbose=verbose)
                                 #verbose=verbose)
            if button:
                if action == 'press':
                    if verbose > 2:
                        print(f"Pressing button '{text}' at {button['center']} with delay {delay}s")
                    sleep(delay)
                    self.ts.tap_screen(button['center'], scale=False)
                    ret = button
                    break
                elif action == 'check' or action == 'search':
                    ret = button
                    break
            retries -= 1
            if retries > 0:
                if call_back:
                    r = call_back()
                    if r:
                        return r
                sleep(1)
        return ret

    def _text_from_screen(self, *args, **kwargs):
        return self._generic_button(self.flat_text_button, *args, **kwargs)

    def _boxed_button(self, *args, **kwargs):
        return self._generic_button(self._button, *args, **kwargs)

    def dark(self, *args, **kwargs):
        self.ocr.invert = True
        return self._boxed_button(*args, **kwargs)

    def white(self, *args, **kwargs):
        return self._boxed_button(*args, **kwargs)
    
    def black_on_white(self, *args, **kwargs):
        reg = ScreenRegion(self.ts, 
                           invert=False,
                           process=True)
        args_list = list(args)
        args_list.insert(1, reg)
        args = tuple(args_list)
        return self._text_from_screen(*args, **kwargs)

    def white_on_black(self, *args, **kwargs):
        reg = ScreenRegion(self.ts, 
                           invert=True,
                           process=True)
        args_list = list(args)
        args_list.insert(1, reg)
        args = tuple(args_list)
        
        return self._text_from_screen(*args, **kwargs)


