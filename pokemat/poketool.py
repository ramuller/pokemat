#!/bin/env python
import math
import keyboard

from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
from pokelib.buttons import ButtonParameter
from pokelib import ScreenRegion
from pokelib import TextOnly, Coordinates,ButtonParameter 
from pokelib import IconButton, TextButton, StdButtons

from hybrid_icon_detector import IconDetector

import logging

import json
import sys
import re
from datetime import datetime
from time import sleep

import numpy as np


def _int(x, d='y'):
    if d == 'x':
        max = phone.specs['max_x'] 
    else:
        max = phone.specs['max_y'] 
    print(f'Value to convert {x}')
    if re.match(r'^\d+%$', x):
        return math.floor((int(x[:-1]) * max) / 100)
    elif re.match(r'^\d+$', x):
        return int(x)
    else:
        print(f'Unknown format {x} only abs and % supported')
        sys.exit(1)

def _set_paramters_from_args():
    reg = ScreenRegion(phone)

    if args.xs != 0:
        reg.xs = _int(args.xs, d='x')
    if args.xe == 0:
        reg.xe = phone.specs['max_x']
    else:    
        reg.xe = _int(args.xe, d='x')

    if args.ys != 0:
        reg.ys = _int(args.ys, d='y')
    if args.ye == 0:
        reg.ye = phone.specs['max_y']
    else:    
        reg.ye = _int(args.ye)

    reg.tl = args.tl
    reg.threshold = args.threshold
    reg.color = args.color
    reg.invert = args.invert
    reg.process = args.process
    reg.mode = args.mode
    return reg

def _post_process(reg):
    if args.show:
        phone.image.show_image(reg.npa, wait=10000, title='Read region')
    if args.save:
        path = f'{phone.config_path}/icons/screen-shots/{args.save}'
        if not re.match(r'.*\.png$', path):
            path += '.png'
        phone.image.save_image(reg.npa, path)
        print(f'Saved image to {path}')

def find_rgb():
    reg = ScreenRegion(phone, color='rgb', ye=phone.rel_y(0.5))
    bw_reg = ScreenRegion(phone, color='rgb', ye=phone.rel_y(0.5))
    reg.npa = phone.image.scan_region(reg)
    for r in range(250, 100, -20):
        g = r * 87 // 180
        b = r * 73 // 180
        vf  = f'r{r}-g{g}-b{b}'
        print(vf)
        bw_reg.npa = phone.image.find_rgb(reg, r, g, b, wait=1, verbose=10)
        det = phone.buttons.i_grunt_r.search(cust_reg=bw_reg, retries=1)
        print(det)
        if args.name:
            fn = f'{phone.config_path}/icons/screen-shots/{args.name}-{vf}.png'
            print(f'Save {fn }')
            phone.image.save_image(bw_reg.npa, fn)
    lines, reg = phone.ocr.read_and_npa(reg, mode='line')
    print(lines)    


def _schow_screen(reg):
    reg.npa = phone.image.scan_region(reg)
    phone.image.show_image(reg.npa, wait=int(args.show_time), title='Screen shoot')
    return phone.image.show_image(reg.npa, wait=int(args.show_time), title='Screen shoot')

def read():
    reg = _set_paramters_from_args()

    print(f'Reading region x:{reg.xs}-{reg.xe} y:{reg.ys}-{reg.ye}')
    print(f'reg.invert:{phone.ocr.invert} reg.process:{phone.ocr.process} reg.mode:{phone.ocr.mode}') 

    startTime = datetime.now()
    text, reg = phone.ocr.read_and_npa(reg)
    endTime = datetime.now()
    print(f'Time to find button: {(endTime - startTime).total_seconds()}')

    _post_process(reg)
    for t in text:
        print(t)
    return

def snapshot ():

    reg = ScreenRegion(phone, color=args.color)
    print("Press 'q' to not save anything")
    k = _schow_screen(reg)
    print(f"Got key {str(k)}")
    if k == 113:
        return
    for i in range(int(args.count)):
        fn = f'{phone.config_path}/icons/screen-shots/{args.name}-{i}.png'
        print(f'Save {fn }')
        reg.npa = phone.image.scan_region(reg)
        phone.image.save_image(reg.npa, fn)
        sleep(float(args.delay))

def ball ():

    print("Check for ball")
    for i in range(200):
        print(f'checkball = {phone.buttons.i_catch_ball.search()}')
        sleep(0.2)

def icon():
    if not  args.name:
        print('Button command needs --name argument')
        return
    reg = _set_paramters_from_args()
    
    print(f'Reading region x:{reg.xs}-{reg.xe} y:{reg.ys}-{reg.ye}')
    print(f'Search icon in region x:{phone.ocr.startx}-{phone.ocr.endx} y:{phone.ocr.starty}-{phone.ocr.endy}')
    print(f'invert:{phone.ocr.invert} process:{phone.ocr.process} mode:{phone.ocr.mode} text:{args.text} kind:{args.kind} press:{args.press}')

    button()
    icon_button = getattr(phone.buttons, args.name)

    detection = icon_button.search(retries=1)


    
def screen():

    print(f'Current screen is "{phone.screen.get_current_screen(verbose=args.verbose)}"')
    if args.save:
        path = f'{phone.config_path}/icons/screens-shots/{args.save}'
        if not re.match(r'.*\.png$', path):
            path += '.png'
        print(f'Saving screen to {path}')
        npa = phone.image.scan_region(xs=0, ys=0, xe=0, ye=0, channel="gray")
        if args.show:
            phone.image.show_image(npa, wait=args.show, title='Screen shoot')
        phone.image.save_image(npa, path)

def home():
    print(f'Current screen is "{phone.screen.get_current_screen(verbose=args.verbose)}"')
    print(f'Try to go home screen')
    phone.screen_go_to_home()
    print(f'Current screen is "{phone.screen.get_current_screen(verbose=args.verbose)}"')
    
'''
Search high level button
'''
def button():
    if not  args.name:
        print('Raw button command needs --name argument')
        print('Available buttons not all a really buttons!:')
        for b in dir(phone.buttons):
            if b.startswith('i_') \
                or b.startswith('b_'): # and callable(getattr(phone.buttons, b)):
                print(f'Button name : {b}')
        return
    print(f'Search button function {args.name}')
    reg = _set_paramters_from_args()
    method = getattr(phone.buttons, args.name)
    method.reg = reg
    method = getattr(phone.buttons, args.name)
    rep = args.count
    for i in range(rep):
        detection = method.search(
                                retries=1, 
                                verbose=args.verbose)
        if not method.updated and detection:
            print('Update button search area based on result')
            try:
                method.update_area(detection)
            except:
                pass
    print(f'Button found:')
    print(detection)

    reg = ScreenRegion(phone,
                             xs=method.reg.xs, xe=method.reg.xe,
                             ys=method.reg.ys, ye=method.reg.ye,
                             )
    
    if args.show:
        _schow_screen(reg)
    return

'''
Directly using the button functions
'''
def raw_button():
    print("Command : raw-button")
    if not  args.text:
        print('Raw button command needs --text argument')
        return
    reg = _set_paramters_from_args()
    
    print(f'Reading region x:{reg.xs}-{reg.xe} y:{reg.ys}-{reg.ye}')
    print(f'invert:{reg.invert} process:{reg.process} mode:{reg.mode} text:{args.text} kind:{args.kind} press:{args.press}')

    sb = StdButtons(reg)
    if args.kind == 'dark':
        # b = phone.buttons.dark
        b = sb.dark
    elif args.kind == 'white':
        b = phone.buttons.white
    elif args.kind == 'black_on_white' \
         or args.kind == 'bw':
        b = phone.buttons.black_on_white
    elif args.kind == 'white_on_black'\
         or args.kind == 'wb':
        b = phone.buttons.white_on_black
    else:
        print(f'Unknown button kind {args.kind}')
        return
    res = b(args.text,
            reg=reg,
            action=args.press, 
            delay=args.delay, 
            retries=1,
            verbose=args.verbose)

    print(f'Button found: {res}')
    return

'''

'''
def test_button_callback():
    print('test button callback')
'''
Free test for what ever new feature
'''
def my_callback(ts, det):
    print("Mycall back")
    x = (det.quad[0][0] + det.quad[1][0]) // 2
    y = det.quad[3][1]
    print(f'button color at x{x} y{y}  {ts.get_rgb(x ,y , scale=False)}')
    if ts.color_match(x, y , 254, 254, 254, threashold=1, scale=False):
        print('Return det')
        return det
    print("Not home")
    return None

def my_test():
    # phone.screen.go_home()
    # return True
    reg = ScreenRegion(phone,
                            xs=int(phone.specs['max_x'] * 0.15),
                            xe=int(phone.specs['max_x'] * 0.30),
                            ys=int(phone.specs['max_y'] * 0.80),
                            ye=int(phone.specs['max_y'] * 0.95),
                            color='green')
    
    reg.npa = phone.image.scan_region(reg)

    print(f'min {reg.npa.min()}, max {reg.npa.max()}')

    test_button_callback()
    b = IconButton(phone, 'pokeball',
                    xs=phone.rel_x(0.38),
                    xe=phone.rel_x(0.62),
                    ys=phone.rel_y(0.85),
                    ye=phone.rel_y(0.97),
                    search_callback=my_callback)

    while True:
        d = b.search()
        if d:
            state = 'home'
        else:
            state = 'somewhere'
        print(f"Icon state {state}")
        print(d)
        sleep(2)

def yuv():
    reg = _set_paramters_from_args()
    reg.color = 'rgb'
    reg.npa = phone.image.scan_region(reg)
    phone.image.show_image(reg.npa[0], 'bw component')
    phone.image.show_image(reg.npa[1], 'u component')
    phone.image.show_image(reg.npa[2], 'v component')

def action(port, arg = None):
    print('Start testing port {}',port)
    global phone
    phone = TouchScreen(port)
    startTime = datetime.now()
  
    if command == 'read':
        ret = read()
    elif re.match('yu.*', command):
        ret = yuv()
    elif re.match('raw.*', command):
        ret = raw_button()
    elif command == 'screen':
        ret = screen()
    elif re.match('ho.*', command):
        ret = home()
    elif re.match('but.*', command):
        ret = button()
    elif re.match('snap.*', command):
        ret = snapshot()
    elif re.match('i.*', command):
        ret = icon()
    elif re.match('bal.*', command):
        ret = ball()
    elif re.match('find.*', command):
        ret = find_rgb()
    elif re.match('test*', command):
        ret = my_test()
    else:
        print(f'Unknown command {command}')
        ret = None
    endTime = datetime.now()
    print(f'Time to find button: {(endTime - startTime).total_seconds()}')

    
def main():

    global args
    global log 
    global command
    
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <command> [options]')
        sys.exit(1)

    command = sys.argv[1]

    
    # 3. Extract the 'remaining' arguments
    # sys.argv[0] is the script name, sys.argv[1] is the command
    remaining_args = sys.argv[2:]
    parser = PokeArgs()
    # Paramters with arguments
    parser.add_argument('--xs', action='store', required=False, default=0, \
                        help='x start.')
    parser.add_argument('--xe', action='store', required=False, default=0, \
                        help='x end.')
    parser.add_argument('--ys', action='store', required=False, default=0, \
                        help='x start.')
    parser.add_argument('--ye', action='store', required=False, default=0, \
                        help='x start.')
    parser.add_argument('--tl', action='store', required=False, default=0, \
                        help='threshold low.', type=int)
    parser.add_argument('-t', '--threshold', action='store', required=False, default=0, \
                        help='threshold high.', type=int)
    parser.add_argument('--count', action='store', required=False, default=1, \
                        help='If something can repeat.', type=int)
    parser.add_argument('--invert', action='store_true', default=False, \
                        help='x start.')
    parser.add_argument('--name', action='store', required=False, default=None, \
                        help='If defined store picture with this name.')
    parser.add_argument('--save', action='store', required=False, default=None, \
                        help='Store picture with this name.')
    parser.add_argument('-c', '--color', action='store', required=False, default='gray', \
                        help='Color mode.')
    parser.add_argument('--text', action='store', required=False, default=None, \
                        help='Where ever text is needed, e.g. button text or input text.')
    parser.add_argument('--kind', action='store', required=False, default='dark', \
                        help='E.g. what kind of button.')
    parser.add_argument('--delay', action='store', required=False, default=0.01, \
                        help='E.g. between detect and pres a button.')
    parser.add_argument('--verbose', action='store', required=False, default=0, \
                        help='E.g. Passed to the library functions.', type=int)
    parser.add_argument('-s', '--show', action='store_true', default=False, \
                        help='E.g. show picture for given milliseconds.')
    parser.add_argument('--show-time', action='store', default=100000, \
                        help='E.g. show picture for given milliseconds.')
    
    # Switches
    parser.add_argument('--process',  action='store_true', default=False, \
                        help='x start.')
    parser.add_argument('--press', nargs='?',const='press', default='check', \
                        help='If button than press default is check only.')
    parser.add_argument('-m', '--mode', action='store', required=False, default='word', \
                        help='Read mode word, line.')
    

    args = parser.parse_args(remaining_args)
    

    log = logging.getLogger('evolve')
    logging.basicConfig(level=args.loglevel)
    log.debug('args {}'.format(args))
    action(args.port)
    print('end')
if __name__ == '__main__':
    main()
