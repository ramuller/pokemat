import re
import numpy as np
from PIL import Image
# import easyocr
import pytesseract
import cv2
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
        return self._tesserocr_from_array(np_array, start, size, confidence=confidence, verbose=verbose)
        
        # return self.tesseract_from_array(np_array, confidence=confidence, verbose=verbose, show=False)

    def _tesserocr_from_array(self, np_array, start, size, mode='L', confidence=20.0, verbose=0):
        """Run tesserocr on a numpy array and return extracted words plus the PIL image.

        Returns (ocr_data, image)
        """

        # roi = cv2.normalize(np_array, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        roi = cv2.normalize(np_array, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        roi = cv2.adaptiveThreshold(
                                    roi,
                                    255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY,
                                    31, 5)

        image = Image.fromarray(roi, mode=mode)
        if verbose > 0:      
            cv2.imshow("Image", roi)
            print("Press any key to continue...")
            cv2.waitKey(0)  
            cv2.destroyAllWindows()
        self.api.SetImage(image)
        # trigger recognition (GetUTF8Text returns full text, iterator used below)
        _ = self.api.GetUTF8Text()
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
                    'center': ((left + width//2) + start[0], (top + height//2) + start[1])
                })
                if len(text) > 1:
                    wi += 1
                else:
                    wi = 1

        return ocr_data, np_array

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