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


def boxes_get(img, verbose=0):
    # self.ts.sc.show_image(img, wait=1000, title='unprocessed')
    img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    candidates = []
    H, W = img.shape
    edges = cv2.Canny(img, 50, 150)
    if verbose > 9:
        cv2.imshow('find boxes', img)
        cv2.waitKey(1000)
    contours, _ = cv2.findContours(
        edges,
        # cv2.RETR_EXTERNAL,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
        )
        
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if verbose > 2:
            print(f'Cont : x{x},y{y},w{w},h{h}')
        # reject small stuff
        if area < 0.01 * W * H:
            continue
    
        # reject near-fullscreen
        if area > 0.9 * W * H:
            continue
    
        # aspect ratio sanity
        aspect = w / float(h)
        # if 0.5 < aspect < 2.5: 
        if 0.5 < aspect < 20: 
            candidates.append((x, y, w, h))
        else:
            if verbose > 5:
                print(f"Rejected box x{x},y{y},w{w},h{h} with aspect {aspect:.2f}") 
    unique = set(candidates)
    boxes = []
    if unique:
        for d in unique:
            x, y, w, h = d
            pad = 10  # pixels
            boxes.append({'rois': img[
                y+pad : y+h-pad,
                x+pad : x+w-pad
                ],
                'x': x+pad, 'y': y+pad
                })
            if verbose > 5:
                self.ts.sc.show_image(boxes[-1]['rois'], wait=1000, title='box')
    return boxes

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

    
