import requests
import json
import os
import psycopg2
import datetime

def main():

    #company = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "TSLA", "BRK.A", "V", "WMT", "JNJ"]
    #for ticker in company:
    #    getStockPrice(ticker)
    #company = input("Enter Stock Ticker Symbol: $")

    company = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "BRK.A", "V", "WMT", "JNJ"]
    for ticker in company:
        getStockPrice(ticker)

def getStockPrice(ticker:str):

    API_KEY = os.getenv("POLYGON_API_KEY")

    # Quartley requests
    tgtDates = [
        {"start":"2005-01-01","end":"2005-03-31"},
        {"start":"2005-04-01","end":"2005-06-30"},
        {"start":"2005-07-01","end":"2005-09-30"},
        {"start":"2005-10-01","end":"2005-12-31"},

        {"start":"2006-01-01","end":"2006-03-31"},
        {"start":"2006-04-01","end":"2006-06-30"},
        {"start":"2006-07-01","end":"2006-09-30"},
        {"start":"2006-10-01","end":"2006-12-31"},

        {"start":"2007-01-01","end":"2007-03-31"},
        {"start":"2007-04-01","end":"2007-06-30"},
        {"start":"2007-07-01","end":"2007-09-30"},
        {"start":"2007-10-01","end":"2007-12-31"},

        {"start":"2008-01-01","end":"2008-03-31"},
        {"start":"2008-04-01","end":"2008-06-30"},
        {"start":"2008-07-01","end":"2008-09-30"},
        {"start":"2008-10-01","end":"2008-12-31"},

        {"start":"2009-01-01","end":"2009-03-31"},
        {"start":"2009-04-01","end":"2009-06-30"},
        {"start":"2009-07-01","end":"2009-09-30"},
        {"start":"2009-10-01","end":"2009-12-31"},

        {"start":"2010-01-01","end":"2010-03-31"},
        {"start":"2010-04-01","end":"2010-06-30"},
        {"start":"2010-07-01","end":"2010-09-30"},
        {"start":"2010-10-01","end":"2010-12-31"},

        {"start":"2011-01-01","end":"2011-03-31"},
        {"start":"2011-04-01","end":"2011-06-30"},
        {"start":"2011-07-01","end":"2011-09-30"},
        {"start":"2011-10-01","end":"2011-12-31"},

        {"start":"2012-01-01","end":"2012-03-31"},
        {"start":"2012-04-01","end":"2012-06-30"},
        {"start":"2012-07-01","end":"2012-09-30"},
        {"start":"2012-10-01","end":"2012-12-31"},

        {"start":"2013-01-01","end":"2013-03-31"},
        {"start":"2013-04-01","end":"2013-06-30"},
        {"start":"2013-07-01","end":"2013-09-30"},
        {"start":"2013-10-01","end":"2013-12-31"},

        {"start":"2014-01-01","end":"2014-03-31"},
        {"start":"2014-04-01","end":"2014-06-30"},
        {"start":"2014-07-01","end":"2014-09-30"},
        {"start":"2014-10-01","end":"2014-12-31"},

        {"start":"2015-01-01","end":"2015-03-31"},
        {"start":"2015-04-01","end":"2015-06-30"},
        {"start":"2015-07-01","end":"2015-09-30"},
        {"start":"2015-10-01","end":"2015-12-31"},

        {"start":"2016-01-01","end":"2016-03-31"},
        {"start":"2016-04-01","end":"2016-06-30"},
        {"start":"2016-07-01","end":"2016-09-30"},
        {"start":"2016-10-01","end":"2016-12-31"},

        {"start":"2017-01-01","end":"2017-03-31"},
        {"start":"2017-04-01","end":"2017-06-30"},
        {"start":"2017-07-01","end":"2017-09-30"},
        {"start":"2017-10-01","end":"2017-12-31"},

        {"start":"2018-01-01","end":"2018-03-31"},
        {"start":"2018-04-01","end":"2018-06-30"},
        {"start":"2018-07-01","end":"2018-09-30"},
        {"start":"2018-10-01","end":"2018-12-31"},

        {"start":"2019-01-01","end":"2019-03-31"},
        {"start":"2019-04-01","end":"2019-06-30"},
        {"start":"2019-07-01","end":"2019-09-30"},
        {"start":"2019-10-01","end":"2019-12-31"},

        {"start":"2020-01-01","end":"2020-03-31"},
        {"start":"2020-04-01","end":"2020-06-30"},
        {"start":"2020-07-01","end":"2020-09-30"},
        {"start":"2020-10-01","end":"2020-12-31"},

        {"start":"2021-01-01","end":"2021-01-31"},
    ]

    for dates in tgtDates:
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