from argparse import ArgumentParser
import os
import logging

class PokeArgs(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.phone_port = os.getenv("PHONE_PORT")
        self.gps_rest_url = os.getenv("GPS_REST_URL")
        if self.phone_port == "":
            self.add_argument("-p", "--port", action="store", required=True, \
                              help="TCP port for the connection ot define envrinment variabe PHONE_PORT")
        else:
            self.add_argument("-p", "--port", action="store", required=False, default=self.phone_port, \
                              help="TCP port for the connection.")

        self.add_argument("--gps-rest-url", action="store", required=False, default="http://localhost:2769", \
                              help="GPSSource REST url.")
        self.add_argument('-l', '--loglevel', action='store', default=logging.INFO)            
            
        