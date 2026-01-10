import re
# import numpy as np
# from PIL import Image
# import easyocr
# import pytesseract
# import cv2
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

    def green(self, text, action='press', retries=3, verbose=0):
        self.ocr.invert = True
        ret = None
        while retries > 0:
            button, npa = self.ocr.button(text, verbose=verbose)
            if button:
                if action == 'press':
                    self.ts.tap_screen(button['center'], scale=False)
                    ret = button
                    break
                elif action == 'check':
                    ret = button
                    break
                sleep(0.5)
            retries -= 1
            print("Retrying to find green button '{}' ({} retries left)".format(text, retries))
            sleep(1)
        self.ocr.reset_parameters()
        return ret
    
    def black_on_white(self, text, action='press', retries=3, verbose=0):
        self.ocr.invert = False
        ret = None
        while retries > 0:
            button, npa = self.ocr.regex(text, verbose=verbose)
            if button:
                if action == 'press':
                    self.ts.tap_screen(button['center'], scale=False)
                    ret = button
                    break
            retries -= 1
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
            retries -= 1
        self.ocr.reset_parameters()
        return ret
