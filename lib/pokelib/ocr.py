import numpy as np
from PIL import Image
import easyocr
import pytesseract
class Ocr:
    def __init__(self, ts):
        self.ts =ts
        self.reader = easyocr.Reader(['en'])
        pass

    def easyocr_read(self, start, size, scale=True):
        jbuf = self.ts.screen_capture_bw(start,size, scale)
        np_a = np.array(jbuf["gray"], dtype=np.uint8)
        np_a = np_a.reshape((jbuf["height"], jbuf["width"]))                       
        # image = Image.fromarray(pixel_array, mode='L')
        t = self.reader.readtext(np_a)
        return t

    def easyocr_read_text(self, start, size, scale=True):
        rt = []
        for t in self.easyocr_read(start, size, scale=True):
            rt.append(t[1])
        return rt

    def easyocr_read_and_image(self, start, size, scale=True):
        jbuf = self.screen_capture_bw(start,size, scale)
        np_a = np.array(jbuf["gray"], dtype=np.uint8)
        np_a = np_a.reshape((jbuf["height"], jbuf["width"]))                       
        # image = Image.fromarray(pixel_array, mode='L')
        text = self.reader.readtext(np_a)
        rt = []
        for t in text:
            rt.append(t[1])
        return rt, Image.fromarray(np_a, mode='L')

    def read_text(self,start,size, scale=True):
        t,_ = self.pocr_read(start, size)
        return t

    def pocr_read(self, start, size, scale=True):
        text,_ = self.pocr_read_and_image(start,size,scale)
        # text,_ = self.pocr_read_and_image(start,size,scale)
        return text
        
    def pocr_read_and_image(self, start, size, scale=True):
        jbuf = self.ts.screen_capture_bw(start, size, scale)
        np_a = np.array(jbuf["gray"], dtype=np.uint8)
        np_a = np_a.reshape((jbuf["height"], jbuf["width"]))                       
        image = Image.fromarray(np_a, mode='L')
        text = pytesseract.image_to_string(np_a)
        # text = "ddsf"
        # print(f"Reader {text}")
        rt = []
        for t in text.split("\n"):
            rt.append(t)
        # print(rt)
        return rt, image
