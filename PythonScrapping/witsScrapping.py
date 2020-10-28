from __future__ import print_function, division
from requests_html import HTMLSession
import pandas as pd
import pyodbc as db
import re
from multireplace import multireplace
import urllib3
import pycountry
import time
import logging
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15


def callWITS(session, headers, country,  product, filterMap):
    '''
    Function to scrap data from the World Integrated Trade Solution which returns a dataframe
    The result is filtered for key words as SELECT, DROP, DATABASE, LOGIN

    Params:

    session - Initialized HTMLSession to make requests

    country - Reporter involved in the trade

    year -  year in which the trade happened

    type -  Imports/Exports

    partner - Partner in the trade

    product - Product code HS 6 digit

    filterMap - Keywords to replace

    Returns: a dataframe from the table queried
    '''

    # The verify is a huge problem
    try:
        responseHTML = session.get(
            'http://wits.worldbank.org/trade/comtrade/en/country/' + country + '/year/2018/tradeflow/Exports/partner/ALL/product/' + product + '#', headers=headers, verify=False)
        # read html makes a list of dataframes out of the tables and we have only a table, so we return that
        df = pd.read_html(multireplace(str(responseHTML.content),
                                       filterMap, ignore_case=True), header=0)[0]
        if 'Partner' in df.columns:
            return df[(df['Partner'] != 'World') & (df['Partner'] != 'Other Asia, nes')]
    except Exception as e:
        logging.error(e)


def makeConnection(server, database, username, password):
    '''
    Function to establish connection to DB

    Params:

    server - server adress

    database - database name

    username - username for SQL Auth

    password - password for SQL Auth

    Returns: Connection Object and Cursor Object
    '''
    connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                            server+';DATABASE='+database+';UID='+username+';PWD=' + password, trusted_connection='yes')
    cursor = connection.cursor()
    return connection, cursor


def writeToDB(connection, cursor, df, country, product):
    '''
    Function to create a connection and write to DB
    It uses paramized queries to protect from SQL Injection

    Params:

    server - server adress

    database - database name

    username - username for SQL Auth

    password - password for SQL Auth
    '''
    try:
        sql_insert_query = """ INSERT INTO TradeLine
                                       (ProductID,DateID,ReporterID,PartnerID,QTY,Amount) VALUES (?,?,?,?,?,?)"""
        print(df)
        for index, row in df.iterrows():
            if 'East Timor' in row['Partner']:
                result = pycountry.countries.search_fuzzy(
                    'timor')
            else:
                result = pycountry.countries.search_fuzzy(
                    row['Partner'].partition(",")[0])
            insert_tuple = (product, '2018-01-01',
                            country, result[0].alpha_2, row['Quantity'], row['Trade Value 1000USD'])
            cursor.execute(sql_insert_query, insert_tuple)
            connection.commit()
    except db.DatabaseError as error:
        logging.error(error)


def getCountries(cursor):
    cursor.execute(
        "SELECT * FROM[python_db].[dbo].[Country] where name in ('DENMARK', 'ROMANIA', 'GERMANY', 'CHINA','JAPAN','UNITED STATES','BRAZIL','RUSSIAN FEDERATION','UNITED KINGDOM','AUSTRALIA','SAUDI ARABIA','SOUTH AFRICA')")
    return cursor.fetchall()


def getProducts(cursor):
    cursor.execute(
        "SELECT * FROM[python_db].[dbo].[Product] WHERE LEN(ProductID) = 6")
    return cursor.fetchall()


if __name__ == "__main__":
    # declare a session object
    logging.basicConfig(filename='example.log', level=logging.ERROR)
    session = HTMLSession()
    urllib3.disable_warnings()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/78.0.3904.108 Safari/537.36'}
    filterMap = {"SELECT": "", "DROP": "", "DATABASE": "",
                 "INSERT": "", "DELETE": "", "AUTHORIZATION": ""}
    server = '(local)'
    database = 'python_db'
    username = 'pynative'
    password = 'toor'
    connection, cursor = makeConnection(
        server, database, username, password)
    '''try:'''
    for country in getCountries(cursor):
        for product in getProducts(cursor):
            df = callWITS(session, headers,
                          country[3], product[0], filterMap)
            if df is not None:
                if len(df) != 0:
                    writeToDB(connection, cursor, df, country[0], product[0])
    '''except Exception as e:
        logging.error(e)
    finally:
        session.close()
        cursor.close()
        connection.close()
        print("SQL connection is closed")'''
