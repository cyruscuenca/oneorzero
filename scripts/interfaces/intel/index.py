"""
By default, 1 million requests per month are allowed with a rate of 5 requests per second.
If you have any queries or problems regarding this API, please contact:
pim360.apigeesupport@intel.com.
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
from interfaces.intel.functions import *

class IntelInterface:

    def __init__(self):

        self.APP_ID = '4b3b2529-7040-43b1-a337-6f72da2d996f'
        self.CLIENT_ID = '6a585184-ffed-48c5-8d66-fbad21e5227d'
        self.CLIENT_SECRET = '4wWR8jA-Rf06F~SES1ymFIl9H6.3_CJ~Hl'
        self.TOKEN = None
        self.AUTH_ENDPOINT = 'https://apis-sandbox.intel.com/v1/'
        self.API_ENDPOINT = 'https://apis.intel.com/pim/v1/'
        self.CATEGORIES = []
        self.CODENAMES = []
        self.PRODUCTS = []

    def auth(self):

        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }

        response = request.post(self.AUTH_ENDPOINT + 'auth/token', data=data)
        content = json.loads(response.content.decode('utf-8'))
        
        try:
            self.TOKEN = content['access_token']
            print('[MESSAGE] Token was assigned!')

        except:

            self.TOKEN = None
            return False

        return True

    def get_categories(self, count):

        if self.TOKEN == None:

            print('ERROR: Auth token is NoneType. Type of "str" was expected.')
            return False
        
        pages = math.ceil(count / 1000)
        categories = []
        for offset, page in enumerate(range(pages)):

            params = {
                'localeGeoId': 'en-US',
                'sort': 'order:asc',
                'limit': 1000,
                'offset': offset + 1
            }

            headers = {
                'Authorization': 'Bearer ' + self.TOKEN
            }

            response = request.get(self.API_ENDPOINT + 'services/categories', params=params, headers=headers)
            response = json.loads(response.content.decode('utf-8'))

            categories.extend(response['categories'])

            # End loop if this request returns less than the limit, because
            # the next request will return nothing anyways
            if response['_metadata']['count'] < params['limit']:

                break
            
        return categories[:count]

    def get_codenames(self, count):

        if self.TOKEN == None:

            print('ERROR: Auth token is NoneType. Type of "str" was expected.')
            return False
        
        pages = math.ceil(count / 1000)
        codenames = []
        for offset, page in enumerate(range(pages)):

            params = {
                'localeGeoId': 'en-US',
                'sort': 'name:asc',
                'limit': 1000,
                'offset': offset + 1
            }

            headers = {
                'Authorization': 'Bearer ' + self.TOKEN
            }

            response = request.get(self.API_ENDPOINT + 'services/codenames', params=params, headers=headers)
            response = json.loads(response.content.decode('utf-8'))
            codenames.extend(response['codeNames'])

            # End loop if this request returns less than the limit, because
            # the next request will return nothing anyways
            if response['_metadata']['count'] < params['limit']:

                break
            
        return codenames[:count]

    def get_processors(self, count):

        if self.TOKEN == None:

            print('ERROR: Auth token is NoneType. Type of "str" was expected.')
            return False
        
        pages = math.ceil(count / 1000)
        products = []
        for offset, page in enumerate(range(pages)):

            params = {
                'localeGeoId': 'en-US',
                'categoryId': '873',
                'limit': 1000,
                'includeAttributes': 'true',
                'offset': offset + 1
            }

            headers = {
                'Authorization': 'Bearer ' + self.TOKEN
            }

            response = request.get(self.API_ENDPOINT + 'services/products', params=params, headers=headers)
            response = json.loads(response.content.decode('utf-8'))
            products.extend(response['products'])

            # End loop if this request returns less than the limit, because
            # the next request will return nothing anyways
            if len(response['products']) < params['limit']:

                break
            
        return products[:count]

    def set_categories(self):

        self.CATEGORIES = self.get_categories(99*99*99)

        # This appends the categories to disk for development reference
        """
        for i, category in enumerate(self.CATEGORIES):
            
            file = open('temp.txt', 'a')
            file.write(str(category))
            file.write('\n')
            file.close()
        """

    def set_codenames(self):

        self.CODENAMES = self.get_codenames(99*99*99)

        # This appends the categories to disk for development reference
        """
        for i, codename in enumerate(self.CODENAMES):
            
            file = open('temp2.txt', 'a')
            file.write(str(codename))
            file.write('\n')
            file.close()
        """

    def set_processors(self):

        products = self.get_processors(99*99*99)

        print('got products')
        for product in products:

            product = normalize_processor(product)

        self.PRODUCTS = products

        # This appends the categories to disk for development reference
        """
        for i, product in enumerate(self.PRODUCTS):
            
            file = open('temp3.txt', 'a')
            file.write(str(product))
            file.write('\n')
            file.close()
        """