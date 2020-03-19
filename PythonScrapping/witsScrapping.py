from __future__ import print_function, division
import os
import requests
from bs4 import BeautifulSoup as Soup
from requests_html import HTMLSession
import ssl
import certifi
# declare a session object
session = HTMLSession()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/78.0.3904.108 Safari/537.36'
headers = {'User-Agent': user_agent}

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

responseHTML = session.get(
    'https://wits.worldbank.org/trade/comtrade/en/country/ALL/year/2018/tradeflow/Exports/partner/WLD/product/030270#', headers=headers, cert=certifi.where())
soup = Soup(responseHTML.content, 'html5lib')
f = open("result.txt", "a")
f.write(str(soup))
# f.write(str(responseHTML.html.xpath('//*[@id="productTitle"]//text()')))
f.close()
