#!/bin/env python
import argparse
import time
from time import sleep
import os
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# import pytesseract
import easyocr

import json
import sys
from datetime import datetime

def action(port, phone, distance = 15, right = True, berry = "g"):
    with open("phone-spec.json", 'r') as file:
        phones = json.load(file)
        
    print("Start testing on  \"{}\" on port {}", phone, port)
    p = TouchScreen(port, phone)
    reader = easyocr.Reader(['en'])
    t1 = datetime.now()
    for i in range(0, 10):
        # import easyocr
        # reader = easyocr.Reader(['en'])
        # jbuf = p.screen_capture_bw(100, 120, 200, 70)
        # jbuf = p.screen_capture_bw(550, 550, 230, 70)
        # jbuf = p.screen_capture_bw(10, 10, 980, 1980)
        jbuf = p.screen_capture_bw(10, 550, 980, 70)
        pixel_array = np.array(jbuf["gray"], dtype=np.uint8)
        pixel_array = pixel_array.reshape((jbuf["hight"], jbuf["width"]))
        image = Image.fromarray(pixel_array, mode='L')
        # print(image.tell())
        if True:
            # text = reader.readtext(pixel_array)
            text = p.read_text(550, 550, 230, 70)
            for t in text:
                print("Read with easyocr {}".format(t[1]))
        # print("Read with easyocr {}".format(text))
        if False:
            text = pytesseract.image_to_string(image)
            print("Read with tessertact {}".format(text))
        # _, image = p.read_text(290, 530, 400, 90)
    t2 = datetime.now()
    print("Elapsed time {}s".format((t2-t1).total_seconds()))
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.title(f'Grayscale Bitmap')
    plt.axis('off')
    plt.show()
    print("Is pokemon : {}".format(p.screen_is_catch_pokemon()))
    
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port, args.phone)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
