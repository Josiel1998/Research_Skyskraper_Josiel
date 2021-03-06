import requests
import json
import os
import psycopg2
import itertools
from dotenv import dotenv_values

# load secret environment variables
config = dotenv_values(".env")
 
def main():
    getStockPrice()
 
def getStockPrice():
 
    API_KEY = config['POLYGON_API']

 
    # headers for Polygon API request
    payload = {}
    headers = {}
 
    # make Tickers API request
    try:
        for i in itertools.count(start=1):
            # Build API URL and iterate numbers starting from 1
            url = '''https://api.polygon.io/v2/reference/tickers?sort=ticker&perpage=50&page=''' + str(i) + '''&apiKey=''' + API_KEY
            response = requests.request("GET", url, headers = headers, data = payload)
            if(response.status_code == 200):
                db(response, i)
    except Exception as e: print(e)
    except:
        print(response.status_code)
        print(response.raise_for_status)
 
def db(data:str, page:int):

    # Make database connection
    conn = psycopg2.connect(database = config['DBNAME'], user = config['DBUSER'], password = config['DBPASSWORD'], host = config['DBHOST'], port = config['DBPORT'])
    cur = conn.cursor()

    # Convert JSON text into JSON object
    res = json.loads(data.text)

    for security in res['tickers']:
        activeStr = str(security['active'])
        # remove apostrophe
        nameStr = security['name'].replace("'","")

        if security['active']:
            try:
                # Create INSERT query for active exchanges with all fields
                sql = '''INSERT INTO tickers.ticker(ticker, name, active, exchange, currency, market) VALUES( ''' + "'" + security['ticker'].lower() + "','" + nameStr + "','" + activeStr + "','" + security['primaryExch'] + "','" + security['currency'] + "','" + security['market'] + "'" + ''');'''
            except:
                # Create INSERT query for active exchanges with no exchange
                sql = '''INSERT INTO tickers.ticker(ticker, name, active, exchange, currency, market) VALUES( ''' + "'" + security['ticker'].lower() + "','" + nameStr + "','" + activeStr + "','" + "" + "','" + security['currency'] + "','" + security['market'] + "'" + ''');'''
        else:
            # Create INSERT query for non-active exchanges
            sql = '''INSERT INTO tickers.ticker(ticker, name, active, exchange, currency, market) VALUES( ''' + "'" + security['ticker'].lower() + "','" + nameStr + "','" + activeStr + "','" + "" + "','" + security['currency'] + "','" + security['market'] + "'" + ''');'''
        cur.execute(sql)
        conn.commit()
        print(nameStr + " commited, on page " + str(page))
 
    conn.close()
 
if __name__ == '__main__':
    main()