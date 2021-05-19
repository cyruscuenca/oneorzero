"""
AMD Product Specifications Tool webscraper
"""

import os
import requests as request
from time import sleep
from random import randint
import base64
import json
import math
import re

# Path is in /scripts due to imports from the database_updaters folder
# from interfaces.intel.functions import *

class AMDInterface:

    def __init__(self):
        pass

    def auth(self):

        return True

    def get_categories(self, count):
    
        return False

    def get_codenames(self, count):

        return False

    def get_processors(self, count):

        return False

    def set_categories(self):

        return False

    def set_codenames(self):

        return False

    def set_processors(self):

        return False