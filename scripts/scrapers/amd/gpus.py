import requests as request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from time import sleep
import os
from os import listdir
from os.path import isfile, join
import shutil
import pandas as pd
from pymongo import MongoClient


options = Options()
options.add_argument("--headless")

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.panel.shown', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

# use the out folder of the script path
profile.set_preference('browser.download.dir', os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'gpu_exports'))

# Selenium driver
service = Service('../geckodriver')
driver = webdriver.Firefox(
    executable_path='../geckodriver', options=options, firefox_profile=profile)
driver.set_window_size(1024, 768)
driver.set_script_timeout(256)

proxies = open('../proxies.txt').read().splitlines()
for i, proxy in enumerate(proxies):

    proxies[i] = 'https://' + str(proxy)

proxy_cycle = 0

def get_proxy():

    global proxy_cycle
    proxy_cycle += 1

    if proxy_cycle > len(proxies) - 1:

        proxy_cycle = 0

    return proxies[proxy_cycle]

shutil.rmtree('gpu_exports')
os.mkdir('gpu_exports')

driver.get('https://www.amd.com/en/products/specifications/graphics')

export = driver.find_element_by_xpath('//button[@title="Export data"]')
export.click()
parent = export.find_element_by_xpath('./..')
parent.find_element_by_xpath('//*[contains(text(), "CSV/Excel")]').click()

driver.quit()

client = MongoClient()
table = client['oneorzero']['graphics-cards']

files = [f for f in listdir('./gpu_exports/') if isfile(join('./gpu_exports/', f))]
print(files)

df = pd.read_csv('./gpu_exports/' + str(files[0]), index_col=False)

for i in range(len(df.index)):

    data = {
        'company': 'AMD',
        'model': df.loc[i, 'Model'].lstrip('AMD '),
        'type': df.loc[i, 'Type'],
        'family': df.loc[i, 'Family'].lstrip('AMD '),
        'launch_date': df.loc[i, 'Launch Date'],
        'compute_units': df.loc[i, 'Compute Units'],
        'base_freq': df.loc[i, 'Base Frequency'],
        'boost_freq': df.loc[i, 'Boost Frequency'],
        'ray_accel': df.loc[i, 'Ray Accelerators'],
        'max_perf': df.loc[i, 'Max Performance'],
        'fp16_perf': df.loc[i, 'Peak Half Precision (FP16) Performance'],
        'fp32_perf': df.loc[i, 'Peak Single Precision (FP32) Performance'],
        'fp64_perf': df.loc[i, 'Peak Double Precision (FP64) Performance'],
        'stream_processors': df.loc[i, 'Stream Processors'],
        'trans_count': df.loc[i, 'Transistor Count'],
        'tbp_d': df.loc[i, 'Typical Board Power (Desktop)'],
        'mem_speed': df.loc[i, 'Memory Speed'],
        'mem_size': df.loc[i, 'Max Memory Size'],
        'mem_type': df.loc[i, 'Memory Type'],
        'mem_interf': df.loc[i, 'Memory Interface'],
        'mem_band': df.loc[i, 'Memory Bandwidth']
    }

    # Yeah, yeah. I know this is lazy.1
    technologies = str(df.loc[i, 'Supported Technologies']).split(',')
    while '' in technologies or None in technologies or 'nan' in technologies:

        try:

            technologies.remove('nan')
        except:

            pass

        try:

            technologies.remove('')
        except:

            pass

        try:

            technologies.remove(None)
        except:

            pass
    
    for i, technology in enumerate(technologies):

        technologies[i] = technology.strip(' ')

    data['supported_tech'] = technologies

    insert = table.insert_one(data).inserted_id
    print('inserted ' + str(insert))
