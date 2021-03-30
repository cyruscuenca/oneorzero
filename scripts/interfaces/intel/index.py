import os
import requests as request
from time import sleep
from random import randint
import psycopg2
from pymongo import MongoClient
import base64
import json

client = MongoClient()

class IntelInterface:

    def __init__(self):
        
        self.BASE_ENDPOINT = 'https://apis-sandbox.intel.com/v1/'
        # 4b3b2529-7040-43b1-a337-6f72da2d996f 
        self.CLIENT_ID = 'HZTdQ7hUjw1xF1y5h1B1qiSLfElxJtjh'
        self.CLIENT_SECRET = '1H8UKOarE6xkNM5c'
        self.REDIRECT_URI = 'https://www.oneorzero.org'

    def auth(self):

        params = {
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URI,
        }
        print(self.BASE_ENDPOINT + 'auth/authorize' )
        contact = request.get(self.BASE_ENDPOINT + 'auth/authorize', params=params)
        print(contact.__dict__)

        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'code': '200'
        }

        contact = request.post(self.BASE_ENDPOINT + 'auth/token', data=data)
        print(contact.__dict__)


interface = IntelInterface()
interface.auth()
