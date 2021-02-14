import requests
import json
import os
import csv
import psycopg2
import datetime

def main():

    #company = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "TSLA", "BRK.A", "V", "WMT", "JNJ"]
    company = input("Enter Stock Ticker Symbol: $")
    getStockPrice(company)
    #for ticker in company:
    #    getStockPrice(ticker)

def getStockPrice(ticker:str):
    API_KEY = os.getenv("POLYGON_API_KEY")
    dataSet = []

    url = "https://api.polygon.io/v2/aggs/ticker/"+ ticker.upper() + "/range/5/minute/2013-02-16/2013-08-16?unadjusted=true&sort=asc&limit=50000&apiKey=" + API_KEY

    # headers for Polygon API request
    payload = {}
    headers = {}

    # make Polygon Aggregates (Bar) API request
    try:
        response = requests.request("GET", url, headers = headers, data = payload)
        db(response.text, ticker.upper())
    except Exception as e: print(e)
    except:
        print(response.status_code)
        print(response.raise_for_status)

def db(data:str, ticker:str):
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    print("Connected to " + conn.dsn)
    cur = conn.cursor()

    exists = '''SELECT EXISTS (SELECT FROM information_schema.tables WHERE  table_schema = 'josiel_project' AND table_name = ''' +  "'" + ticker.lower() + '''');'''

    cur.execute(exists)

    row = cur.fetchone()

    if (not row[0]):
        print("Table does not exists.")
        
        # Create table
        createSQL ='''
            CREATE TABLE josiel_project.''' + ticker.lower() + '''
        (
            tickerdate date NOT NULL,
            tickertime time without time zone NOT NULL,
            open numeric(9, 2),
            high numeric(9, 2),
            low numeric(9, 2),
            close numeric(9, 2),
            volume bigint,
            CONSTRAINT ''' + ticker.lower() + '''_pkey PRIMARY KEY (tickerdate, tickertime)
        );

            ALTER TABLE josiel_project.''' + ticker.lower() + '''
                OWNER to jkd5377;'''
        
        cur.execute(createSQL)
        conn.commit()
    else:
        print("Table does exist.")

    res = json.loads(data)

    for data in res['results']:
        timestamp = datetime.datetime.fromtimestamp((int(data['t'])/1000))
        tickerDate = timestamp.strftime("%x")
        tickerTime = timestamp.strftime("%X")
        # Create INSERT query
        sql = '''INSERT INTO josiel_project.''' + ticker.lower() + '''(tickerdate,tickertime,open,high,low,close,volume) VALUES( ''' + "'" + tickerDate + "','" + tickerTime + "'," + str(data['o']) + "," + str(data['h']) + "," + str(data['l']) + "," + str(data['c']) + "," + str(data['v']) + ''');'''
        print(tickerDate + " " + tickerTime)
        cur.execute(sql)
        conn.commit()
    conn.close()

if __name__ == '__main__':
    main()