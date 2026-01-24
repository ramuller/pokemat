#!/bin/env python
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs
from pokelib.buttons import ButtonParameter

import logging

import json
import sys
import re
from datetime import datetime
from time import sleep


def _int(x, d='y'):
    if d == 'x':
        max = phone.specs['max_x'] 
    else:
        max = phone.specs['max_y'] 

    if re.match(r'^\d+%$', x):
        return math.floor((int(x[:-1]) * max) / 100)
    elif re.match(r'^\d+$', x):
        return int(x)
    else:
        print(f'Unknown format {x} only abs and % supported')
        sys.exit(1)

def _set_paramters_from_args(ocr):
        
    if args.xs != 0:
        ocr.startx = _int(args.xs, d='x')
    if args.ys != 0:
        ocr.starty = _int(args.ys)
    if args.xe == 0:
        ocr.endx = phone.specs['max_x']
    else:    
        ocr.endx = _int(args.xe, d='x')
    if args.ye == 0:
        ocr.endy = phone.specs['max_y']
    else:    
        ocr.endy = _int(args.ye)
    ocr.invert = args.invert
    ocr.process = args.process
    ocr.mode = args.mode
    print(ocr.invert)

def _post_process(p_npa):
    if args.show:
        phone.image.show_image(p_npa, wait=10000, title='Read region')
    if args.save:
        path = f'{phone.config_path}/icons/screen-shots/{args.save}'
        if not re.match(r'.*\.png$', path):
            path += '.png'
        phone.image.save_image(p_npa, path)
        print(f'Saved image to {path}')

def _schow_screen(ocr):
    
    _set_paramters_from_args(ocr)
    npa = phone.image.scan_region(xs=ocr.startx, ys=ocr.starty, xe=ocr.endx, ye=ocr.endy, channel="gray")
    return phone.image.show_image(npa, wait=int(args.show_time), title='Screen shoot')

def read():
    _set_paramters_from_args(phone.pocr)

    print(f'Reading region x:{phone.pocr.startx}-{phone.pocr.endx} y:{phone.pocr.starty}-{phone.pocr.endy}')
    print(f'invert:{phone.pocr.invert} process:{phone.pocr.process} mode:{phone.pocr.mode}') 

    startTime = datetime.now()
    text, npa, p_npa = phone.pocr.read_and_npa()
    endTime = datetime.now()
    print(f'Time to find button: {(endTime - startTime).total_seconds()}')

    _post_process(p_npa)
    for t in text:
        print(t)
    return

def snapshot ():

    print("Press 'q' to not save anything")
    o= phone.pocr 
    k = _schow_screen(o)
    print(f"Got key {str(k)}")
    if k == 113:
        return
    for i in range(int(args.count)):
        fn = f'{phone.config_path}/icons/screen-shots/{args.name}-{i}.png'
        print(f'Save {fn }')
        npa = phone.image.scan_region(xs=o.startx, xe=o.endx, \
                                      ys=o.starty, ye=o.endy)
        phone.image.save_image(npa, fn)
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
    _set_paramters_from_args(phone.buttons.ocr)
    
    print(f'Search icon in region x:{phone.pocr.startx}-{phone.pocr.endx} y:{phone.pocr.starty}-{phone.pocr.endy}')
    print(f'invert:{phone.pocr.invert} process:{phone.pocr.process} mode:{phone.pocr.mode} text:{args.text} kind:{args.kind} press:{args.press}')

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
    method = getattr(phone.buttons, args.name)
    rep = args.count
    for i in range(rep):
        detection = method.search(
                 retries=1, 
                 verbose=args.verbose)
        if not method.updated and detection:
            print('Update button search area based on result')
            method.update_area(detection)
    print(f'Button found:')
    print(detection)
    _set_paramters_from_args(phone.pocr)
    
    if args.show:
        _schow_screen(phone.pocr)
    return

'''
Directly using the button functions
'''
def raw_button():
    print("Command : raw-button")
    if not  args.text:
        print('Raw button command needs --text argument')
        return
    _set_paramters_from_args(phone.buttons.ocr)
    
    print(f'Search button in region x:{phone.pocr.startx}-{phone.pocr.endx} y:{phone.pocr.starty}-{phone.pocr.endy}')
    print(f'invert:{phone.pocr.invert} process:{phone.pocr.process} mode:{phone.pocr.mode} text:{args.text} kind:{args.kind} press:{args.press}')

    if args.kind == 'dark':
        b = phone.buttons.dark
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
            action=args.press, 
            delay=args.delay, 
            retries=1, 
            verbose=args.verbose)

    print(f'Button found: {res}')
    return

def action(port, arg = None):
    global phone
    print('Start testing port {}',port)
    global phone
    phone = TouchScreen(port)
    startTime = datetime.now()
    if command == 'read':
        ret = read()
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
    parser.add_argument('--count', action='store', required=False, default=1, \
                        help='If something can repeat.')
    parser.add_argument('--invert', action='store_true', default=False, \
                        help='x start.')
    parser.add_argument('--name', action='store', required=False, default=None, \
                        help='If defined store picture with this name.')
    parser.add_argument('--save', action='store', required=False, default=None, \
                        help='Store picture with this name.')
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
