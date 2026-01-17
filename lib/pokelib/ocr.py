import re
import numpy as np
from PIL import Image
# import easyocr
import pytesseract
import cv2
# from pytesseract import Output
from tesserocr import PyTessBaseAPI, RIL, iterate_level, PSM
import pandas as pd
import re
from .image import PokeImage

TESSDATA_PATH = '/usr/share/tesseract/tessdata/'

class Ocr:
    def __init__(self, ts):
        self.ts = ts
        self.api = PyTessBaseAPI(path=TESSDATA_PATH, lang='eng')
        self.image = PokeImage(ts)
        # self.reader = easyocr.Reader(['en'])
        self.reset_parameters()

    def __del__(self):
        pass

    def reset_parameters(self):
        self.startx = 0
        self.starty = 0
        self.endx = self.ts.specs['max_x']
        self.endy = self.ts.specs['max_y']
        self.confidence = 20.0
        self.invert = False
        self.process = True
        self.color = 'gray'
        self.mode = 'word'
        self.npa = None

    def set_mode(self, mode):
        self.mode = mode
 
    def _tesserocr_from_array(self, array, verbose=0):
        """Run tesserocr on a numpy array and return extracted words plus the PIL image.

        Returns (ocr_data, image)
        """


        if verbose > 5:
            self.ts.sc.show_image(array, wait=4000, title='button-candidate-preprocessed')
        # trigger recognition (GetUTF8Text returns full text, iterator used below)
        # Only tesserocr after here
        # self.api.SetPageSegMode(PSM.SINGLE_WORD)

        h, w = array.shape
        self.api.SetImageBytes(
                array.tobytes(),
                w, h,
                1,      # bytes per pixel (grayscale)
                w       # bytes per line
        )

        # with suppress_stderr():
        t = self.api.GetUTF8Text()
        ri = self.api.GetIterator()
        if self.mode == 'line':
            level = RIL.TEXTLINE
        elif self.mode == 'symbol':
            self.level = RIL.SYMBOL
        else:
            level = RIL.WORD
        # level = RIL.TEXTLINE
        ocr_data = []
        wi = 1
        # For line detection
        button_of_line = -1
        for r in iterate_level(ri, level):
            try:
                text = r.GetUTF8Text(level)
            except:
                continue
            conf = r.Confidence(level)
            left, top, right, bottom = r.BoundingBox(level)
            width = right - left
            height = bottom - top
            if conf > self.confidence:
                # print(f"Detected text: '{text}' with confidence {conf}")
                ocr_data.append({
                    'text': text,
                    'conf': conf,
                    'left': left,
                    'top': top,
                    'width': width,
                    'height': height,
                    'word': wi,
                    'center': ((left + width//2), (top + height//2))
                })
                if len(text) > 1:
                    wi += 1
                else:
                    wi = 1
        # print(f"Total OCR words: {ocr_data}")
        return ocr_data, array
    
    def _concat_tesserocr_results(self, words):
        """Concatenate tesserocr results based on word index."""
        concatenated = []
        for w in words:
            if w['word'] == 1:
                concatenated.append(w)
            else:
                concatenated[-1]['text'] += ' ' + w['text']
        return concatenated
    
    def read_and_npa(self, npa=None,verbose=0):
        if npa == None:
            npa = self.image.scan_region(xs=self.startx, ys=self.starty, xe=self.endx, ye=self.endy, channel=self.color)
        self.npa = npa
        self.p_npa = self.image.process_array(npa, self.invert, self.process, verbose=verbose)
        t, _ = self._tesserocr_from_array(self.p_npa, verbose=verbose)
        self.reset_parameters() 
        return t, self.npa, npa

    def read(self, *args, **kwargs):
        text, self.npa, processed_npa = self.read_and_npa(*args, **kwargs)
        return text


    def regex(self, regex, npa=None, verbose=0):
        lines, self.npa, self.p_npa = self.read_and_npa(npa, verbose=verbose)
        self.reset_parameters()
        for l in lines:
            if re.search(regex, l['text']):
                return l, self.npa

        return None, self.npa
    
