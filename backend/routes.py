import os
import requests as request
from time import sleep
from random import randint
import psycopg2
from pymongo import MongoClient
from flask import Flask, redirect, url_for, render_template, jsonify
import base64
import json

app = Flask(__name__)

# conn = psycopg2.connect("dbname='deals' user='hak' host='localhost' password='123456'")
client = MongoClient()

@app.route('/')
def index():

    quips = [
        'What do you want to know?'
    ]

    return render_template('/pages/index.html', quip=quips[randint(0, len(quips) - 1)])

@app.route('/charts/<product_class>/')
def compare(product_class):

    types = [
        ['gpus', 'Graphics cards'],
        ['cpus', 'Processors'],
        ['fans', 'Fans'],
        ['cases', 'Cases'],
        ['power-supplies', 'Power supplies'],
        ['motherboards', 'Motherboards'],
        ['coolers', 'Coolers'],
        ['drives', 'Drives']
    ]

    match = None
    for _type in types:

        if product_class == _type[0]:
    
            match = _type
            break

    if match is None:

        return 'Invalid URL!'

    table = client['oneorzero'][str(match[0])]
    products = list(table.find({}).sort([['_id', -1]]))
    uniques = []
    
    for product in products:

        del product['_id']

        for key, value in product.items():
            
            if str(value) == 'nan':

                product[key] = 'null'

        if product not in uniques:

            uniques.append(product)

    json_encoded = json.dumps(uniques)

    valid_axes = [
        'launch_date',
        'compute_units',
        'base_freq',
        'boost_freq',
        'ray_accel',
        'max_perf',
        'stream_processors',
        'trans_count',
        'tbp_d',
        'mem_speed',
        'mem_size_list',
        'mem_type',
        'mem_band'
    ]

    return render_template('/pages/chart.html', header=match[1].lower(), products=json_encoded, valid_axes=valid_axes)

@app.route('/benchmark/')
def benchmark():

    return render_template('/pages/benchmark.html', header='Benchmark your PC')

@app.route('/about/')
def about():

    return render_template('/pages/about.html')

@app.route('/contact/')
def contact():

    return render_template('/pages/contact.html')

@app.route('/api/about')
def api_about():

    return render_template('/pages/api_about.html')

@app.route('/contribute/')
def contribute():

    return render_template('/pages/contribute.html')

@app.route('/404')
def error_404():

    return '404.html'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8020)