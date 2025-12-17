import re
import numpy as np
from PIL import Image
# import easyocr
import pytesseract
import cv2
from pytesseract import Output
from tesserocr import PyTessBaseAPI, RIL, iterate_level
import pandas as pd
import re

TESSDATA_PATH = '/usr/share/tesseract/tessdata/'

class Ocr:
    def __init__(self, ts):
        self.ts =ts
        self.api = PyTessBaseAPI(path=TESSDATA_PATH, lang='eng')
        # self.reader = easyocr.Reader(['en'])
        pass

    def __del__(self):
        pass

    def boxes_get(self, img, verbose=0):
        candidates = []
        H, W = img.shape
        edges = cv2.Canny(img, 50, 150)
        if verbose > 5:
            self.ts.sc.schow_image(edges, wait=1000)
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
            if 0.5 < aspect < 6: 
                candidates.append((x, y, w, h))
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
                    self.ts.sc.show_image(boxes[-1], wait=2000, title='box')
        return boxes

    def read_rec_line(self,
                       start,
                       size,
                       verbose=0,
                       np_array=None,
                       confidence=20.0,
                       scale=False
                       ):
        t, _ = self.read_rec_line(start=start, size=size, 
                                          verbose=verbose, np_array=np_array,
                                          confidence=confidence,
                                          scale=scale)
        return t[0]
    
    def read_rec_lines(self,
                       start,
                       size,
                       verbose=0,
                       np_array=None,
                       confidence=20.0,
                       scale=False
                       ):
        t, np_array = self.read_rec_and_np_array(start=start, size=size, 
                                          verbose=verbose, np_array=np_array,
                                          confidence=confidence,
                                          scale=scale)
        rt = []
        last_word=1000000
        for w in t:
            if w['word'] <=  last_word:
                rt.append(w)
            else:
                rt[-1]['text'] = f"{rt[-1]['text']} {w['text']}"
            last_word = w['word']
        return rt, np_array

    def read_rec(self, 
                 start=(0, 0), 
                 size=None, 
                 scale=False):
        text,_ = self.read_rec_and_np_array(start,size,scale)
        # text,_ = self.pocr_read_and_image(start,size,scale)
        return text
        
    def read_rec_and_np_array(self, 
                              start=(0, 0), 
                              size=None, 
                              verbose=0,
                              np_array=None,
                              confidence=20.0,
                              scale=False
                              ):
        if verbose > 0:
            pd.set_option('display.max_rows', None)     # Show all rows
            pd.set_option('display.max_columns', None)  # Show all columns
            pd.set_option('display.width', None)        # Use full width of the terminal/notebook
            pd.set_option('display.max_colwidth', None) # Show all text within each column (don't truncate long strings)

        if not np_array:
            if size == None:
                size = (self.ts.specs ['w'], self.ts.specs['h'])
            jbuf = self.ts.screen_capture_bw(start, size, scale)
            np_array = np.array(jbuf["gray"], dtype=np.uint8)
            np_array = np_array.reshape((jbuf["height"], jbuf["width"]))
        return self._tesserocr_from_array(np_array, confidence=confidence, verbose=verbose)
        
        # return self.tesseract_from_array(np_array, confidence=confidence, verbose=verbose, show=False)

    def _tesserocr_from_array(self, array, confidence=20.0, verbose=0):
        """Run tesserocr on a numpy array and return extracted words plus the PIL image.

        Returns (ocr_data, image)
        """
        h, w = array.shape
        self.api.SetImageBytes(
                array.tobytes(),
                w, h,
                1,      # bytes per pixel (grayscale)
                w       # bytes per line
        )        
        # trigger recognition (GetUTF8Text returns full text, iterator used below)
        t = self.api.GetUTF8Text()
        ri = self.api.GetIterator()

        level = RIL.WORD
        ocr_data = []
        wi = 1
        for r in iterate_level(ri, level):
            if verbose > 0:
                print(dir(r))
            try:
                text = r.GetUTF8Text(level)
            except:
                continue
            conf = r.Confidence(level)
            left, top, right, bottom = r.BoundingBox(level)
            width = right - left
            height = bottom - top
            if conf > confidence:
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
    
    def find_regex(self,
                   regex,
                   start=(0,0),
                   size=None,    
                   verbose=0,
                   np_array=None,
                   confidence=20.0,
                   scale=False):
        if np_array == None:
            if size == None:
                size = (self.ts.specs ['w'], self.ts.specs['h'])
            lines, np_array = self.read_rec_and_np_array(start=start, size=size, 
                                     verbose=verbose, np_array=np_array,
                                     confidence=confidence,
                                     scale=scale)
        for l in lines:
            if re.search(regex, l['text']):
                return l, np_array
        return None, np_array
    
    def find_button(self,
                   name,
                   start=(0,0),
                   size=None,    
                   verbose=0,
                   npa=None,
                   confidence=20.0,
                   scale=False):
        if npa == None:
            if size == None:
                size = (self.ts.specs ['w'], self.ts.specs['h'])
            npa = self.ts.sc.scan_image(x=start[0], y=start[1], w=size[0], h=size[1], channel='gray')

        boxes = self.boxes_get(npa, verbose=0)            

        for box in boxes:
            if verbose > 5:
                self.ts.sc.show_image(box['rois'], wait=1000, title='button-candidate')
            t, _ = self._tesserocr_from_array(box['rois'])

            for w in t:
                print("Found word: {}".format(w['text']))
                if re.search(name, w['text']):
                    w['left'] += box['x'] + w['left']
                    w['top']  += box['y'] + w['top']
                    w['center'] = (w['center'][0] + box['x'], w['center'][1] + box['y'])                  
                    return w, npa

            roi = cv2.normalize(box['rois'], None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
            roi = cv2.bitwise_not(roi)
            roi = cv2.adaptiveThreshold(
                roi,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31,
                5
            )
            if verbose > 5:
                self.ts.sc.show_image(roi, wait=1000, title='button-candidate-preprocessed')
            words, _ = self._tesserocr_from_array(roi)
            texts = self._concat_tesserocr_results(words)
            for w in texts:
                print("Found word: {}".format(w['text']))
                if re.search(f'.*{name}.*', w['text']):
                    w['left'] += box['x'] + w['left']
                    w['top']  += box['y'] + w['top']
                    w['center'] = (w['center'][0] + box['x'], w['center'][1] + box['y'])                  
                    return w, npa   

        return None, npa