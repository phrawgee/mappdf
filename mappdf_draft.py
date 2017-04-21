import re
import requests
from urlparse import urlparse
from bs4 import BeautifulSoup

def getTextFromUrl(url):
    # Http GET request to website
    resp = None
    try:
        resp = requests.get(url)
    except:
        # invalid url
        return ''
    # read response text
    html_doc = resp.text
    # use beautifulsoup to parse response text as html/xml tree
    parsed_html = BeautifulSoup(html_doc, 'html.parser')
    # get body tag from parsed html
    page_body = parsed_html.find('body')
    if page_body:
        # Strip script and style tags
        # source:
        #   http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
        # kill all script and style elements
        for script in page_body(["script", "style"]):
            script.extract()    # rip it out
        # get text
        text = page_body.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        # return site text
        return text.encode('utf-8')
    return ''


website_url = 'https://library.uoregon.edu/map/gis_data/data_in_commons.html'
base_domain = 'https://library.uoregon.edu'

# Http GET request to website
resp = requests.get(website_url)

# read response text
html_doc = resp.text

# parsed html
parsed_html = BeautifulSoup(html_doc, 'html.parser')

# all links on page
pages = {}
for link in parsed_html.find_all('a'):
    link = link.get('href')
    if link:
        if 'http' not in link:
            # handle relative links
            link = base_domain + link
        print(link)
        # print(urlparse(link))
        pages[link] = getTextFromUrl(link)


print(pages)
