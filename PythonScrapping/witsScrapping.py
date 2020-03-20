from __future__ import print_function, division
import os
import requests
from bs4 import BeautifulSoup as Soup
from requests_html import HTMLSession
import ssl
import certifi
import pandas as pd


def callWITS(session, country, year, type, partner, product):
    '''
    Function to scrap data from the World Integrated Trade Solution which returns a dataframe

    Params:

    session - Initialized HTMLSession to make requests

    country - Reporter involved in the trade

    year -  year in which the trade happened

    type -  Imports/Exports

    partner - Partner in the trade

    product - Product code HS 6 digit

    Returns: a dataframe from the table queried 
    '''

    # The verify is a huge problem
    responseHTML = session.get(
        'https://wits.worldbank.org/trade/comtrade/en/country/' + country + '/year/' + year + '/tradeflow/' + type + '/partner/' + partner + '/product/' + product + '#', headers=headers, verify=False)
    # read html makes a list of dataframes out of the tables and we have only a table, so we return that
    return pd.read_html(responseHTML.content, header=0)[0]


if __name__ == "__main__":
    # declare a session object
    session = HTMLSession()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/78.0.3904.108 Safari/537.36'
    headers = {'User-Agent': user_agent}
    df = callWITS(session=session, country='ALL', partner='WLD',
                  year='2018', type='Exports', product='030270')
    print(df.head())
