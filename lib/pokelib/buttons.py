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
from pokelib import ExPokeLibFatal
from hybrid_icon_detector import IconDetector

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
    }
}

class ButtonNotFoundError(Exception):
    pass

class PokeClip:
    def __init__(self, ts, xs=0, xe=0, ys=0, ye=0, verbose=0):
        self.ts = ts
        self.pi = PokeImage(ts)
        if xe == 0:
            xe = ts.specs['max_x']
        if ye == 0:
            ye = ts.specs['max_y']
        self.xs = xs
        self.ys = ys
        self.xe = xe
        self.ye = ye
        self.verbose = verbose
        self.reset_parameters()

    def __del__(self):
        pass

    def reset_parameters(self):
        self.startx = self.xs
        self.starty = self.ys
        self.endx = self.xe
        self.endy = self.ye
        self.confidence = 20.0
        self.invert = False
        self.process = True
        self.color = 'gray'
        self.mode = 'word'
        self.npa = None

class IconButton(PokeClip):
    def __init__(self, ts, icons, xs=0, xe=0, ys=0, ye=0, verbose=0):
        super().__init__(ts, xs=xs, xe=xe, ys=ys, ye=ye, verbose=verbose)
        self._init_icons(icons)
        self.updated = False
        self.detector = IconDetector(self.icons, offset=(self.xs, self.ys))     

    def _init_icons(self, icons):
        self.icons = {}
        for name, path in ICONS_PATH[icons].items():
            full_path = f'{self.ts.config_path}/icons/{path}'
            self.icons[name] = cv2.imread(f'{full_path}', cv2.IMREAD_GRAYSCALE)
            if self.icons[name] is None:
                raise FileNotFoundError(f"Icon file not found: {full_path}")

    def press(self, *args, **kwargs):
        det = self.search(*args, **kwargs)
        if det:
            if kwargs.get('verbose', 0) > 2:
                print(f"Pressing icon button '{det.icon_name}' at {det.center}")
            sleep(kwargs.get('delay', 0.01))
            self.ts.tap_screen(det.center, scale=False)
            return det
        else:
            self.ts.log.debug("Icon button not found.") 
        
    def search(self, 
                npa=None,
                threshold=0.8,
                action='press', 
                retries=3,
                delay=0.01,
                verbose=0):
        print("Searching for icon button...")
        if npa == None:
            npa = self.pi.scan_region(xs=self.startx, 
                                            ys=self.starty, 
                                            xe=self.endx, 
                                            ye=self.endy, 
                                            channel=self.color)

        if verbose > 5:
            self.ts.image.show_image(npa, wait=1000, title='button-area')
        dets = self.detector.detect(npa)
        # highest score and det with highest score
  
        hs = -1
        hdet = None
        for det in dets:
            if det.score >= threshold:
                if det.score > hs:
                    hs = det.score
                    hdet = det
                print(f"Found icon button with score {det.score} at {det.center}")
        if hs > 0.0:
            return hdet
        print("Icon button not found.")
        return None
    
    def update_area(self, det):
        print(det)
        print(det.quad)
        self.startx = int(det.quad[0][0]) - 5
        self.endx = int(det.quad[2][0]) + 5
        self.starty = int(det.quad[0][1]) - 5
        self.endy = int(det.quad[3][1]) + 5
        self.updated = True


class Buttons:
    def __init__(self, ts):
        self.ts = ts
        self.ocr = Ocr(ts)
        self.image = ts.image
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
                                    ys=int(ts.specs['max_y'] * 0.20),
                                    ye=int(ts.specs['max_y'] * 0.40))
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
                                    xs=int(ts.specs['max_x'] * 0.70),
                                    xe=int(ts.specs['max_x'] * 0.98),
                                    ys=int(ts.specs['max_y'] * 0.80),
                                    ye=int(ts.specs['max_y'] * 0.99))
        self.i_friends_gift = IconButton(ts, 'friends_gift',
                                    xs=int(ts.specs['max_x'] * 0.70),
                                    xe=int(ts.specs['max_x'] * 0.98),
                                    ys=int(ts.specs['max_y'] * 0.80),
                                    ye=int(ts.specs['max_y'] * 0.99))

    def __del__(self):
        pass

    def _button(self, name, npa=None, verbose=0):
        if npa == None:
            npa = self.ts.image.scan_region(xs=self.startx, 
                                         ys=self.starty, 
                                         xe=self.endx, 
                                         ye=self.endy, 
                                         channel=self.ocr.color)
        self.npa = npa
    
        boxes = self.image.boxes_get(npa, verbose=verbose)            

        for box in boxes:
            roi = self.image.process_array(box['rois'], 
                                            self.ocr.invert,
                                            self.ocr.process,
                                            verbose=verbose)
            if verbose > 5:
                self.ts.image.show_image(roi, wait=1000, title='button-candidate-preprocessed')
            words, _ = self.ocr._tesserocr_from_array(roi)
            # texts = self._concat_tesserocr_results(words)
            for w in words:
                if verbose > 2:
                    print("Found word: {}".format(w['text']))
                if re.search(f'{name}', w['text']):
                    # self.ts.sc.show_image(roi, wait=000, title='button-candidate-preprocessed')
                    w['left'] += box['x'] + w['left'] + self.startx
                    w['top']  += box['y'] + w['top'] + self.starty
                    w['center'] = (w['center'][0] + box['x'] + self.startx, \
                                    w['center'][1] + box['y'] + self.starty )
                    return w, self.npa

        return None, self.npa

    def _re_button(self, text, action='press', retries=3, verbose=0):
        ret = None
        while retries > 0:
            button, npa = self.ocr.regex(text, verbose=verbose)
            if button:
                if action == 'press':
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
        self.ocr.reset_parameters()
        return ret, npa

    def _generic_button(self, 
                        method,
                        text, 
                        action='press', 
                        retries=3,
                        delay=0.01,
                        verbose=0):
        ret = None
        while retries > 0:
            button, npa = method(text, verbose=verbose)
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
        self.ocr.reset_parameters()
        return ret

    def _text_from_screen(self, *args, **kwargs):
        return self._generic_button(self.ocr.regex, *args, **kwargs)

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

    def t_friends(self, *args, **kwargs):
        self.ocr.endy = int(0.2 * self.ts.specs['max_y'])
        return self.black_on_white('.*FRIENDS.*')
    
    def t_gift(self, *args, **kwargs):
        self.ocr.startx = int(0.6 * self.ts.specs['max_x'])
        self.ocr.endx = int(0.8 * self.ts.specs['max_x'])
        self.ocr.starty = int(0.6 * self.ts.specs['max_y'])
        self.ocr.endy = int(0.8 * self.ts.specs['max_y'])
        return self.white_on_black('GIFT.*')
    
    def c_avatar(self):
        x = int(0.15 * self.ts.specs['max_x'])
        y = int(0.90 * self.ts.specs['max_y'])
        self.ts.tap_screen(x, y, scale=False)
    
