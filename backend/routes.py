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
        'graphics-cards',
        'cpus',
        'fans',
        'cases'
    ]

    if str(product_class) not in types:

        return 'Invalid URL!'

    table = client['oneorzero'][str(product_class)]
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
    product_class = product_class.replace('-', ' ')

    valid_axes = [
        'launch_date',
        'compute_units',
        'base_freq',
        'boost_freq',
        'ray_accel',
        'max_perf',
        'fp16_perf',
        'fp32_perf',
        'fp64_perf',
        'stream_processors',
        'trans_count',
        'tbp_d',
        'mem_speed',
        'mem_size',
        'mem_type',
        'mem_interf',
        'mem_band'
    ]

    return render_template('/pages/chart.html', header=product_class, products=json_encoded, valid_axes=valid_axes)

@app.route('/:class/<slug>/')
def product(slug):

    return redirect(url_for('error_404'))

@app.route('/404')
def error_404():

    return '404.html'

if __name__ == '__main__':
    app.run(debug=True)