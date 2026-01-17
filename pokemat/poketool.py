#!/bin/env python
import math
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal
from pokelib import PokeArgs

import logging

import json
import sys
import re
from datetime import datetime


def _int(x, d='y'):
    if d == 'x':
        max = phone.specs['max_x'] 
    else:
        max = phone.specs['max_y'] 

    if re.match(r'^\d+%$', x):
        return math.floor((int(x[:-1]) * max) / 100)
    elif re.match(r'^\d+x$', x):
        return int(x)
    else:
        print(f'Unknown format {x} only abs and % supported')
        sys.exit(1)

def _set_paramters_from_args(ocr):
        
    if args.xs != 0:
        ocr.startx = _int(args.xs)
    if args.ys != 0:
        ocr.starty = _int(args.ys)
    if args.xe == 0:
        ocr.endx = phone.specs['max_x']
    else:    
        ocr.endx = _int(args.xe)
    if args.ye == 0:
        ocr.endy = phone.specs['max_y']
    else:    
        ocr.endy = _int(args.ye)
    ocr.invert = args.invert
    ocr.process = args.process
    ocr.mode = args.mode

def _post_process(p_npa):
    if args.show:
        phone.image.show_image(p_npa, wait=10000, title='Read region')
    if args.name:
        phone.image.save_image(p_npa, args.name)
        print(f'Saved image to {args.name}')

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


def icon():
    if not  args.name:
        print('Button command needs --name argument')
        return
    _set_paramters_from_args(phone.buttons.ocr)
    
    print(f'Search icon in region x:{phone.pocr.startx}-{phone.pocr.endx} y:{phone.pocr.starty}-{phone.pocr.endy}')
    print(f'invert:{phone.pocr.invert} process:{phone.pocr.process} mode:{phone.pocr.mode} text:{args.text} kind:{args.kind} press:{args.press}')

    icon_button = getattr(phone.buttons, args.name)

    ib = icon_button.press(delay=1)

    startTime = datetime.now()
    
def screen():
    

    print(f'Current screen is "{phone.screen.get_current_screen(verbose=args.verbose)}"')
    icon_button = getattr(phone.buttons, args.name)

    ib = icon_button.press(delay=1)

    startTime = datetime.now()
    
def button():
    if not  args.text:
        print('Button command needs --text argument')
        return
    _set_paramters_from_args(phone.buttons.ocr)
    
    print(f'Search button in region x:{phone.pocr.startx}-{phone.pocr.endx} y:{phone.pocr.starty}-{phone.pocr.endy}')
    print(f'invert:{phone.pocr.invert} process:{phone.pocr.process} mode:{phone.pocr.mode} text:{args.text} kind:{args.kind} press:{args.press}')

    startTime = datetime.now()
    if args.kind == 'dark':
        b = phone.buttons.dark
    elif args.kind == 'light':
        b = phone.buttons.light
    elif args.kind == 'black_on_white':
        b = phone.buttons.black_on_white
    elif args.kind == 'white_on_black':
        b = phone.buttons.white_on_black
    else:
        print(f'Unknown button kind {args.kind}')
        return
    res = b(args.text, 
            action=args.press, 
            delay=args.delay, 
            retries=1, 
            verbose=args.verbose)
    endTime = datetime.now()
    print(f'Time to find button: {(endTime - startTime).total_seconds()}')

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
    elif command == 'button':
        ret = button()
    elif command == 'screen':
        ret = screen()
    elif re.match('i.*', command):
        ret = icon()
    else:
        print(f'Unknown command {command}')
        ret = None
    startTime = datetime.now()
    
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
    parser.add_argument('--invert', action='store_true', default=False, \
                        help='x start.')
    parser.add_argument('--name', action='store', required=False, default=False, \
                        help='If defined store picture with this name.')
    parser.add_argument('--text', action='store', required=False, default=None, \
                        help='Where ever text is needed, e.g. button text or input text.')
    parser.add_argument('--kind', action='store', required=False, default='dark', \
                        help='E.g. what kind of button.')
    parser.add_argument('--delay', action='store', required=False, default=0.01, \
                        help='E.g. between detect and pres a button.')
    parser.add_argument('--verbose', action='store', required=False, default=0, \
                        help='E.g. Passed to the library functions.', type=int)

    # Switches
    parser.add_argument('--process',  action='store_true', default=False, \
                        help='x start.')
    parser.add_argument('--press', nargs='?',const='press', default='check', \
                        help='If button than press default is check only.')
    parser.add_argument('-m', '--mode', action='store', required=False, default='word', \
                        help='Read mode word, line.')
    parser.add_argument('-s', '--show', action='store_true', default=False, \
                        help='E.g. show picture from where it reads.')    

    args = parser.parse_args(remaining_args)
    

    log = logging.getLogger('evolve')
    logging.basicConfig(level=args.loglevel)
    log.debug('args {}'.format(args))
    action(args.port)
    print('end')
if __name__ == '__main__':
    main()
