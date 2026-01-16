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
from .screen_capture import ScreenCapture

TESSDATA_PATH = '/usr/share/tesseract/tessdata/'

class Ocr:
    def __init__(self, ts):
        self.ts = ts
        self.sc = ts.sc
        self.api = PyTessBaseAPI(path=TESSDATA_PATH, lang='eng')
        self.capture = ScreenCapture(ts)
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

    def _boxes_get(self, img, verbose=0):
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
    
    def _process_array(self, npa, verbose=0):
        if self.invert:
            npa = cv2.bitwise_not(npa)
        npa = cv2.normalize(npa, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        if self.process:
            npa = cv2.adaptiveThreshold(
                npa,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31,
                5
            )
        return npa
 
    def _tesserocr_from_array(self, array, verbose=0):
        """Run tesserocr on a numpy array and return extracted words plus the PIL image.

        Returns (ocr_data, image)
        """


        if verbose > 5:
            self.ts.sc.show_image(array, wait=2000, title='button-candidate-preprocessed')
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



    def tesseract_from_array(self, np_array, confidence=20.0, verbose=0):
        """Run pytesseract on a numpy array and return extracted words plus the array.

        Returns (rt, np_array) where `rt` is a list of word dicts with keys
        `text`, `center`, `h`, `w`, `confidence`, `word`.
        """
        # text = pytesseract.image_to_string(np_a)
        df = pytesseract.image_to_data(np_array, output_type=Output.DATAFRAME)
        if verbose > 0:
            print(f"Reader {df}")
        rt = []
        wc = 0
        for index, row in df.iterrows():
            text = row['text']
            # bounding box and confidence
            x = row['left']
            y = row['top']
            w = row['width']
            h = row['height']
            c = row['conf']
            if text and c > confidence:  # Check if the text is not None/empty
                wc += 1
                rt.append({
                    "text": text,
                    "center": (x + w//2, y + h//2),
                    "h": h,
                    "w": w,
                    "confidence": c,
                    "word": row['word_num']
                })
                if verbose > 0:
                    print(f"Index: {index}, Word: {text}, Confidence: {c}")

        if verbose > 0:
            print(f"Total words {wc}")
        return rt, np_array
    
    def read_and_npa(self, npa=None,verbose=0):
        if npa == None:
            npa = self.capture.scan_region(xs=self.startx, ys=self.starty, xe=self.endx, ye=self.endy, channel=self.color)
        self.npa = npa
        if self.process:
            npa = self._process_array(npa, verbose=verbose)
        t, _ = self._tesserocr_from_array(npa, verbose=verbose)
        self.reset_parameters() 
        return t, self.npa, npa

    def read(self, *args, **kwargs):
        text, self.npa, processed_npa = self.read_and_npa(*args, **kwargs)
        return text


    def regex(self, regex, npa=None, verbose=0):
        lines, self.npa = self.read(npa, verbose=verbose)
        self.reset_parameters()
        for l in lines:
            if re.search(regex, l['text']):
                return l, self.npa

        return None, self.npa
    
    def button(self, name, npa=None, verbose=0):
        if npa == None:
            npa = self.capture.scan_region(xs=self.startx, ys=self.starty, xe=self.endx, ye=self.endy, channel=self.color)
        self.npa = npa
    
        boxes = self._boxes_get(npa, verbose=verbose)            

        for box in boxes:
            roi = self._process_array(box['rois'], verbose=verbose)
            if verbose > 5:
                self.ts.sc.show_image(roi, wait=1000, title='button-candidate-preprocessed')
            words, _ = self._tesserocr_from_array(roi)
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