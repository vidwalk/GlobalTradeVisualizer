from __future__ import print_function, division
from requests_html import HTMLSession
import pandas as pd
import pyodbc as db
import re
from multireplace import multireplace
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15


def callWITS(session, country, year, type, partner, product, filterMap):
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
    responseHTML = session.get(
        'https://wits.worldbank.org/trade/comtrade/en/country/' + country + '/year/' + year + '/tradeflow/' + type + '/partner/' + partner + '/product/' + product + '#', headers=headers, verify=False)
    # read html makes a list of dataframes out of the tables and we have only a table, so we return that

    return pd.read_html(multireplace(str(responseHTML.content), filterMap, ignore_case=True), header=0)[0]


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


def writeToDB(server, database, username, password):
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
        connection, cursor = makeConnection(
            server, database, username, password)
        try:
            sql_insert_query = """ INSERT INTO testTable
                                   (test1) VALUES (?)"""
            insert_tuple = (2)
            cursor.execute(sql_insert_query, insert_tuple)
            connection.commit()
        except db.DatabaseError as error:
            print("parameterized query failed {}".format(error))
        finally:
            cursor.close()
            connection.close()
            print("SQL connection is closed")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # declare a session object
    session = HTMLSession()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/78.0.3904.108 Safari/537.36'
    headers = {'User-Agent': user_agent}
    filterMap = {"SELECT": "", "DROP": "", "DATABASE": "",
                 "INSERT": "", "DELETE": "", "AUTHORIZATION": ""}
    df = callWITS(session=session, country='ALL', partner='WLD',
                  year='2018', type='Exports', product='030270', filterMap=filterMap)
    print(df.head())
    server = '(local)'
    database = 'python_db'
    username = 'pynative'
    password = 'toor'
    writeToDB(server, database, username, password)
