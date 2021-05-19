import configparser
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
client = MongoClient()

@app.route('/')
def index():

    return None

@app.route('/charts/<product_class>/')
def compare(product_class):

    return None

if __name__ == '__main__':
    app.run(debug=True)