import re
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
    'exits': {
        'exit_bright': 'exit_bright.png',
        'exit_dark': 'exit_dark.png',
        'exit_check_dark': 'exit_check_dark.png',
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
    'friends_gift': {
        'friends_gift': 'friends_gift.png',
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
    'route_started': {
        'route_started': 'route_started.png',
    },
    'route_end': {
        'route_end': 'route_end.png',
    },
    'catch_ball': {
        'red_5': 'red-5.png',
        'red_6': 'red-6.png',
        'red_7': 'red-7.png',
        'red_8': 'red-8.png',
        'red_9': 'red-9.png',
    },
    'catch_berry': {
        'catch_berry': 'catch_berry.png',
    },
    'buttons': {
        'ok': 'button-ok.png',
    },
    'test_button': {
        'test_button': 'screen-shots/test_button.png',
    },
}


class ButtonNotFoundError(Exception):
    pass

class ButtonParameter:
    def __init__(self, ts, xs=0, xe=0, ys=0, ye=0,
                 confidence=25.0, invert=False, process=False,
                 color='gray', delay= 0.01, mode='word'):
        self.ts = ts
        self.reg = ScreenRegion(ts, xs=xs, xe=xe, ys=ys, ye=ye)
        if xe == 0:
            xe = ts.specs['max_x']
        if ye == 0:
            ye = ts.specs['max_y']

        self.confidence = confidence
        self.invert = invert
        self.process = process
        self.color = color
        self.mode = mode
        self.delay = delay
        self.npa = None
 
    def __del__(self):
        pass

    def press(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass

    def correct_button_positon(self, reg, b):
        b['left'] += reg.xs
        b['top'] += reg.ys
        b['center'] = (b['center'][0] + reg.xs,
                       b['center'][1] + reg.ys)

class Coordinates(ButtonParameter):
    def __init__(self, ts, xs=0, xe=0, ys=0, ye=0):
        super.__init__(ts, xs=xs, xe=xe, ys=ys, ye=ye)

'''
Text only now extra surrounding
'''
class TextOnly(ButtonParameter):
    def __init__(self, ts, text, invert=False, xs=0, xe=0, ys=0, ye=0):
        super().__init__(ts, xs=xs, xe=xe, ys=ys, ye=ye)
        self.text = text
        self.invert = invert
        self.updated = False

    def search(self, text,
                xs=0, xe=0, ys=0, ye=0,               
                threshold=0.8,
                mode='word',
                delay=0.01,
                retries=1,
                invert=False,
                process=False,
                verbose=0):
        reg = ScreenRegion(self.ts, 
                           xs=xs, xe=xe, 
                           ys=ys, ye=ye)
        reg.mode = mode
        reg.invert = invert
        reg.process = process
        b, _ = self.ts.buttons.flat_text_button(text,
                                                reg, 
                                                retries=retries,
                                                delay=delay,
                                                verbose=verbose)
        return b
        

    def press(self, *args, **kwargs):
        b = self.search(*args, **kwargs)
        if b:
            if 'delay' in kwargs:
                sleep(delay)
            else:
                sleep(self.delay)
            # self.ts.tap_screen(b['center'][0], b['center'][1], scale=False)
            self.ts.tap_screen(b['center'], scale=False)
        return b

'''
Button shape with text
'''
class TextButton(ButtonParameter):
    def __init__(self, ts, text="", invert=False, xs=0, xe=0, ys=0, ye=0):
        super().__init__(ts, xs=xs, xe=xe, ys=ys, ye=ye)
        self.text = text
        self.reg.invert = invert
        self.updated = False

    def search(self,
                threshold=0.8,
                delay=0.01,
                retries=1, 
                verbose=0):
        b = Buttons(self.ts)
        if self.invert:
            return b.dark(
                self.text,
                reg=self.reg,
                action='check',
                delay=delay,
                retries=retries, 
                verbose=verbose)
        else:
            return b.white(
                self.text,
                reg=self.reg,
                action='check',
                delay=delay,
                retries=retries, 
                verbose=verbose)

        

class IconButton(ButtonParameter):
    def __init__(self, ts, icons, xs=0, xe=0, ys=0, ye=0):
        super().__init__(ts, xs=xs, xe=xe, ys=ys, ye=ye)
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

    def press(self, verbose=0, *args, **kwargs):
        det = self.search(*args, **kwargs)
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
                threshold=0.8,
                retries=3,
                delay=0.01,
                verbose=0):
        if verbose > 1:
            print("Searching for icon button...")
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
            return hdet
        if verbose > 1:
            print("Icon button not found.")
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
    def __init__(self, ts, xs=0, xe=0, ys=0, ye=0):
        super().__init__(ts, xs=xs, xe=xe, ys=ys, ye=ye)
        self.ocr = Ocr(ts)
        self.image = ts.image
        self.text_only = TextOnly(ts, "")
        self.i_pokeball = IconButton(ts, 'pokeball',
                                    xs=int(ts.specs['max_x'] * 0.38),
                                    xe=int(ts.specs['max_x'] * 0.62),
                                    ys=int(ts.specs['max_y'] * 0.85),
                                    ye=int(ts.specs['max_y'] * 0.97))
        self.i_exits = IconButton(ts, 'exits',
                                    xs=int(ts.specs['max_x'] * 0.38),
                                    xe=int(ts.specs['max_x'] * 0.62),
                                    ys=int(ts.specs['max_y'] * 0.85),
                                    ye=int(ts.specs['max_y'] * 0.97))
        self.i_poke_stop_check = IconButton(ts, 'poke_stop_check',
                                    xs=int(ts.specs['max_x'] * 0.38),
                                    xe=int(ts.specs['max_x'] * 0.62),
                                    ys=int(ts.specs['max_y'] * 0.15),
                                    ye=int(ts.specs['max_y'] * 0.25))
        self.i_has_gift = IconButton(ts, 'has_gift',
                                    xs=int(ts.specs['max_x'] * 0.70),
                                    xe=int(ts.specs['max_x'] * 0.98),
                                    ys=int(ts.specs['max_y'] * 0.84),
                                    ye=int(ts.specs['max_y'] * 0.99))
        self.i_sort = IconButton(ts, 'sort',
                                    xs=int(ts.specs['max_x'] * 0.70),
                                    xe=int(ts.specs['max_x'] * 0.98),
                                    ys=int(ts.specs['max_y'] * 0.80),
                                    ye=int(ts.specs['max_y'] * 0.99))
        self.i_change_sort = IconButton(ts, 'change_sort',
                                    xs=int(ts.specs['max_x'] * 0.60),
                                    xe=int(ts.specs['max_x'] * 0.98),
                                    ys=int(ts.specs['max_y'] * 0.80),
                                    ye=int(ts.specs['max_y'] * 0.99))
        self.i_friends_gift = IconButton(ts, 'friends_gift',
                                    xs=int(ts.specs['max_x'] * 0.20),
                                    xe=int(ts.specs['max_x'] * 0.43),
                                    ys=int(ts.specs['max_y'] * 0.32),
                                    ye=int(ts.specs['max_y'] * 0.50))
        self.i_friend_has_gift = IconButton(ts, 'friend_has_gift',
                                    xs=int(ts.specs['max_x'] * 0.38),
                                    xe=int(ts.specs['max_x'] * 0.62),
                                    ys=int(ts.specs['max_y'] * 0.38),
                                    ye=int(ts.specs['max_y'] * 0.57))
        self.i_test_button = IconButton(ts, 'test_button',
                                    xs=int(ts.specs['max_x'] * 0.38),
                                    xe=int(ts.specs['max_x'] * 0.62),
                                    ys=int(ts.specs['max_y'] * 0.38),
                                    ye=int(ts.specs['max_y'] * 0.57))
        self.i_gym_photo_disk = IconButton(ts, 'gym_photo_disk',
                                    xs=int(ts.specs['max_x'] * 0.8),
                                    xe=int(ts.specs['max_x']),
                                    ys=int(ts.specs['max_y'] * 0.85),
                                    ye=int(ts.specs['max_y']))
        self.i_gym_defeat = IconButton(ts, 'gym_defeat',
                                    xs=int(ts.specs['max_x'] * 0.8),
                                    xe=int(ts.specs['max_x']),
                                    ys=int(ts.specs['max_y'] * 0.75),
                                    ye=int(ts.specs['max_y'] * 0.90))
        tb=0.02
        self.i_catch_ball = IconButton(ts, 'catch_ball',
                                    xs=int(ts.specs['max_x'] * (0.45 - tb)),
                                    xe=int(ts.specs['max_x'] * (0.56 + tb)),
                                    ys=int(ts.specs['max_y'] * (0.88 - tb)),
                                    ye=int(ts.specs['max_y'] * (0.96 + tb)))
        
        self.i_catch_berry = IconButton(ts, 'catch_berry',
                                    xs=int(ts.specs['max_x'] * 0.07),
                                    xe=int(ts.specs['max_x'] * 0.18),
                                    ys=int(ts.specs['max_y'] * 0.85),
                                    ye=int(ts.specs['max_y'] * 0.96))
        
        self.i_gym_defeat_in_battle = IconButton(ts, 'gym_defeat_in_battle',
                                    xs=int(ts.specs['max_x'] * 0.8),
                                    xe=int(ts.specs['max_x']),
                                    ys=int(ts.specs['max_y'] * 0.85),
                                    ye=int(ts.specs['max_y'] * 0.95))
        self.i_gym_mine = IconButton(ts, 'gym_mine',
                                    xs=int(ts.specs['max_x'] * 0.8),
                                    xe=int(ts.specs['max_x']),
                                    ys=int(ts.specs['max_y'] * 0.70),
                                    ye=int(ts.specs['max_y'] * 0.90))
        self.i_route_started = IconButton(ts, 'route_started',
                                    xs=int(ts.specs['max_x'] * 0.8),
                                    xe=int(ts.specs['max_x']),
                                    ys=int(ts.specs['max_y'] * 0.70),
                                    ye=int(ts.specs['max_y'] * 0.90))
        self.i_route_end = IconButton(ts, 'route_end',
                                    xs=int(ts.specs['max_x'] * 0.8),
                                    xe=int(ts.specs['max_x']),
                                    ys=int(ts.specs['max_y'] * 0.70),
                                    ye=int(ts.specs['max_y'] * 0.90))
        self.i_button_ok = IconButton(ts, 'buttons',
                                    xs=int(ts.specs['max_x'] * 0.4),
                                    xe=int(ts.specs['max_x'] * 0.6),
                                    ys=int(ts.specs['max_y'] * 0.5),
                                    ye=int(ts.specs['max_y'] * 0.7))
        self.b_passanger_fast = TextButton(ts, 'SS', # I M A PASSANGER
                                    invert=True,
                                    xs=int(ts.specs['max_x'] * 0.45),
                                    xe=int(ts.specs['max_x'] * 0.55),
                                    ys=int(ts.specs['max_y'] * 0.65),
                                    ye=int(ts.specs['max_y'] * 0.72))
        self.b_catch_berry = TextButton(ts, 'Berry', # I M A PASSANGER
                                    invert=True,
                                    ys=int(ts.specs['max_y'] * 0.40),
                                    ye=int(ts.specs['max_y'] * 0.72))

    def __del__(self):
        pass

    def _button(self, name, reg : ScreenRegion=None, verbose=0):
        reg = reg or ScreenRegion(self.ts)
        if reg.npa is None:
            reg.npa = self.ts.image.scan_region(reg)
    
        boxes = self.image.boxes_get(reg.npa, verbose=verbose)            

        for box in boxes:
            box_reg = ScreenRegion(self.ts) # , xs=box['x'], ys=box['y'])
            box_reg.npa = self.image.process_array(box['rois'], 
                                            self.ocr.invert,
                                            self.ocr.process,
                                            verbose=verbose)
            
            if verbose > 5:
                self.ts.image.show_image(box_reg.npa, wait=000, title='button-candidate-preprocessed')
            if box_reg.npa is None:
                continue

            words = self.ocr._tesserocr_from_array(box_reg)
            # texts = self._concat_tesserocr_results(words)
            for w in words:
                if verbose > 2:
                    print("Found word: {}".format(w['text']))
                if re.search(f'{name}', w['text']):
                    # self.ts.sc.show_image(roi, wait=000, title='button-candidate-preprocessed')
                    # w['left'] += box['x'] + w['left'] + self.ocr.startx
                    # Add region offset to box offset
                    box['x'] += reg.xs
                    box['y'] += reg.ys
                    w['left'] = box['x'] + w['left']
                    w['top']  = box['y'] + w['top']
                    w['center'] = (w['center'][0] + box['x'], \
                                    w['center'][1] + box['y'])
                    return w, self.npa

        return None, self.npa

    def flat_text_button(self, text, reg=None, 
                         delay=0.1, action='press', retries=1, verbose=0):
        button = None

        while button is None and retries > 0:
            retries -= 1
            reg.npa = self.ts.image.scan_region(reg)
            button, npa = self.ocr.regex(text, reg=reg, verbose=verbose)

        if button is not None:
            self.correct_button_positon(self.reg, button)
        return button, reg

    def _generic_button(self, 
                        method,
                        text, 
                        reg : ScreenRegion=None,
                        action='press', 
                        retries=3,
                        delay=0.01,
                        verbose=0):
        reg = reg or ScreenRegion(self.ts)
        ret = None
        while retries > 0:
            reg.npa = None
            print(f'Retry - {retries}')
            button, _ = method(text, reg,
                                 verbose=0)
            if button:
                if action == 'press':
                    if verbose > 2:
                        print(f"Pressing button '{text}' at {button['center']} with delay {delay}s")
                    sleep(delay)
                    self.ts.tap_screen(button['center'], scale=False)



                    ret = button
                    break
                elif action == 'check':
                    ret = button
                    break
            retries -= 1
            if retries > 0:
                sleep(0.7)
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
        self.ocr.invert = False
        self.ocr.process = False
        return self._text_from_screen(*args, **kwargs)

    def white_on_black(self, *args, **kwargs):
        self.ocr.invert = True
        return self._text_from_screen(*args, **kwargs)

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

