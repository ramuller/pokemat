import logging
import os


class PokeLogger():
    def __init__(self, name):
        self.logger = logging.getLogger(name)
    
    def get_logger(self):
        return self.logger
    
    def set_level(self, level):
        str_2_ll = {
            "info": logging.INFO,
            "debug": logging.DEBUG
            }
        print(type(level))
        if type(level) == str:
            level = str_2_ll[level]
        logging.basicConfig(level=level)