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
import shutil
import pandas as pd
from pymongo import MongoClient

"""
options = Options()
options.add_argument("--headless")

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.panel.shown', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

# use the out folder of the script path
profile.set_preference('browser.download.dir', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'))

# Selenium driver
service = Service('./geckodriver')
driver = webdriver.Firefox(executable_path='./geckodriver', options=options, firefox_profile=profile)
driver.set_window_size(1024, 768)
driver.set_script_timeout(256)

proxies = open('./proxies.txt').read().splitlines()

for i, proxy in enumerate(proxies):

  proxies[i] = 'https://' + str(proxy)

proxy_cycle = 0
def get_proxy():

  global proxy_cycle
  proxy_cycle += 1

  if proxy_cycle > len(proxies) - 1:

    proxy_cycle = 0

  return proxies[proxy_cycle]

shutil.rmtree('out')
os.mkdir('out')

driver.get('https://www.amd.com/en/products/specifications/processors')

export = driver.find_element_by_xpath('//button[@title="Export data"]')
export.click()
parent = export.find_element_by_xpath('./..')
parent.find_element_by_xpath('//*[contains(text(), "CSV/Excel")]').click()

driver.quit()
"""
client = MongoClient()
table = client['oneorzero']['processors']
df = pd.read_csv('./out/tableExport.csv', index_col=False)

for i in range(len(df.index)):

  data = {
    'company': 'AMD',
    'model': df.loc[i, 'Model'].lstrip('AMD '),
    'platform': df.loc[i, 'Platform'],
    'family': df.loc[i, 'Family'].lstrip('AMD '),
    'launch_date': df.loc[i, 'Launch Date'],
    'cpu_core_count': df.loc[i, '# of CPU cores'],
    'thread_count': df.loc[i, '# of Threads'],
    'gpu_core_count': df.loc[i, '# of GPU Cores
    'launch_date': df.loc[i, 'Base Clock'],
    'launch_date': df.loc[i, 'Max Boost Clock'],
    'launch_date': df.loc[i, 'Total L1 Cache'],
    'launch_date': df.loc[i, 'Total L2 Cache'],
    'launch_date': df.loc[i, 'Total L3 Cache'],
    'launch_date': df.loc[i, 'Unlocked'],
    'launch_date': df.loc[i, 'CMOS'],
    'launch_date': df.loc[i, 'Package'],
    'PCI Express': df.loc[i, 'Default TDP'],
    'PCI Express': df.loc[i, 'Max Temps'],
    'PCI Express': df.loc[i, 'System Memory Specification'],
    'PCI Express': df.loc[i, 'System Memory Type'],
    'PCI Express': df.loc[i, 'Graphics Frequency'],
    'PCI Express': df.loc[i, 'Graphics Model'],
    'PCI Express': df.loc[i, 'Graphics Core Count'],
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

    
  data['supported_tech'] = technologies
  insert = table.insert_one(data).inserted_id

  print('inserted ' + str(insert))