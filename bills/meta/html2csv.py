from bs4 import BeautifulSoup
from pprint import pprint 
import re
import sys
import csv

from utils import check_dir
from settings import BASEURL, DIR, HTML_FIELDS
META_HEADERS = ["bill_id","status","title","link_id","proposer_type","proposed_date","decision_date","decision_result","has_summaries","status_detail"]

def get_elems(page, x):
    return page.xpath(x)

def html2csv(assembly_id, npages):
    # npages = 10
    
    def list_to_file(l, f):
        f.writerow(l)

    def parse_columns(columns):
        data = []
        for j, c in enumerate(columns):
            if j==1:
                p = re.compile(r"icon_(?P<name>\w+).gif")
                re_link = re.compile(r"fGoDetail\(\'(?P<bill_code>\w+)\'")
                status = p.search(str(c.find('img')['src'])).group('name')
                title = c.find('a').text.replace('"','\'').strip()
                link = re_link.search(str(c.find('a')['href'].strip())).group('bill_code')
                data.extend([status, title, link])

            elif j==6:
                data.append('1' if c.find('img') else '0')
            else:
                data.append(c.text.strip().replace('\n', ''))
        return data
    
    def parse_page(page, f, assembly_id):
        pn_html = open("1.html", 'r')
        bs = BeautifulSoup(pn_html, 'lxml')
        bills_table = bs.find('div', class_="tableCol01")
        bills = bills_table.find_all('tr')
        
        for r in reversed(bills):
            columns = r.find_all('td')
            p = parse_columns(columns)
            list_to_file(p, c)

        sys.stdout.write('%d\t' % page)
        sys.stdout.flush()

    directory = DIR['meta']
    check_dir(directory)
    meta_data = '%s/%d.csv' % (directory, assembly_id)

    # meta_data = './%s/%d.csv' % (directory, assembly_id)

    print ('\nParsing:')
    with open(meta_data, 'w+') as f:
        c = csv.writer(f, delimiter=',', 
                quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        list_to_file(META_HEADERS, c)
        for page in range(1, npages+1):
            parse_page(page, f, assembly_id)