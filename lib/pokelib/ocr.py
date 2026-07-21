from time import sleep
import traceback
import re
import os
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
from .structs import ScreenRegion


def _get_tessdata_path():
    """Find tessdata directory, supporting both Ubuntu and non-Ubuntu distros."""
    candidates = [
        '/usr/share/tesseract-ocr/5/tessdata/',  # Non-Ubuntu (ROM-based)
        '/usr/share/tesseract-ocr/tessdata/',    # Alternative non-Ubuntu path
        '/usr/share/tesseract/tessdata/',         # Ubuntu
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    # If none found, return first candidate (will fail with clear error)
    return candidates[0]

TESSDATA_PATH = _get_tessdata_path()

class Ocr:
    def __init__(self, ts):
        self.ts = ts
        self.api = PyTessBaseAPI(path=TESSDATA_PATH, lang='eng')
        self.image = PokeImage(ts)
        self.reset_parameters()

    def __del__(self):
        pass

    def reset_parameters(self):
        self.confidence = 20.0
        self.invert = False
        self.process = True
        self.color = 'gray'
        self.mode = 'word'

    def set_mode(self, mode):
        self.mode = mode
 
    def _tesserocr_from_array(self, reg : ScreenRegion, verbose=0):
        """Run tesserocr on a numpy array and return extracted words plus the PIL image.

        Returns (ocr_data, image)
        """


        if verbose > 5:
            self.ts.image.show_image(reg.npa, wait=4000, title='button-candidate-preprocessed')
        # trigger recognition (GetUTF8Text returns full text, iterator used below)
        # Only tesserocr after here
        # self.api.SetPageSegMode(PSM.SINGLE_WORD)
        try:
            h, w = reg.npa.shape
        except Exception as e:
            print("Call stack:")
            traceback.print_stack()   # prints current stack to stdout
            print(f'ERROR : ocr npa {e}')
            return []
        self.api.SetImageBytes(
                reg.npa.tobytes(),
                w, h,
                1,      # bytes per pixel (grayscale)
                w       # bytes per line
        )

        # with suppress_stderr():
        t = self.api.GetUTF8Text()
        ri = self.api.GetIterator()
        if reg.mode == 'line':
            level = RIL.TEXTLINE
        elif reg.mode == 'symbol':
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
                    'left': left + reg.xs,
                    'top': top + reg.ys,
                    'width': width,
                    'height': height,
                    'word': wi,
                    'center': ((left + width//2 + reg.xs), \
                               (top + height//2 + reg.ys))
                })
                if len(text) > 1:
                    wi += 1
                else:
                    wi = 1
        # print(f"Total OCR words: {ocr_data}")
        return ocr_data
    
    def _concat_tesserocr_results(self, words):
        """Concatenate tesserocr results based on word index."""
        concatenated = []
        for w in words:
            if w['word'] == 1:
                concatenated.append(w)
            else:
                concatenated[-1]['text'] += ' ' + w['text']
        return concatenated
    
    def read_and_npa(self, reg : ScreenRegion=None,
                     verbose=0):
        reg = reg or ScreenRegion(self.ts)
        if reg.npa is None:
            reg.npa = self.image.scan_region(reg)
        reg = self.image.process_array(reg, verbose=verbose)
        t = self._tesserocr_from_array(reg, verbose=verbose)
        return t, reg

    def read(self, *args, **kwargs):
        text, _ = self.read_and_npa(*args, **kwargs)
        return text

    '''

    '''
    def read_area_percent(self, reg : ScreenRegion=None,
                          invert=False, process=False, verbose=0):
        reg = reg or ScreenRegion(self.ts)
        reg.xs = int(self.ts.specs['max_x'] * xs/100.0)
        reg.xe = int(self.ts.specs['max_x'] * xe/100.0)
        reg.ys = int(self.ts.specs['max_y'] * ys/100.0)
        reg.ye = int(self.ts.specs['max_y'] * ye/100.0)
        self.invert = invert
        self.process = process
        return self.read(reg, verbose=verbose)

    def regex(self, regex, reg : ScreenRegion=None, 
              retries=1,
              pause=1,
              find_all=False,    # Find all matches
              retry_callback=None,
              verbose=0):
        if reg is None:
            reg = ScreenRegion(self.ts)
        res=[]
        for tries in range(retries, 0, -1):
            reg.npa = None
            lines, reg = self.read_and_npa(reg, verbose=verbose)
            # self.reset_parameters()
            # print(f'Tries {tries}')
            for l in lines:
                # print(f'Line {l["text"]}')
                if re.search(regex, l['text']):
                    res.append(l)
                    if not find_all:
                        return res[0]
            if tries <= 1 or res:
                return res
            if retry_callback:
                retry_callback()
            sleep(pause)
        return res
    
    
    
    def scan_vertical(self, bs, start_rel=1.0, end_rel=0.6, steps=20, window_factor=2, **kw):
        start = self.ts.rel_y(start_rel)
        end = self.ts.rel_y(end_rel)

        # step based on full height
        full_height = self.ts.rel_y(1)
        step = max(1, full_height // steps)

        # correct direction
        step = -step if start > end else step

        for y in range(start, end, step):
            ys = y + window_factor * step
            ye = y

            b = self.ts.buttons.text_only.search(bs, ys=ys, ye=ye, **kw)
            # print(f'Line : {b}')
            if b:
                return b

        return None
        
