import pywikibot
from pymongo import MongoClient
import re
import dateparser
from datequarter import DateQuarter
import pandas as pd
from calendar import monthrange

client = MongoClient()
table = client['oneorzero']['gpus']
site = pywikibot.Site('en', 'oneorzero')

def clean_string(string):
    
    string = str(string).strip(' ')

    string = re.sub('[^0-9a-zA-Z]+', '_', string)
    string = string.replace('__', '')
    string = string.strip('_')
    return string

documents = list(table.find())
for i, document in enumerate(documents):

    if pywikibot.Page(site, document['slug']).exists():

        # Skip this loop if the page already exists
        continue

    # Check if the brand exists. If it doesn't create it.
    # MediaWiki can handle this by itself, but I want this done explicitly.
    if not pywikibot.Page(site, document['company']).exists():

        company = pywikibot.Page(site, document['company'])
        company.save()
    
    title = ''
    title += str(document['company'])
    title += ' ' + str(document['model'])
    title = clean_string(title)
    print('[title] ' + title)

    if 'Q' in str(document['launch_date']):

        q_pos = document['launch_date'].find('Q')
        quarter = 0

        if q_pos == 0 and (len(document['launch_date']) - 1) > q_pos + 1:

            quarter = document['launch_date'][q_pos + 1]

            # Remove the quarter from the string
            document['launch_date'] = document['launch_date'][:q_pos + 1] + document['launch_date'][q_pos + 1 + 1:]
        else: 

            quarter = document['launch_date'][q_pos - 1]

            # Remove the quarter from the string
            document['launch_date'] = document['launch_date'][:q_pos - 1] + document['launch_date'][q_pos - 1 + 1:]

        document['launch_date'] = document['launch_date'].replace('Q', '')
        document['launch_date'] = document['launch_date'].replace(' ', '')
        document['launch_date'] = document['launch_date'].replace('/', '')

        if len(document['launch_date']) == 2:

            document['launch_date'] = str(20) + document['launch_date']

        month = int(quarter) * 3
        normalized = str(month) + '/' + str(1) + '/' + str(document['launch_date'])
        date = str(dateparser.parse(str(normalized)).strftime("%B %d, %Y"))
        document['launch_date'] = date
    else:

        document['launch_date'] = str(dateparser.parse(str(document['launch_date'])).strftime("%B %d, %Y"))


    technologies = []
    if 'supported_tech_list' in document:

        for technology in list(document['supported_tech_list']):

            link = '[[' + clean_string(technology) + ' | ' + str(technology) + ']]'
            technologies.append(link)

    if 'mem_type' in document:

        document['mem_type'] = '[[' + clean_string(document['mem_type']) + ' | ' + str(document['mem_type']) + ']]'

    if 'company' in document:

        document['company'] = '[[' + clean_string(document['company']) + ' | ' + str(document['company']) + ']]'

    # Unsure that all product families are appended with "series"
    # or something similar
    series_syns = ['series', 'line', 'family']
    series_words = set(str(document['family']).lower().split(' '))
    series_present = False

    for syn in series_syns:

        if syn in series_words:

            series_present = True
    
    if series_present ==  False:

        document['family'] += ' Series'

    if 'family' in document:

        document['family'] = '[[' + clean_string(document['family']) + ' | ' + str(document['family']) + ']]'

    page = pywikibot.Page(site, title)
    page.text = ''
    
    infobox = """
        {{{{ GPU |
    """

    for key in ['company', 'model', 'series', 'compute_units', 'base_freq', 'boost_freq', 'ray_accel', 'stream_processors', 'mem_size_list', 'mem_type', 'mem_speed', 'mem_band']:
        
        if key not in ['nan', None, 'null']:

            infobox = infobox + key + '=' + document[key] + ' |'

    infobox = infobox + f"""
        mem_interface={document['mem_interf'].replace('-', ' ').replace('_', ' ')} |
        supported_tech_list={', '.join(technologies)}
        }}}}
    """

    infobox = infobox.replace('  ', '')
    page.text += infobox
    page.text += '\n'

    page.text += 'The ' + str(document['company']) + ' ' + str(document['model']) + ' is '
    page.text += 'a [[GPU]] launched on ' + str(document['launch_date']) + ' by ' + str(document['company']) + '.'
    page.text += f""" The card was a part of the {document['family']} of products."""

    page.text += '\n'
    page.text += '[[Category:AMD]]'
    page.text += '\n'
    page.text += '[[Category:GPUs]]'

    print('[saved] ' + title)
    page.save()

