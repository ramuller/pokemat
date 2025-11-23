#!/bin/env python
import argparse
import time
from time import sleep
import os
import sys
import logging
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
# from icon_detector import IconDetector
from hybrid_icon_detector import IconDetector

# import pytesseract
# import easyocr

import json
import sys
from datetime import datetime

import cv2
import numpy as np

#
#  From chatgpt
def nms_boxes(boxes, scores, iou_thr=0.3):
    idxs = np.argsort(scores)[::-1]
    keep = []
    while len(idxs) > 0:
        i = idxs[0]
        keep.append(i)
        x1, y1, x2, y2 = boxes[i]
        xx1 = np.maximum(x1, np.array([boxes[j][0] for j in idxs[1:]]))
        yy1 = np.maximum(y1, np.array([boxes[j][1] for j in idxs[1:]]))
        xx2 = np.minimum(x2, np.array([boxes[j][2] for j in idxs[1:]]))
        yy2 = np.minimum(y2, np.array([boxes[j][3] for j in idxs[1:]]))
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        inter = w * h
        area_i = (x2 - x1) * (y2 - y1)
        area_j = (np.array([boxes[j][2] for j in idxs[1:]]) - np.array([boxes[j][0] for j in idxs[1:]])) * \
                 (np.array([boxes[j][3] for j in idxs[1:]]) - np.array([boxes[j][1] for j in idxs[1:]]))
        iou = inter / (area_i + area_j - inter + 1e-9)
        idxs = idxs[1:][iou < iou_thr]
    return [boxes[i] for i in keep], [scores[i] for i in keep]

def detect_template_multiscale(scene_gray, tmpl_gray,
                               scales=np.linspace(0.6, 1.6, 21),
                               rotations=(0,),   # add e.g. (-15, 15) if rotation varies
                               thr=0.88,         # tighten/loosen as needed
                               max_candidates=50):
    scene = scene_gray if scene_gray.ndim == 2 else cv2.cvtColor(scene_gray, cv2.COLOR_BGR2GRAY)
    tmpl0 = tmpl_gray

    boxes, scores = [], []
    for ang in rotations:
        print(f"rotation{ang}")
        if ang != 0:
            # rotate around center without cropping
            h, w = tmpl0.shape
            M = cv2.getRotationMatrix2D((w/2, h/2), ang, 1.0)
            cos, sin = abs(M[0,0]), abs(M[0,1])
            nW, nH = int((h*sin) + (w*cos)), int((h*cos) + (w*sin))
            M[0,2] += (nW/2) - w/2
            M[1,2] += (nH/2) - h/2
            tmpl_rot = cv2.warpAffine(tmpl0, M, (nW, nH), flags=cv2.INTER_LINEAR, borderValue=0)
        else:
            tmpl_rot = tmpl0

        for s in scales:
            t = cv2.resize(tmpl_rot, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
            th, tw = t.shape[:2]
            if th < 8 or tw < 8 or th >= scene.shape[0] or tw >= scene.shape[1]:
                continue

            res = cv2.matchTemplate(scene, t, cv2.TM_CCOEFF_NORMED)
            # collect high responses
            loc = np.where(res >= thr)
            for (y, x) in zip(*loc):
                boxes.append((x, y, x+tw, y+th))
                scores.append(float(res[y, x]))
                if len(scores) >= max_candidates:
                    break
            if len(scores) >= max_candidates:
                break

    if not boxes:
        return []

    # non-maximum suppression to keep only best, non-overlapping boxes
    boxes_nms, scores_nms = nms_boxes(boxes, scores, iou_thr=0.3)
    return list(zip(scores_nms, boxes_nms))
#
#  From chatgpt end

def yuv420_to_rgb(yuv_bytes: bytes, width: int, height: int):
    # YUV420p (I420) has height * 1.5 rows
    yuv = np.frombuffer(yuv_bytes, dtype=np.uint8).reshape((height * 3 // 2, width))

    # Convert to BGR (I420 = YUV420p: Y plane, then U, then V)
    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

    # Convert BGR → RGB if you prefer RGB
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb




def yuv420_dict_to_rgb(jbuf):
    w = jbuf["width"]
    h = jbuf["height"]  # use your real key here

    # Y plane (full resolution)
    Y = np.array(jbuf["gray"], dtype=np.uint8).reshape(h, w)

    # U, V planes (subsampled by 2 in both directions)
    U = np.array(jbuf["u"], dtype=np.uint8).reshape(h // 2, w // 2)
    V = np.array(jbuf["v"], dtype=np.uint8).reshape(h // 2, w // 2)

    # Upsample U and V to match Y
    U_full = cv2.resize(U, (w, h), interpolation=cv2.INTER_NEAREST).astype(np.float32)
    V_full = cv2.resize(V, (w, h), interpolation=cv2.INTER_NEAREST).astype(np.float32)
    Y_f    = Y.astype(np.float32)

    # YUV (BT.601) to RGB
    # R = Y + 1.402 * (V-128)
    # G = Y - 0.344136*(U-128) - 0.714136*(V-128)
    # B = Y + 1.772 * (U-128)
    d = U_full - 128.0
    e = V_full - 128.0

    R = Y_f + 1.402    * e
    G = Y_f - 0.344136 * d - 0.714136 * e
    B = Y_f + 1.772    * d

    # Clip and stack
    R = np.clip(R, 0, 255).astype(np.uint8)
    G = np.clip(G, 0, 255).astype(np.uint8)
    B = np.clip(B, 0, 255).astype(np.uint8)

    # Make RGB image (H, W, 3)
    rgb = np.stack([R, G, B], axis=-1)
    return rgb

def scan_image(x, y, w, h, channel="gray"):
    if channel == "gray":
        jbuf = p.screen_capture_bw((x, y), (w, h), scale=False)
        pixel_array = np.array(jbuf["gray"], dtype=np.uint8).reshape((jbuf["height"], jbuf["width"]))
    else:
        jbuf = p.screen_capture((x, y), (w, h), scale=False)
        rgb = yuv420_dict_to_rgb(jbuf)
   
        if channel == "red":
            pixel_array = np.array(rgb[:, :, 0], dtype=np.uint8).reshape(h, w)
    return pixel_array
    return Image.fromarray(pixel_array, mode='L')

def use_template_only(scene, icon):
    t1 = datetime.now()
    for i in range(0,1):
        matches = detect_template_multiscale(scene, icon,
                                     scales=np.linspace(0.5, 1.4, 15),
                                     rotations=(0,),   # add (-10, 10) if needed
                                     thr=0.90)
    t2 = datetime.now()
    print("Templ : Elapsed time {}s".format((t2-t1).total_seconds()))

    for score, (x1, y1, x2, y2) in matches:
        print(f"score={score:.3f} box=({x1},{y1},{x2},{y2})")
        # cv2.rectangle(scene, (x1,y1), (x2,y2), 255, 1)
   

def scan_center_image(x, y, w, h, channel="bw"):
    return scan_image(x - (w/2), y - h/2, w, h, channel)

from cv_motion import MotionDetectorRA
def motion(port):
    det = MotionDetectorRA(alpha=0.05, thresh=25, min_area=500)

    print("Start motion port {}",port)
    global p
    p = TouchScreen(port)
    while True:
        frame = scan_image(0, 0, p.specs['w'], p.specs['h'])
        mask, boxes = det.update(frame)
        # do something with mask / boxes
        # Example: draw boxes (if frame is color; for gray, convert to BGR first)
        vis = frame if frame.ndim == 3 else cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        for (x,y,w,h) in boxes:
            cv2.rectangle(vis, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.imshow("mask", mask); cv2.imshow("vis", vis); cv2.waitKey(1)
    
    

def action(port, arg = None):
        
    print("Start testing port {}",port)
    global p
    p = TouchScreen(port)
    t1 = datetime.now()
    
    print(f"specs {p.specs}")
    print(f"maxX {p.specs['width']}")
    
    
    n = "friend_order_arrow_down.png"
    n = "friend_order_arrow_up.png"
    # n = "pokemon_order_recent.png"
    n = "icon.png"
    icon =  cv2.imread(n, cv2.IMREAD_GRAYSCALE)
    print(f"ICON shape {icon.shape}")
    
    # jbuf = p.screen_capture_bw((0,0), (p.specs['width'], p.specs['height']), scale=False)
    # icon = scan_center_image(int(576/2), 943, 72,72)
    # Friend order
    # icon = scan_center_image(498, 948, 100,106)
    # Only arrow
    #icon = scan_center_image(540, 949, 38,38)
    # pokemon RECENT
    # icon = scan_center_image(500, 327, 38,38)
    # pokemon FAVORITE
    # icon = scan_center_image(500, 429, 38,38)
    # pokemon NUMBER
    # icon = scan_center_image(500, 531, 38,38)
    # pokemon HP
    # icon = scan_center_image(500, 633, 38,38)
    # pokemon az
    # icon = scan_center_image(500, 736, 38,38)
    # pokemon az
    # icon = scan_center_image(500, 838, 38,38)
    # Scan red R
    # icon = scan_center_image(299, 399, 48, 48, channel="red")
        
    
    
    
    # icon =  cv2.imread("friend_order_arrow_up.png", cv2.IMREAD_GRAYSCALE)
    # cv2.imwrite("icon.png", icon)
    
    # icon = cv2.imread("pokeball.png", cv2.IMREAD_GRAYSCALE)
    # icon = scan_center_image(int(p.specs['width']/2), 700, 72,72)
    # scene = scan_image(0, 0, p.specs['width'], p.specs['height'])
    ende = True
    while ende:
        scene = scan_image(0, 0, p.specs['w'], p.specs['h'])
        # scene = scan_image(p.specs['width'] - 150, p.specs['height'] - 150, 150, 100)
        cv2.imshow("result", scene)
        ende = False    

    print("icon:", icon.shape, icon.dtype, int(icon.min()), int(icon.max()))
    print("scene:", scene.shape, scene.dtype, int(scene.min()), int(scene.max()))

    # cv2.imshow("Screen", scene)
    # cv2.imshow("icon", icon)

    icons = {
        "icon": icon,
    }
    use_template_only(scene, icon)
    detector = IconDetector(icons)
    dets = detector.detect(scene)
    t1 = datetime.now()
    for i in range(0,1):
        # scene = scan_image(p.specs['width'] - 150, p.specs['height'] - 150, 150, 100)
        channel="red"
        scene = scan_image(0, 0, p.specs['w']-1, p.specs['h']-1, channel=channel)
        dets = detector.detect(scene)
    t2 = datetime.now()
    print("Hybrid : Elapsed time {}s".format((t2-t1).total_seconds()))
    print(f"Detected\n {dets}")
    for d in dets:
        print(f"score {d.score}")
        print(f"coord\n {d.quad}")
        cv2.rectangle(scene, (int(d.quad[0][0]),int(d.quad[0][1])), \
                      (int(d.quad[2][0]),int(d.quad[2][1])), 255, 2)
        
    
    h, w = scene.shape
    icon=cv2.resize(icon, (w, h))
    # cv2.imshow("scene", scene)
    cv2.imshow("result", cv2.hconcat([icon,scene]))
    cv2.waitKey(000)
    cv2.destroyAllWindows()    
    # plt.imshow(icon, cmap='gray', vmin=0, vmax=255)
    # plt.imshow(scene, cmap='gray', vmin=0, vmax=255)
    # plt.title(f'Grayscale Bitmap')
    # plt.axis('off')
    # plt.show()        
   
    
def main():

    parser = PokeArgs()
    global args
    args = parser.parse_args()
    
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    action(args.port)
    # motion(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
