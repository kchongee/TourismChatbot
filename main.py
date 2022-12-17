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

# place_finding = re.findall(r"\*place\*",qry)
qry.replace('*stateft*',state_n_ft)
qry.replace('*place*',place)


URL = f"https://www.google.com/search?q={QUERY[0]}&"

# print(URL)
# html_page = requests.get(URL).text
# print(html_page)
# soup = BeautifulSoup(html_page, 'html.parser')
# soup = BeautifulSoup(html_page, 'lxml')
# print('------------------------------------------------------------------------------------------')

# google_ans = soup.find_all('h1.Uo8X3b')
# # print(google_ans)
# for ans in google_ans:
#     # print(ans.getText())
#     print(ans)
#     print('------------')

# chrome_driver_path = "C:\PythonDevelopment\chromedriver"
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("C:\PythonDevelopment\chromedriver", chrome_options=options)
driver.get(f"https://www.google.com.my/search?q={QUERY[0]}")    
# first_weblink = driver.find_element(by=By.TAG_NAME,value="h3")
# print(first_weblink)
page_source = driver.page_source
soup = BeautifulSoup(page_source,'lxml')
# print(soup.select('div.V3FYCf')) # suggested answer
# print(soup.select('div.Wt5Tfe')) # people also asked
first_faq = soup.select('div[jsname="Cpkphb"]')[0]
print(first_faq) # people also asked, 1st question section
print('------------------------------------------------------------------------------------------')
print(first_faq.select_one('div.yuRUbf a h3')) # 1st question
print('------------------------------------------------------------------------------------------')
print(first_faq .select_one('span.hgKElc')) # answer of 1st question
