#!/bin/env python

import argparse
import time
from time import sleep
import os
import logging
from pokelib import TouchScreen
from pokelib import ExPokeLibFatal

phone = TouchScreen(3002, "s7")
phone.scroll(0,-400)
