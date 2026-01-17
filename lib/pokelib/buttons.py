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
from hybrid_icon_detector import IconDetector

# from hybrid_icon_detector import IconDetector


TESSDATA_PATH = '/usr/share/tesseract/tessdata/'

class ButtonNotFoundError(Exception):
    pass

class PokeClip:
    def __init__(self, ts, xs=0, xe=0, ys=0, ye=0, verbose=0):
        self.ts = ts
        self.pi = PokeImage(ts)
        self.xs = xs
        self.ys = ys
        self.verbose = verbose
        if xe == 0:
            self.xe = ts.specs['max_x']
        if ye == 0:
            self.ye = ts.specs['max_y']
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
    def __init__(self, ts, icon_path, xs=0, xe=0, ys=0, ye=0, verbose=0):
        super().__init__(ts, xs=xs, xe=xe, ys=ys, ye=ye, verbose=verbose)
        self.icons = { 
             'pokeball': cv2.imread(icon_path, cv2.IMREAD_GRAYSCALE)
        }
        self.detector = IconDetector(self.icons, offset=(self.xs, self.ys))     


    def press(self, *args, **kwargs):
        det = self.search(*args, **kwargs)
        if det:
            if kwargs.get('verbose', 0) > 2:
                print(f"Pressing icon button '{det.icon_name}' at {det.center}")
            sleep(kwargs.get('delay', 0.01))
            self.ts.tap_screen(det.center, scale=False)
            return det
        else:
            raise ButtonNotFoundError("Icon button not found.") 
        
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

class Buttons:
    def __init__(self, ts):
        self.ts = ts
        self.ocr = Ocr(ts)
        self.image = ts.image
        self.pokeball = IconButton(ts, 'icons/home_pokeball.png',
                                   ys= int(ts.specs['max_y'] * 0.8))

    def __del__(self):
        pass

    def _button(self, name, npa=None, verbose=0):
        if npa == None:
            npa = self.ts.image.scan_region(xs=self.ocr.startx, 
                                         ys=self.ocr.starty, 
                                         xe=self.ocr.endx, 
                                         ye=self.ocr.endy, 
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
                    w['left'] += box['x'] + w['left'] + self.ocr.startx
                    w['top']  += box['y'] + w['top'] + self.ocr.starty
                    w['center'] = (w['center'][0] + box['x'], w['center'][1] + box['y'])                  
                    return w, self.npa

        return None, self.npa
    

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
        return self._generic_button(self._button, *args, **kwargs)

    def _boxed_button(self, *args, **kwargs):
        return self._generic_button(self._button, *args, **kwargs)

    def dark(self, *args, **kwargs):
        self.ocr.invert = True
        return self._boxed_button(*args, **kwargs)

    def white(self, *args, **kwargs):
        return self._boxed_button(*args, **kwargs)
    
    def black_on_white(self, *args, **kwargs):
        self.ocr.invert = False
        return self._text_from_screen(*args, **kwargs)

    def white_on_black(self, *args, **kwargs):
        self.ocr.invert = False
        return self._text_from_screen(*args, **kwargs)

    def pokeball(self):
        self.ts.tap_screen(292, 921, scale=False)

    
