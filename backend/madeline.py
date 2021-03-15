"""
One or Zero recent changes watcher.

This script creates a server with a single endpoint on port 1738 /madeline and 
consumes page updates.
"""

import os
# import requests as request
from time import sleep
from random import randint
import psycopg2
import json
from flask import Flask, redirect, url_for, render_template, request
import requests
import datetime
import pywikibot

site = pywikibot.Site('en', 'oneorzero')
S = requests.Session()
app = Flask(__name__)

conn = psycopg2.connect("dbname='deals' user='hak' host='localhost' password='123456'")
"""OneOrZero Bot@madeline is bgiufbsq2c8jq2encpumtrlp3783tnv7"""

def auth():

    # Login
    PARAMS_0 = {
        'action': 'query',
        'meta':  'tokens',
        'type': 'login',
        'format': 'json'
    }

    R = S.get(url='http://127.0.0.1/api.php', params=PARAMS_0)

    DATA = R.json()
    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    PARAMS_1 = {
        'action': 'login',
        'lgname': 'OneOrZero Bot@madeline',
        'lgpassword': 'bgiufbsq2c8jq2encpumtrlp3783tnv7',
        'lgtoken': LOGIN_TOKEN,
        'format': 'json'
    }

    R = S.post(url='http://127.0.0.1/api.php', data=PARAMS_1)
    DATA = R.json()
    
    if DATA['login']['result'] == 'Success':

        return True
    else:

        return False

def get_watchlist():

    pages = []
    building = True
    start_from = None
    while building:

        building = False
        PARAMS_1 = {
            'action': 'query',
            'list': 'watchlistraw',
            'wrlimit': 500,
            'wrnamespace': 0,
            'format': 'json'
        }

        if start_from is not None:

            PARAMS_1['wrfromtitle'] = start_from

        R = S.post(url='http://127.0.0.1/api.php', data=PARAMS_1)
        DATA = dict(R.json())
        
        if 'continue' in DATA.keys():

            start_from = DATA['continue']['wrcontinue']
            building = True
        else:

            start_from = None

        pages.extend(DATA['watchlistraw'])

    return pages
    
auth_state = auth()
last_auth = datetime.datetime.now()

watchlist = get_watchlist()
last_watchlist_refresh = datetime.datetime.now()

@app.route('/')
def index():

    return '404'

@app.route('/madeline', methods=['POST'])
def madeline():

    global auth_state
    global last_auth
    global last_watchlist_refresh
    global watchlist

    now = datetime.datetime.now()

    # If time delta is greater than 24 hours
    if int((now - last_auth).total_seconds()) > 86400:

        auth_state = auth()
        last_auth = datetime.datetime.now()

    # If time delta is greater than 15 minutes
    if int((now - last_watchlist_refresh).total_seconds()) > 900:

        watchlist = get_watchlist()
        last_watchlist_refresh = datetime.datetime.now()

    event = dict(request.form)['data']
    event = json.loads(event)

    title = event['wikiPage']['mTitle']['mTextform']
    page_path = event['wikiPage']['mTitle']['mUrlform']
    user_name = event['user']['mName']

    if {'ns': 0, 'title': title} in watchlist:

        print('page was watched')
    else:
        print(title + ' was updated by ' + user_name + '. However, the page is not monitored, so nothing was pushed to the database')

    return '200'

if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port='1738')