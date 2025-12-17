#!/bin/env python
import argparse
import time
from time import sleep
import os
import sys
import logging
import math
import cv2
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from tesserocr import PyTessBaseAPI, RIL, iterate_level, PSM
# import easyocr

import json
import sys
from datetime import datetime
import pandas as pd

TESSDATA_PATH = '/usr/share/tesseract/tessdata/'

def dialogs_get(img):
    H, W = img.shape
    candidates = []
    edges = cv2.Canny(img, 50, 150)
    p.sc.show_image(edges, wait=1000)
    contours, _ = cv2.findContours(
        edges,
        # cv2.RETR_EXTERNAL,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
        )
        
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
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
    if not candidates:
        rois = None
    else:        
        rois = []
        for d in unique:
            x, y, w, h = d
            pad = 10  # pixels
            rois.append({'rois': img[
                y+pad : y+h-pad,
                x+pad : x+w-pad
                ],
                'x': x+pad, 'y': y+pad
                })
            #p.sc.show_image(rois[-1], wait=2000, title='dialog')
      
    return rois


def action(port, arg = None):
        
    print("Start testing port {}",port)
    global p
    rounds = 1
    p = TouchScreen(port)

    t1 = datetime.now()
    
    # img = p.sc.scan_image(size=(p.specs['w'], p.specs['h'] // 2))
    # img = img ** 2
    x = 0
    y = 0
    h = 0
    w = 0
    img = p.sc.scan_image(x=x, y=y, h=h, w=w)
    ir = p.sc.scan_image(x=x, y=y, h=h, w=w, channel="red")    
    ig = p.sc.scan_image(x=x, y=y, h=h, w=w, channel="green")
    ib = p.sc.scan_image(x=x, y=y, h=h, w=w, channel="blue")
    if True:
            pd.set_option('display.max_rows', None)     # Show all rows
            pd.set_option('display.max_columns', None)  # Show all columns
            pd.set_option('display.width', None)        # Use full width of the terminal/notebook
            pd.set_option('display.max_colwidth', None) # Show all text within each column (don't truncate long strings)

    roi = img
    
    rois = dialogs_get(roi)

    for roi in rois:
        # roi = dialogs_get(roi)
        factor=1.0
        roi = cv2.resize(roi, None, None, interpolation=cv2.INTER_CUBIC, fx=factor, fy=factor)
        # roi = 255 - cv2.normalize(roi, None, alpha=-00, beta=255, norm_type=cv2.NORM_MINMAX)
        roi = cv2.normalize(roi, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        # roi = cv2.GaussianBlur(roi, (3,3), 0)
        p.sc.show_image(roi, wait=1000, title='normalized')

        ocr_data = read_roi(roi)
        print(ocr_data)

        roi = cv2.bitwise_not(roi)

        p.sc.show_image(roi, wait=1000, title='inverted')
        ocr_data = read_roi(roi)
        print(ocr_data)
        roi = cv2.adaptiveThreshold(
            roi,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            5
        )
        p.sc.show_image(roi, wait=000, title='preprocessed')
        # cv2.imwrite("/tmp/debug_preprocessed.png", roi
        
        ocr_data = read_roi(roi)
        print(ocr_data)
        
   
    p.sc.show_image(roi)
    # p.sc.show_image(ir)
    # p.sc.show_image(ig)
    # p.sc.show_image(ib)
    
    
    t2 = datetime.now()
    print("Elapsed time {}s".format((t2-t1).total_seconds()))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def read_roi(roi):
    # roi = np.ascontiguousarray(roi, dtype=np.uint8)
    h, w = roi.shape
    print(f'OCR ROI w:{w}, h:{h}')
    with PyTessBaseAPI(
        path=TESSDATA_PATH,
        lang="eng"
        #,
        # psm=PSM.SPARSE_TEXT
    ) as api:
        api.SetVariable("load_system_dawg", "0")
        api.SetVariable("load_freq_dawg", "0")
        # api.SetVariable("tessedit_char_whitelist", "OK")
  
    
        api.SetImageBytes(
            roi.tobytes(),
            w, h,
            1,      # bytes per pixel (grayscale)
            w       # bytes per line
        )
        t = api.GetUTF8Text()
        ri = api.GetIterator()
        print(t)

        level = RIL.WORD
        ocr_data = []
        wi = 1
        for r in iterate_level(ri, level):
            try:
                text = r.GetUTF8Text(level)
            except:
                continue
            conf = r.Confidence(level)
            left, top, right, bottom = r.BoundingBox(level)
            width = right - left
            height = bottom - top
            if conf > 10:
                ocr_data.append({
                    'text': text
                    })
                    
    return ocr_data
    
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
