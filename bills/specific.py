#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
from operator import itemgetter
import requests
import json

from pprint import pprint
from utils import check_dir, get_webpage_text, get_webpage
from settings import BASEURL, DIR, HTML_FIELDS

def get_metadata(assembly_id, range=(None, None)):
    with open('./%s/%d.csv' % (DIR['meta'], assembly_id), 'r') as f:
        data = []
        for row in f.readlines():
            items = [item.strip('"') for item in row.split('","')]
            if len(items) < 8:
                continue
            data.append((items[0], items[3], items[8]))
    meta = {}
    for d in data:
        meta[d[0]] = (d[1], d[2])
    return meta

def get_page(assembly_id, bill_id, link_id, field):
    url = '%s%s' % (BASEURL[field], link_id)
    outp = '%s/%s/%s.html' % (DIR[field], assembly_id, bill_id)

    i = 0
    while i==0 or ('TEXTAREA ID="MSG" STYLE="display:none"' in doc and i<10):
        try:
            doc = get_webpage_text(url)
        except requests.exceptions.RequestException:
            continue
        i += 1
    with open(outp, 'w+') as f:
        f.write(doc)    

def get_specifics(assembly_id, bill_id, link_id):
    if assembly_id > 16:
        baseurl = BASEURL['specifics']
    outp = '%s/%s/%s.html' % (DIR['specifics'], assembly_id, bill_id)
    url = '%s%s' % (baseurl, link_id)
    get_webpage(url, outp)

def get_summaries(assembly_id, bill_id, link_id, has_summaries):
    outp = '%s/%s/%s.html' % (DIR['summaries'], assembly_id, bill_id)
    try:
        get_webpage('%s%s' % (BASEURL['summaries'], link_id), outp)
    except:
        pass

def get_html(assembly_id=None, range=(None, None), bill_ids=None):
    assembly_id = 20
    range=(0, 1)
    if bill_ids is not None and not bill_ids:
        return
    for field in HTML_FIELDS:
        utils.check_dir('%s/%s' % (DIR[field], assembly_id))
    metadata = get_metadata(assembly_id, range=range)

    for bill_id in metadata:
        if bill_id == 'bill_id':
            continue
        if bill_ids and bill_id not in bill_ids:
            continue
        link_id, has_summaries = metadata[bill_id]
        for field in HTML_FIELDS[1:3]:
            get_page(assembly_id, bill_id, link_id, field)
            
        get_specifics(assembly_id, bill_id, link_id)
        get_summaries(assembly_id, bill_id, link_id, has_summaries)

        sys.stdout.write('%s\t' % bill_id)
        sys.stdout.flush()
get_html()