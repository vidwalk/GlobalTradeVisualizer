
import unittest
from witsScrapping import makeConnection, callWITS, writeToDB
import pyodbc
import urllib3
from requests_html import HTMLSession


class TestScrappingMethods(unittest.TestCase):
    def testConnectionToSource(self):
        session = HTMLSession()
        urllib3.disable_warnings()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/78.0.3904.108 Safari/537.36'}
        filterMap = {"SELECT": "", "DROP": "", "DATABASE": "",
                     "INSERT": "", "DELETE": "", "AUTHORIZATION": ""}
        callWITS(session, headers,
                 'DNK', '20110', filterMap)

    def testDatabaseConnection(self):
        server = '(local)'
        database = 'python_db'
        username = 'pynative'
        password = 'toor'
        makeConnection(server, database, username, password)

    def testDatabaseThrowError(self):
        server = '(local)'
        database = 'unavailable'
        username = 'pynative'
        password = 'toor'
        with self.assertRaises(pyodbc.InterfaceError):
            makeConnection(server, database, username, password)

    def testExtractTradeLines(self):
        server = '(local)'
        database = 'python_db'
        username = 'pynative'
        password = 'toor'
        session = HTMLSession()
        urllib3.disable_warnings()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/78.0.3904.108 Safari/537.36'}
        filterMap = {"SELECT": "", "DROP": "", "DATABASE": "",
                     "INSERT": "", "DELETE": "", "AUTHORIZATION": ""}
        connection, cursor = makeConnection(
            server, database, username, password)
        df = callWITS(session, headers,
                      'DNK', '020110', filterMap)
        writeToDB(connection, cursor, df, 'DK', '020110')


if __name__ == '__main__':
    unittest.main()
