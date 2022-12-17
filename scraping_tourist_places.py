import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd
from collections import OrderedDict

STATE_N_FT = ['Malaysia','Kelantan','Pahang','Kedah','Sabah','Terengganu','Malacca','Negeri Sembilan','Perak','Perlis', 'Kuala Lumpur','Putrajaya','Labuan']

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("C:\PythonDevelopment\chromedriver", chrome_options=options)

tourist_places = []
for state in STATE_N_FT:
    # try:
        print(f'getting --> https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_{state}')
        driver.get(f"https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_{state}")
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,'lxml')
        type_tag = 'h3' if soup.select('h3+ul li a') else 'h2'
        tourist_places_tag = soup.select(f'{type_tag}+ul li a')
        attraction_type = ''
        for place_tag in tourist_places_tag:
            attraction_type_element = place_tag.previous_element.previous_element.find_previous_sibling(type_tag)
            # print(attraction_type_element.select_one('span.mw-headline').text if attraction_type_element else 'no no')
            attraction_type = attraction_type_element.select_one('span.mw-headline').text if attraction_type_element else attraction_type    
            place = place_tag.text
            tourist_places.append({'type':attraction_type,'place':place,'state':state})
            # print({'type':attraction_type,'place':place})
    # except:
    #     print(f'{state} is not found!!!!!!!')
    #     continue    

df =  pd.DataFrame(tourist_places)
df = df[df['type']!='See also']
print(df)
df.to_csv('tourist_places.csv',index=False)
