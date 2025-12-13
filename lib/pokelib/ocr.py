import re
import numpy as np
from PIL import Image
# import easyocr
import pytesseract
from pytesseract import Output
from tesserocr import PyTessBaseAPI, RIL, iterate_level
import pandas as pd

TESSDATA_PATH = '/usr/share/tesseract/tessdata/'

class Ocr:
    def __init__(self, ts):
        self.ts =ts
        self.api = PyTessBaseAPI(path=TESSDATA_PATH, lang='eng')
        # self.reader = easyocr.Reader(['en'])
        pass

    # def easyocr_read(self, start, size, scale=True):
    #     jbuf = self.ts.screen_capture_bw(start,size, scale)
    #     np_a = np.array(jbuf["gray"], dtype=np.uint8)
    #     np_a = np_a.reshape((jbuf["height"], jbuf["width"]))                       
    #     # image = Image.fromarray(pixel_array, mode='L')
    #     t = self.reader.readtext(np_a)
    #     return t
    #
    # def easyocr_read_center(self, start, size, scale=True):
    #     results = self.easyocr_read(start, size, scale)
    #     output = []
    #     for box, text, conf in results:
    #         # box is a list of 4 points: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    #         xs = [p[0] for p in box]
    #         ys = [p[1] for p in box]
    #         cx = sum(xs) / 4.0
    #         cy = sum(ys) / 4.0
    #         output.append({
    #             "text": text,
    #             "center": (int(cx), int(cy)),
    #             "confidence": conf
    #         })
    #     return output
    #
    # def easyocr_read_text(self, start, size, scale=True):
    #     rt = []
    #     for t in self.easyocr_read(start, size, scale=True):
    #         rt.append(t[1])
    #     return rt
    #
    # def easyocr_read_and_image(self, start, size, scale=True):
    #     jbuf = self.screen_capture_bw(start,size, scale)
    #     np_a = np.array(jbuf["gray"], dtype=np.uint8)
    #     np_a = np_a.reshape((jbuf["height"], jbuf["width"]))                       
    #     # image = Image.fromarray(pixel_array, mode='L')
    #     text = self.reader.readtext(np_a)
    #     rt = []
    #     for t in text:
    #         rt.append(t[1])
    #     return rt, Image.fromarray(np_a, mode='L')
    #
    
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

    def read_rec(self, start, size, scale=False):
        text,_ = self.read_rec_and_np_array(start,size,scale)
        # text,_ = self.pocr_read_and_image(start,size,scale)
        return text
        
    def read_rec_and_np_array(self, 
                              start, 
                              size, 
                              verbose=0,
                              np_array=None,
                              confidence=20.0,
                              scale=False, 
                              ):
        if verbose > 0:
            pd.set_option('display.max_rows', None)     # Show all rows
            pd.set_option('display.max_columns', None)  # Show all columns
            pd.set_option('display.width', None)        # Use full width of the terminal/notebook
            pd.set_option('display.max_colwidth', None) # Show all text within each column (don't truncate long strings)

        if not np_array:
            jbuf = self.ts.screen_capture_bw(start, size, scale)
            np_array = np.array(jbuf["gray"], dtype=np.uint8)
            np_array = np_array.reshape((jbuf["height"], jbuf["width"]))
        if verbose < 0:
            ocr_data = self.read_with_api(np_array, mode='L')
            image = Image.fromarray(np_array, mode='L')
    
            self.api.SetImage(image)
            df = self.api.GetUTF8Text()
            # Get the iterator object
            # ri stands for ResultIterator
            ri = self.api.GetIterator() 
        
            # Define the level you want to iterate over (WORD is level 5)
            level = RIL.WORD
            
            # --- 2. Iterate and Extract Data ---
            # iterate_level is a helper function that handles the iteration logic
            ocr_data = []
            wi = 1
            for r in iterate_level(ri, level):
                
                # Get the text string for the current level (word)
                text = r.GetUTF8Text(level)
                
                # Get the confidence score (0-100)
                conf = r.Confidence(level)
                
                # Get the bounding box coordinates (left, top, right, bottom)
                # Note: tesserocr returns (left, top, right, bottom), not (x, y, w, h)
                left, top, right, bottom = r.BoundingBox(level)
                
                # Calculate width and height (required to match pytesseract output format)
                width = right - left
                height = bottom - top
                # word_index = r.GetElementIndex(level)
                # Append the data to the list
                ocr_data.append({
                    'text': text,
                    'conf': conf,
                    'left': left,
                    'top': top,
                    'width': width,
                    'height': height,
                    'word': wi,
                    'center': (left + width//2, top + height//2)
                })        
                if len(text) > 1:
                    wi += 1
                else:
                    wi = 1
                
                
            return ocr_data, image
        
        else:
            # text = pytesseract.image_to_string(np_a)
            df = pytesseract.image_to_data(np_array, output_type=Output.DATAFRAME)
            # text = "ddsf"
            if verbose > 0:
                print(f"Reader {df}")
            rt = []
            wc = 0
            for index, row in df.iterrows():
                # Example 1: Accessing columns by name
                text = row['text']
                c = row['conf']
        
                # Example 2: Accessing the bounding box coordinates
                x = row['left']
                y = row['top']
                w = row['width']
                h = row['height']
                c = row['conf']
                if text and c > confidence: # Check if the text is not None/empty
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
            #for t in text.split("\n"):
            #     rt.append(t)
            # print(rt)
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
            lines = self.read_rec_lines(start=start, size=size, 
                                     verbose=verbose, np_array=np_array,
                                     confidence=confidence,
                                     scale=scale)
        for l in lines:
            if re.search(regex, l['text']):
                return l, np_array
        return None, np_array