import requests
import json
import os
import csv
import psycopg2
import datetime

def main():

    #company = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "TSLA", "BRK.A", "V", "WMT", "JNJ"]
    #for ticker in company:
    #    getStockPrice(ticker)
    company = input("Enter Stock Ticker Symbol: $")
    getStockPrice(company)

def getStockPrice(ticker:str):

    API_KEY = os.getenv("POLYGON_API_KEY")

    # Quartley requests
    tslaDates = [
        {"start":"2013-07-17","end":"2013-10-17"},
        {"start":"2013-10-17","end":"2014-01-17"},
        {"start":"2014-01-17","end":"2014-04-17"},
        {"start":"2014-04-17","end":"2014-07-17"},
        {"start":"2014-07-17","end":"2014-10-17"}
    ]

    for dates in tslaDates:
        print("Starting the " + dates['start'] + " batch")

        # Build API URL
        url = "https://api.polygon.io/v2/aggs/ticker/"+ ticker.upper() + "/range/5/minute/" + dates['start'] + "/" + dates['end'] + "?unadjusted=true&sort=asc&limit=50000&apiKey=" + API_KEY

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

    # Create SQL code to see if table for ticker exist
    exists = '''SELECT EXISTS (SELECT FROM information_schema.tables WHERE  table_schema = 'josiel_project' AND table_name = ''' +  "'" + ticker.lower() + '''');'''
    cur.execute(exists)
    row = cur.fetchone()

    # Check if table exist
    if (not row[0]):
        print("Table does not exist.")
        
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

    # Convert JSON text into JSON object
    res = json.loads(data)
    print("Starting insert statements")

    # Loop through all items within JSON object and insert into database.schema.table
    for data in res['results']:
        timestamp = datetime.datetime.fromtimestamp((int(data['t'])/1000))

        # Create INSERT query
        sql = '''INSERT INTO josiel_project.''' + ticker.lower() + '''(tickerdate,tickertime,open,high,low,close,volume) VALUES( ''' + "'" + datetime.datetime.fromtimestamp((int(data['t'])/1000)).strftime("%x") + "','" + datetime.datetime.fromtimestamp((int(data['t'])/1000)).strftime("%X") + "'," + str(data['o']) + "," + str(data['h']) + "," + str(data['l']) + "," + str(data['c']) + "," + str(data['v']) + ''');'''
        cur.execute(sql)
        conn.commit()

    conn.close()

if __name__ == '__main__':
    main()