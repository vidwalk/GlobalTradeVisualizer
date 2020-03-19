from __future__ import print_function, division
import os
import requests
from bs4 import BeautifulSoup as Soup
from requests_html import HTMLSession
import ssl
import certifi
import pandas as pd
# declare a session object
session = HTMLSession()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/78.0.3904.108 Safari/537.36'
headers = {'User-Agent': user_agent}

# The verify is a huge problem
responseHTML = session.get(
    'https://wits.worldbank.org/trade/comtrade/en/country/ALL/year/2018/tradeflow/Exports/partner/WLD/product/030270#', headers=headers, verify=False)
soup = Soup(responseHTML.content, 'html5lib')
#f = open("result.txt", "a")
# f.write()
# f.write(str(responseHTML.html.xpath('//*[@id="productTitle"]//text()')))
# f.close()
print(pd.read_html(responseHTML.content, header=0))
