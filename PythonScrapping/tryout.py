from __future__ import print_function, division
from requests_html import HTMLSession
import pandas as pd
import pyodbc as db
import re
from multireplace import multireplace
import urllib3
import pycountry
if __name__ == "__main__":
    filterMap = {"SELECT": "", "DROP": "", "DATABASE": "",
                 "INSERT": "", "DELETE": "", "AUTHORIZATION": ""}
    session = HTMLSession()
    urllib3.disable_warnings()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/78.0.3904.108 Safari/537.36'}
    server = '(local)'
    database = 'python_db'
    username = 'pynative'
    password = 'toor'
    connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                            server+';DATABASE='+database+';UID='+username+';PWD=' + password, trusted_connection='yes')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM[python_db].[dbo].[Country] where name in ('DENMARK', 'ROMANIA', 'GERMANY', 'SWEDEN')")
    countries = cursor.fetchall()
    cursor.execute(
        "SELECT TOP(3) * FROM[python_db].[dbo].[Product] WHERE ProductID in ('020110')")
    products = cursor.fetchall()
    for country in countries:
        for product in products:
            responseHTML = session.get(
                'http://wits.worldbank.org/trade/comtrade/en/country/' + country[3] + '/year/2018/tradeflow/Exports/partner/ALL/product/' + product[0] + '#', headers=headers, verify=False)

            df = pd.read_html(multireplace(str(responseHTML.content),
                                           filterMap, ignore_case=True), header=0)[0]
            df = df[df['Partner'] != 'World']
            sql_insert_query = """ INSERT INTO TradeLine
                                       (ProductID,DateID,ReporterID,PartnerID,QTY,Amount) VALUES (?,?,?,?,?,?)"""
            for index, row in df.iterrows():
                result = pycountry.countries.search_fuzzy(
                    row['Partner'])
                insert_tuple = (product[0], '2018-01-01',
                                country[0], result[0].alpha_2, int(row['Quantity']), row['Trade Value 1000USD'])
                cursor.execute(sql_insert_query, insert_tuple)
                connection.commit()
    cursor.close()
    connection.close()
