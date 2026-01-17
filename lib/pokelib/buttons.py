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

TESSDATA_PATH = '/usr/share/tesseract/tessdata/'




class Buttons:
    def __init__(self, ts):
        self.ts = ts
        self.ocr = Ocr(ts)
        

    def __del__(self):
        pass

    @classmethod
    def starty(cls, y):
        self.ocr.starty = y
    @classmethod
    def endy(cls, y):
        self.ocr.endy = y

    def _button(self, name, npa=None, verbose=0):
        if npa == None:
            npa = self.ts.sc.scan_region(xs=self.ocr.startx, 
                                         ys=self.ocr.starty, 
                                         xe=self.ocr.endx, 
                                         ye=self.ocr.endy, 
                                         channel=self.ocr.color)
        self.npa = npa
    
        boxes = boxes_get(npa, verbose=verbose)            

        for box in boxes:
            roi = self._process_array(box['rois'], verbose=verbose)
            if verbose > 5:
                self.ts.sc.show_image(roi, wait=1000, title='button-candidate-preprocessed')
            words, _ = self.ocr._tesserocr_from_array(roi)
            # texts = self._concat_tesserocr_results(words)
            for w in words:
                if verbose > 2:
                    print("Found word: {}".format(w['text']))
                if re.search(f'{name}', w['text']):
                    # self.ts.sc.show_image(roi, wait=000, title='button-candidate-preprocessed')
                    w['left'] += box['x'] + w['left']
                    w['top']  += box['y'] + w['top']
                    w['center'] = (w['center'][0] + box['x'], w['center'][1] + box['y'])                  
                    return w, self.npa

        return None, self.npa

    def dark(self, text, action='press', retries=3, verbose=0):
        self.ocr.invert = True
        ret = None
        while retries > 0:
            button, npa = self._button(text, verbose=verbose)
            if button:
                if action == 'press':
                    self.ts.tap_screen(button['center'], scale=False)
                    ret = button
                    break
                elif action == 'check':
                    ret = button
                    break
            retries -= 1
            if retries > 0:
                sleep(0.7)
            print("Retrying to find green button '{}' ({} retries left)".format(text, retries))
        self.ocr.reset_parameters()
        return ret

    def white(self, text, action='press', retries=3, verbose=0):
        ret = None
        while retries > 0:
            button, npa = self._button(text, verbose=verbose)
            if button:
                if action == 'press':
                    self.ts.tap_screen(button['center'], scale=False)
                    ret = button
                    break
                elif action == 'check':
                    ret = button
                    break
            retries -= 1
            if retries > 0:
                sleep(0.7)
            print("Retrying to find white button '{}' ({} retries left)".format(text, retries))
        self.ocr.reset_parameters()
        return ret
    
    def black_on_white(self, text, action='press', retries=3, verbose=0, delay=0.01):
        self.ocr.invert = False
        ret = None
        while retries > 0:
            button, npa = self.ocr.regex(text, verbose=verbose)
            if button:
                if action == 'press':
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
    
    def white_on_black(self, text, action='press', retries=3, verbose=0):
        self.ocr.invert = True
        ret = None
        while retries > 0:
            button, npa = self.ocr.regex(text, verbose=verbose)
            if button:
                if action == 'press':
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

    def pokeball(self):
        self.ts.tap_screen(292, 921, scale=False)

    
