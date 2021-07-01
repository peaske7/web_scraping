"""
My first project using Selenium instead of scrapy-splash.
This project is from Jay M Patel's Getting Structured Data from the Internet
"""
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

test_url = '''https://web.archive.org/web/20200406193325/https://www.fda.gov/
inspections-compliance-enforcement-and-criminal-investigations/compliance-
actions-and-activities/warning-letters'''

option = webdriver.ChromeOptions()
option.add_argument('--incognito')
chromedriver = '/Users/shimadaharuki/chromedriver'
browser = webdriver.Chrome(chromedriver, options=option)
browser.get(test_url)

time.sleep(20)

element = browser.find_element_by_xpath('//*[@id="DataTables_Table_0_length"]/label/select')
select = Select(element)

# select by visible text
select.select_by_visible_text('All')

time.sleep(20)

posted_date_list = []
letter_issue_list = []
warning_letter_url = []
company_name_list = []
issuing_office_list = []

soup_level1 = BeautifulSoup(browser.page_source, 'lxml')

for tr in soup_level1.find_all('tr')[1:]:
    tds = tr.find_all('td')
    posted_date_list.append(tds[0].text)
    letter_issue_list.append(tds[1].text)
    warning_letter_url.append(tds[2].find('a')['href'])
    company_name_list.append(tds[2].text)
    issuing_office_list.append(tds[3].text)
browser.close()

df = pd.DataFrame({
    'posted_date': posted_date_list,
    'letter_issue': letter_issue_list,
    'warning_letter_url': warning_letter_url,
    'company_name': company_name_list,
    'issuing_office': issuing_office_list
})
df.to_json('warning_letters.json')
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)
df.head()
