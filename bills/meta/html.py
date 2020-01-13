#! /usr/bin/python3.6
# -*- coding: utf-8 -*-

import os
import re
import sys
import math

# import gevent
# from gevent import monkey; monkey.patch_all()
import requests
import utils
from settings import BASEURL, DIR, HTML_FIELDS, PAGE_SIZE

def convert(assembly_id):
    directory = '%s/%s' % (DIR['list'], assembly_id)
    return directory

def get_npages(driver):    
    nbills_o = str(driver.find_element_by_css_selector('p.textType01 > span').text.strip())
    m = re.search(u'총([A-Z0-9,]+)건이 검색되었습니다.', nbills_o)
    nbills = int(m.group(1).replace(',', ''))
    npages = int(math.ceil(nbills/float(PAGE_SIZE)))
    print ("Total {} bills, total pages {} ".format(nbills, npages))
    return npages

# def get_list_html(a, npages):
#     html = driver.page_source
#     pn = npages - page + 1
#     fn = '%s/%d.html' % (directory, pn)
#     is_first = True
    
#     while is_first or 'TEXTAREA ID="MSG" STYLE="display:none"' in doc:
        
#         is_first = False
#     fn = '{}.html'.format(1)
#     with open(fn, 'w') as f:
#         f.write(html)

def get_list_html(driver, assembly_id, npages):

    def get_page(baseurl, page, directory, npages):
        try:
            # driver.find_element_by_css_selector('.mt20 > button.btnd:nth-child(1)').click()
            driver.execute_script("javascript:GoPage({})".format(page))
            # pn = npages - page + 1
            pn = page
            fn = '%s/%d.html' % (directory, pn)
            is_first = True

            doc = driver.page_source
            is_first = False

            with open(fn, 'w') as f:
                f.write(doc)

            sys.stdout.write('%s\t' % pn)
            sys.stdout.flush()

        except (requests.exceptions.RequestException, IOError) as e:
            print ('\nFailed to get %s due to %s' % (fn, e.__repr__))

    directory = convert(assembly_id)
    utils.check_dir(directory)
    
    print ('Download Start')
    for np in range(1,npages+1):
        print ('Downloading:' + str(np) + '...' )
        get_page(BASEURL, np, directory, npages)
    
    
    return npages