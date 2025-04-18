import numpy as np
from PIL import Image
# import easyocr
import pytesseract
class Text:
    def __init__(self, ts):
        self.ts =ts
        # self.reader = easyocr.Reader(['en'])
        pass

    def easyocr_read_text(self, x, y, w, h):
        jbuf = self.ts.screen_capture_bw(x, y, w, h)
        np_a = np.array(jbuf["gray"], dtype=np.uint8)
        np_a = np_a.reshape((jbuf["hight"], jbuf["width"]))                       
        # image = Image.fromarray(pixel_array, mode='L')
        text = self.reader.readtext(np_a)
        rt = []
        for t in text:
            rt.append(t[1])
        return rt

    def easyocr_read_text_and_image(self, x, y, w, h):
        jbuf = self.screen_capture_bw(x, y, w, h)
        np_a = np.array(jbuf["gray"], dtype=np.uint8)
        np_a = np_a.reshape((jbuf["hight"], jbuf["width"]))                       
        # image = Image.fromarray(pixel_array, mode='L')
        text = self.reader.readtext(np_a)
        rt = []
        for t in text:
            rt.append(t[1])
        return rt, Image.fromarray(np_a, mode='L')

    def read_text(self, x, y, w, h):
        t,_ = self.read_text_and_image(x, y, w, h)
        return t

    def read_text_and_image(self, x, y, w, h):
        jbuf = self.ts.screen_capture_bw(x, y, w, h)
        np_a = np.array(jbuf["gray"], dtype=np.uint8)
        np_a = np_a.reshape((jbuf["hight"], jbuf["width"]))                       
        image = Image.fromarray(np_a, mode='L')
        text = pytesseract.image_to_string(np_a)
        # print(text)
        rt = []
        for t in text.split("\n"):
            rt.append(t)
        # print(rt)
        return rt, image
