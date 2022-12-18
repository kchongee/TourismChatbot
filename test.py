import requests
import html
import pandas as pd
import re
import time 

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


# Test Pandas
# df = pd.read_csv('tourist_places.csv')
# print(df)
# df = df.fillna('')
# dict = df.to_dict('records')
# print(dict)

# Test Selenium 
# [Scrap FAQs]
# def expand_faq(find_faq_elements_func):            
#     elements_to_expand = find_faq_elements_func()
#     # print(len(elements_to_expand))
#     for element in elements_to_expand:                
#         element.click()
#     time.sleep(2)
#     # print(len(find_faq_elements_func()))

# def find_faq_elements():
#     try:        
#         return WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[jsname="Cpkphb"]')))                        
#     except TimeoutException:
#         print("Loading took too much time!")
#         find_faq_elements()
#     finally:
#         print("Page is ready!")

# Chrome driver
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
# driver = webdriver.Chrome("C:\PythonDevelopment\chromedriver", chrome_options=options)

# Firefox driver
options = Options()
# options.set_preference("general.useragent.override", user_agent)
# options.set_preference("dom.webnotifications.serviceworker.enabled", False)
# options.set_preference("dom.webnotifications.enabled", False)
options.set_preference("browser.privatebrowsing.autostart", True)
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')
service = Service(r"C:\Users\666\Downloads\FirefoxDriver.exe")
driver = Firefox(service=service, options=options)

driver.get(f"https://www.google.com.my/search?q=Which part of Malaysia is the best?&")    

# input = driver.find_element(By.CSS_SELECTOR, 'input.gLFyf')
# input.send_keys('Which part of Malaysia is the best?')
# input.submit()
# time.sleep(2)

# # click to expand the faq so that generate more faq
# expand_faq(find_faq_elements)

# # parse whole page source to use BeautifulSoup to scrape
# page_source = driver.page_source
# soup = BeautifulSoup(page_source,'lxml')

# faqs_list = []
# faqs_elements = soup.select('div[jsname="Cpkphb"]') # people also asked, each element
# # print(len(faqs_elements))
# for faqs_element in faqs_elements:        
#     question_element = faqs_element.select_one('div[jsname="Cpkphb"] div.iDjcJe span') # question        
#     link_element = faqs_element.select_one('div[jsname="Cpkphb"] div.yuRUbf a') # link
#     title_element = link_element.select_one('h3') # title
#     full_answer_element = faqs_element.select_one('div.di3YZe') or faqs_element.select_one('span.hgKElc') # full answer
#     short_answer_element = full_answer_element.select_one('b') # short answer
#     answer_list_elements = faqs_element.select('div.di3YZe ul li') # answer in list

#     question = html.unescape(question_element.text) if question_element else ''
#     link = link_element['href'] if link_element else ''
#     title = html.unescape(title_element.text) if title_element else ''
#     full_answer = html.unescape(full_answer_element.text) if full_answer_element else ''
#     short_answer = html.unescape(short_answer_element.text) if short_answer_element else ''  
#     short_answer = short_answer[0].upper()+short_answer[1:] if short_answer else short_answer
#     answer_list = ', '.join([html.unescape(item.text).split('.')[0] for item in answer_list_elements])
    
#     # print('t: '+title)
#     # print('fa: '+full_answer)
#     # print('l: '+link)
#     # print('sa: '+short_answer)
#     # print('al: '+answer_list) 
#     faq_dict = {
#         'question': question,
#         'link': link,
#         'title': title,
#         'answer': f'{short_answer}. \n {answer_list if answer_list else full_answer}'
#     }
#     # print(faq_dict)
#     # print('----------------------------')
#     faqs_list.append(faq_dict)
# # print(faqs_list)

def get_faqs_dict(question,root_element):    
    link_element = root_element.select_one('div.yuRUbf a') # link
    title_element = link_element.select_one('h3') # title
    full_answer_element = root_element.select_one('div.di3YZe') or root_element.select_one('span.hgKElc') # full answer
    short_answer_element = full_answer_element.select_one('b') # short answer
    answer_list_elements = root_element.select('div.di3YZe li') # answer in list

    question = question
    link = link_element['href'] if link_element else ''
    title = html.unescape(title_element.text) if title_element else ''
    full_answer = html.unescape(full_answer_element.text) if full_answer_element else ''
    short_answer = html.unescape(short_answer_element.text) if short_answer_element else ''  
    short_answer = short_answer[0].upper()+short_answer[1:] if short_answer else short_answer
    answer_list = ', '.join([html.unescape(item.text).split('.')[0] for item in answer_list_elements])

    faq_dict = {
        'question': question,
        'link': link,
        'title': title,
        'answer': f'{short_answer}. \n {answer_list+" ..." if answer_list else full_answer}'
    }    

    return faq_dict

page_source = driver.page_source
soup = BeautifulSoup(page_source,'lxml')
a = get_faqs_dict('Which part of Malaysia is the best?',soup.select_one('div.V3FYCf'))

time.sleep(1.5)

faqs_elements = soup.select('div[jsname="Cpkphb"]') # people also asked, each element    

question_element = faqs_elements[0].select_one('div[jsname="Cpkphb"] div.iDjcJe span') # question
question = html.unescape(question_element.text) if question_element else ''
b = get_faqs_dict(question,faqs_elements[0])

time.sleep(1.5)

question_element = faqs_elements[1].select_one('div[jsname="Cpkphb"] div.iDjcJe span') # question
question = html.unescape(question_element.text) if question_element else ''
c = get_faqs_dict(question,faqs_elements[1])

time.sleep(1.5)

question_element = faqs_elements[2].select_one('div[jsname="Cpkphb"] div.iDjcJe span') # question
question = html.unescape(question_element.text) if question_element else ''
d = get_faqs_dict(question,faqs_elements[2])

time.sleep(1.5)

print(a)
print('--------')
print(b)
print('--------')
print(c)
print('--------')
print(d)


# Back Up
# paa_section_element= driver.find_element(by=By.CSS_SELECTOR,value='div[jsname="Cpkphb"]')
# paa_section_element.click()
# first_faq = soup.select('div[jsname="Cpkphb"]') # people also asked, each element
# print(first_faq) 
# print('------------------------------------------------------------------------------------------')
# print(first_faq.select_one('div.yuRUbf a h3')) # 1st question
# print('------------------------------------------------------------------------------------------')
# print(first_faq .select_one('span.hgKElc')) # answer of 1st question    


# Pandas dataframe
# places_df = pd.read_csv('tourist_places.csv').fillna('')
# places_dict_list = places_df.to_dict('records')
# for place_dict in places_dict_list:
#     print(place_dict['place'])