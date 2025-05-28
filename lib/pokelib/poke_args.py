from argparse import ArgumentParser
import os
import logging

class PokeArgs(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.phone_port = os.getenv("PHONE_PORT")
        if self.phone_port == "":
            self.add_argument("-p", "--port", action="store", required=True, \
                              help="TCP port for the connection ot define envrinment variabe PHONE_PORT")
        else:
            self.add_argument("-p", "--port", action="store", required=False, default=self.phone_port, \
                              help="TCP port for the connection.")
        self.add_argument("-P", "--phone", action="store", required=False, default="s7", \
                                help="Name os the phone model. Check phones.json.")
        self.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
            
            
        