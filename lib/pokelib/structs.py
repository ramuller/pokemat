import numpy as np
from dataclasses import dataclass
from pokelib import ExPokeLibError


class ExRegion(Exception):
    """ Somthing fatal should not be ignored """
    pass

@dataclass
class Region:
    npa : np.ndarray       # Numpy Area from screen
    nwa : np.ndarray       # Numpy Work area
    xs : int
    xe : int
    ys : int
    ye : int
    tl : int               # threshold low
    th : int
    color : str = 'gray'
    mode: str = 'word'
    invert: bool = False
    process: bool = False
    threshold: int = 0
    blur: int = 0
    scan: bool = False
    scan_dir: str = 'vertical'
    scan_step: int = 4
    # Factor to over smaple the scan area to avoid missing small buttons, in pixels
    scan_overlap: int = 2
class ScreenRegion(Region):
    def __init__(self, ts, xs=0, xe=0, ys=0, ye=0, 
                 tl=0, th=255, color='gray', mode='word', 
                 invert=False, process=False,
                 threshold=0, blur=0):
        self.ts = ts
        if xs < 0  \
            or xe > ts.specs['max_x'] \
            or ys < 0 \
            or ye > ts.specs['max_y']:
            raise ExRegion(f'Region parameter out of bounce xe{xe} xs{xs} ys{ys} ye{ye}')
        
        if xe == 0:
            xe = ts.specs['max_x']
        if ye == 0:
            ye = ts.specs['max_y']
        super().__init__(None, None, xs, xe, ys, ye, tl, th, color, mode, invert, process, threshold, blur)

    def foo(self):
        print('foo')

