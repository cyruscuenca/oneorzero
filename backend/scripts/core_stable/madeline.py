"""
One or Zero recent changes watcher.

This script creates a server with a single endpoint on port 1738 /madeline and 
consumes page updates.
"""

import os
from time import sleep
from random import randint
import json
from flask import Flask, redirect, url_for, render_template, request
import requests
import datetime
import pywikibot
import wikitextparser as wtp
from pymongo import MongoClient
from pymemcache.client.base import Client
import time
import sys
sys.path.append('../')
import shutil
import requests
from caching import key_collector
import ast

memcache = Client('localhost')
site = pywikibot.Site('en', 'oneorzero')
S = requests.Session()
app = Flask(__name__)
client = MongoClient()

#conn = psycopg2.connect("dbname='deals' user='hak' host='localhost' password='123456'")
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

def template2dict(template):

    transformed = {}

    for argument in template.arguments:

        # Turn comma seperated lists into arrays
        if 'list' in argument.value:

            transformed[argument.name.strip()] = argument.value.split(',')
            for i, item in enumerate(transformed[argument.name.strip()]):

                item = item.strip(' ').strip('\n')
                if item.isspace():

                    transformed[argument.name.strip()].pop(i)
                else:

                    if len(item.wikilinks):

                        transformed[argument.name.strip()] = item.wikilinks[0].text.strip()
                    
        if argument.value.isspace():

            continue

        if argument.value in ['', None, '\n', '\t']:

            continue

        else:

            if hasattr(argument.value, 'wikilinks'):

                if len(argument.value.wikilinks):

                    transformed[argument.name.strip()] = argument.value.wikilinks[0].text.strip()
                else:

                    transformed[argument.name.strip()] = str(argument.value).strip()
            else:

                transformed[argument.name.strip()] = str(argument.value).strip()
            
    return transformed

def mirror2db(slug, content, contains_template, templates):

    # Example: Power Supplies -> power_supplies
    table_key = contains_template['pair'][1].lower().replace(' ', '_')
    table = client['oneorzero'][table_key]
    document = table.find_one({'slug': slug})

    if 'graphics_cards' in document:

        document['graphics_cards'] = []

    # Push template names to template_names
    for template in templates:

        formatted = template.pformat()
        lines = formatted.splitlines()
        template_type = lines[0].lstrip('{{').strip(' ').replace('_', ' ')

        # The "Graphics Card" template is a special sub template that should be appended
        # to the graphics card's object
        if template_type == 'Graphics Card':
            
            if 'graphics_cards' not in document:
                
                document['graphics_cards'] = []
            
            document['graphics_cards'].append(template2dict(template))

        if table.count_documents({ 'slug': slug }, limit = 1) == 0:
            
            table.insert_one(document)

        table.update_one({'slug': slug},  {"$set": document}, upsert=True)
    return True


@app.route('/')
def index():

    return '404'


auth_state = auth()
last_auth = datetime.datetime.now()
key_collector.recache()
@app.route('/madeline', methods=['POST'])
def madeline():

    global auth_state
    global last_auth

    now = datetime.datetime.now()

    # If time delta is greater than 24 hours
    if int((now - last_auth).total_seconds()) > 86400:

        auth_state = auth()
        last_auth = datetime.datetime.now()

    event = dict(request.form)['data']
    event = json.loads(event)

    if 'token' not in event:

        print('ERROR RETURNED')
        return { 'message': 'ERROR: Unverified validation request.'}, 400

    if event['token'] != 'SEhKm2D4k0quCZYs6rsh':

        print('ERROR RETURNED')
        return { 'message': 'ERROR: Unverified validation request.'}, 400

    content = wtp.parse(event['wikiPage'])
    slug = event['title']['mUrlform']
    namespace = int(event['title']['mNamespace'])

    if namespace == 0:

        links = content.wikilinks
        categories = []
        for link in links:

            link = link.title.replace('  ', '')
            if link[0:9] in ['Category:', ' Category:']:

                categories.append(link.lstrip('Category:'))

        # Define a list of template to category mappings
        # First is the table, second is the category, third is the table name
        possibilities = [
            ('GPU', 'GPUs'),
            ('CPU', 'CPUs'),
            ('Fan', 'Fans'),
            ('Power Supply', 'Power supplies'),
            ('Motherboard', 'Motherboards'),
            ('Memory', 'Memory'),
            ('Drive', 'Drives'),
            ('Case', 'Cases'),
            ('Cooler', 'Coolers')
        ]

        # Extract templates from article
        templates = content.templates
        template_names = []

        # Push template names to template_names
        for template in templates:

            formatted = template.pformat()
            lines = formatted.splitlines()
            template_type = lines[0].lstrip('{{').strip(' ').replace('_', ' ')
            template_names.append(template_type.capitalize())
        
        is_watched = False
        contains_template = { 'flag': False, 'pair': None }
        for category in categories:

            # Check if the category is in the template map
            for possibility in possibilities:
                
                if category.capitalize() == possibility[1].capitalize():
                    
                    print('match')
                    is_watched = True
                    contains_template['pair'] = ( possibility[0], possibility[1] )

                    # If the category has a mapping, and the article doesn't have
                    # a template for the category, return an error code
                    if possibility[0].capitalize() not in template_names:

                        contains_template['flag'] = False
                    else:

                        contains_template['flag'] = True
                else:
                    
                    pass

        if is_watched:

            # If the article doesn't have the right template, abort
            if contains_template['flag'] == False:

                return { 'message': 'ERROR: The page you are saving has the category "' + str(contains_template['pair'][1]) + '" but does not have a "' + str(contains_template['pair'][0]) + '" template.'}, 400
            
            mirror = mirror2db(slug, content, contains_template, templates)

            print('mirrored done!')
            return { 'message': 'success'}, 200
    
    elif namespace == 10:

        # Parse template for key value pairs
        recache = key_collector.recache()

        if recache == False:

            print('ERROR RETURNED')
            return { 'message': 'ERROR: The backend cache for the mirrored component database could not be updated with the this template\'s keys. Contact User:Jobgh to get this resolved.'}, 400

    return { 'message': 'success'}, 200

if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port='1738')