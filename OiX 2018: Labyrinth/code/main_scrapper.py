########### Python 2.7 #############
import httplib, urllib, base64, json

import utils

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib import patches
from io import BytesIO
import requests
 
import time 

plt.close("all")

from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep
 
import scrapper_lib

companyurls = ['https://www.linkedin.com/company/tata-consultancy-services']
extracted_data = []

#for url in companyurls:
#    extracted_data.append(scrapper_lib.linkedin_companies_parser(url))
#    f = open('data.json', 'w')
#    json.dump(extracted_data, f, indent=4)
#        

#import urllib2 as URL
#
#urlopener= URL.build_opener()
#urlopener.addheaders = [('User-agent', 'Mozilla/5.0')]
#html= urlopener.open('https://www.linkedin.com/in/manuwhs').read()



from subprocess import call
#call(["export CHROMEDRIVER=~/chromedriver", ""])
os.system("export CHROMEDRIVER=~/chromedriver")
from selenium import webdriver
driver = webdriver.Chrome('./chromedriver') 
 
from linkedin_scraper import Person
person = Person("https://www.linkedin.com/in/manuwhs")