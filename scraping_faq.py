import requests
import re
import pandas as pd
import html
import time 

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

STATE_N_FT = ['Kelantan','Pahang','Kedah','Sabah','Terengganu','Malacca','Negeri Sembilan','Perak','Perlis', 'Kuala Lumpur','Putrajaya','Labuan']
QUERY = ['Why is *place* popular?',
'What is *place* best known for?',
'What is *place* well known for?',
'What does *place* have?',
'What is so special about *place*?',
'Where can I take pictures in *place*?',
'Is *place* worth visiting?',
'What to do in *place*?',
'What do people do in *place*?',
'What activities we can do at *place*?',
'What is there to do in *place* at night?',
'How much is the entrance fee in *place*?',
'What is the most delicious food in *place*?',
'Which is the best month to visit *place*?',
'When is the best time to travel to *place*?',
'What is the best time to go *place*?',
'How many days do you need in *place*?',
'Is it safe to travel to *place*?',
'How to go to *place* by bus from *stateft*?',
'What is the cost-effective way to get from *stateft* to *place*?',
'How do I get from *stateft* to *place*?']

# Selenium Scraping setup
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# # options.add_argument('--headless')
# driver = webdriver.Chrome("C:\PythonDevelopment\chromedriver", chrome_options=options)

options = Options()
options.set_preference("browser.privatebrowsing.autostart", True)
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')
service = Service(r"C:\Users\666\Downloads\FirefoxDriver.exe")
driver = Firefox(service=service, options=options)

faqs_list = []

def get_page_source():
    # parse whole page source to use BeautifulSoup to scrape    
    return BeautifulSoup(driver.page_source,'lxml')

def append_to_faqs_list(faq_dict):
    if faq_dict:
        faqs_list.append(faq_dict)

def expand_faq(find_faq_elements_func):            
    elements_to_expand = find_faq_elements_func()    
    print(f'elements to expand:: {elements_to_expand}')

    if elements_to_expand:
        # print(len(elements_to_expand))
        for element in elements_to_expand:                
            # try:
                webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
                time.sleep(0.5)
                print('expand element')
                # element.click()
            # except:        
            #     print('whats wrong')
                time.sleep(2)    
        return True
    else:
        return False


def find_faq_elements():
    try:        
        return WebDriverWait(driver, 8).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[jsname="Cpkphb"]')))                                    
    except TimeoutException or NoSuchElementException:
        print("Loading took too much time!")
        return None

def get_faqs_dict(question,root_element):    
    print(question)
    try:
        link_element = root_element.select_one('div.yuRUbf a') or root_element.select_one('div.g div.yuRUbf a') # link    
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
        next_line = '\n'
        faq_dict = {
            'question': question,
            'link': link,
            'title': title,
            'answer': f'{short_answer + ". "+next_line if short_answer else ""} {answer_list+" ..." if answer_list else full_answer}'
        }    

        return faq_dict 
    except:
        print('cant get faqs dict')

def scaping_other_faqs():
    # click to expand the faq so that generate more faq
    is_other_faq_exist = expand_faq(find_faq_elements) 
    if is_other_faq_exist:
        print('finished expand element')   
        
        faqs_elements = get_page_source().select('div[jsname="Cpkphb"]') # people also asked, each element    
        print(f'faqs elements: {len(faqs_elements)}')
        for faqs_element in faqs_elements:       
            question_element = faqs_element.select_one('div[jsname="Cpkphb"] div.iDjcJe span') # question        
            question = html.unescape(question_element.text) if question_element else ''        
            faq_dict = get_faqs_dict(question, faqs_element)         
            append_to_faqs_list(faq_dict)    

def scraping_faqs(query):        
    driver.get(f"https://www.google.com.my/search?q={query}&")        

    page_source = get_page_source() 

    if page_source.select_one('div#recaptcha'):
        raise KeyboardInterrupt('recaptcha catached')

    try:
        suggested_ans_element = page_source.select_one('div.V3FYCf')    
        faq_dict = get_faqs_dict(query, suggested_ans_element)
        append_to_faqs_list(faq_dict)
    except:
        print('dont have any suggested answer')

    scaping_other_faqs()
    

places_df = pd.read_csv('tourist_places.csv').fillna('')
places_dict_list = places_df.to_dict('records')
query_index_stopped = 0
place_index_stopped = 0
with open('index_stopped.txt', 'r') as f:
    txt = f.read()
    if txt:
        list = txt.split(',')
        query_index_stopped = int(list[0])
        place_index_stopped = int(list[1])

try:
    for query_index, query  in enumerate(QUERY[query_index_stopped:]):    
        for place_index, place_dict in enumerate(places_dict_list[place_index_stopped:]):
            replaced_query = query.replace('*place*',place_dict['place'])            
            if re.search('\*stateft\*',query):
                # print('searched STATE AND FT.........')
                for state_n_ft in STATE_N_FT:
                    replaced_query2 = replaced_query.replace('*stateft*',state_n_ft)
                    # print(replaced_query2)
                    try:
                        scraping_faqs(replaced_query2)
                    except:
                        print(f'cant fetch this query2: {replaced_query2}')
                        with open("index_stopped.txt", "w") as f:
                            f.write(f'{query_index+query_index_stopped},{place_index+place_index_stopped}')
                        raise KeyboardInterrupt('Manual Interrupt for scraping faq 2')
            else:
                try:
                    # print(replaced_query)
                    scraping_faqs(replaced_query)                            
                except:
                    print(f'cant fetch this query: {replaced_query}')
                    with open("index_stopped.txt", "w") as f:
                        f.write(f'{query_index+query_index_stopped},{place_index+place_index_stopped}')
                    raise KeyboardInterrupt('Manual Interrupt for scraping faq 1')
            # print(faqs_list)
            print(len(faqs_list))
except KeyboardInterrupt:
    print('KeyboardInterrupt')
    

try:
    faqs_df = pd.DataFrame(faqs_list)
    print(faqs_df)
    faqs_df.to_csv('faqs.csv', mode='a', index=False)
except:
    print(faqs_list)