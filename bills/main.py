
import meta
import os
import utils
# import specific
# import pdf
import re
import math
import sys

from selenium import webdriver
from settings import BASEURL, DIR, HTML_FIELDS, PAGE_SIZE
from utils import check_dir, get_webpage_text, get_webpage
from meta import get_list_html, get_npages, html2csv
from specific import html2json


assembly_s, assembly_e = 20, 20 # start, end id of assembly
bill_s, bill_e = None, None     # start, end number of bill

assembly_e = 20

## for PhantomJS
# driver = webdriver.PhantomJS('/Users/beomi/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
# url = "http://likms.assembly.go.kr/bill/BillSearchSimple.do"

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--disable-gpu")
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

# options.binary_location = os.getcwd()

# driver = webdriver.Chrome('/Users/donggeunyi/backup_by_dong/PycharmProjects/new-crawlers/chromedriver')
# driver.get(url)

# driver.find_element_by_xpath("//select[@name='ageFrom']/option[@value='{}']".format(assembly_s)).click()
# driver.find_element_by_xpath("//select[@name='ageTo']/option[@value='{}']".format(assembly_e)).click()
# driver.find_element_by_css_selector('.mt20 > button.btnd:nth-child(1)').click()

# driver.implicitly_wait(1)
# driver.find_element_by_xpath("//select[@id='pageSizeOption']/option[@value='{}']".format(PAGE_SIZE)).click()
# driver.implicitly_wait(1)

a = 20
npages = 495
# npages = get_npages(driver)
# meta.get_list_html(driver, a, npages)
# meta.html2csv(a, npages)

html2json(a, range=(bill_s, bill_e))