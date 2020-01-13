import requests
import os 
import html5lib

# ===== for utils 
HEADERS = {
    'Referer': 'http://likms.assembly.go.kr/bill/BillSearchResult.do',
}

s = requests.Session()

def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_webpage_text(url):
    r = s.get(url, headers=HEADERS, stream=True)
    content = r.content.decode('utf-8')
    return content

def get_webpage(url, outp):
    try:
        r = s.get(url, headers=HEADERS, stream=True)
        assert r.ok
    except (requests.exceptions.RequestException, AssertionError) as e:
        import sys
        traceback.print_exc(file=sys.stdout)
        return
    with open(outp, 'wb') as f:
        for block in r.iter_content(1024):
            if not block:
                break
            f.write(block)

def read_webpage(filename):
    with open(filename) as f:
        page = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)
        p = page.parse(f)
    return p

def get_elems(page, x):
    return page.xpath(x)