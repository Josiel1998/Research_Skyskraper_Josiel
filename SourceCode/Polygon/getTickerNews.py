import requests
import json
import os
import psycopg2
import datetime
import itertools
 
def main():
    company = ["TSLA", "AAPL", "MSFT", "AMZN", "GOOG", "FB", "BRK.A", "V", "WMT", "JNJ"]
    for ticker in company:
        print("Start " + ticker)
        getTickerNews(ticker)
 
def getTickerNews(ticker:str):
 
    API_KEY = os.getenv("POLYGON_API_KEY")

 
    # headers for Polygon API request
    payload = {}
    headers = {}
 
    # make Tickers API request
    try:
        for i in itertools.count(start=1):
            # Build API URL and iterate numbers starting from 1
            url = '''https://api.polygon.io/v1/meta/symbols/''' + ticker + '''/news?perpage=50&page=''' + str(i) + '''&apiKey=''' + API_KEY
            response = requests.request("GET", url, headers = headers, data = payload)
            if(response.status_code == 200):    #check if response is OK
                res = json.loads(response.text)
                if(len(res) != 0):      #check if response is OK and has results
                    db(response, i)
                else:
                    print("No results")
                    break
    except Exception as e: print(e)
    except:
        print(response.status_code)
        print(response.raise_for_status)
 
def db(data:str, page:int):

    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    print(DATABASE_CRED["user"])
    # Make database connection
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    cur = conn.cursor()

    # Convert JSON text into JSON object
    res = json.loads(data.text)

    for news in res:
        # Convert time from ISO to datetime
        isoTime = news['timestamp'].split(".")
        dateTimeOBJ = datetime.datetime.fromisoformat(isoTime[0])


        # Create INSERT query for active exchanges with all fields
        sql = '''INSERT INTO polygon_meta.ticker_news(ticker, tickerdate, tickertime, title, url, source, summary) VALUES( ''' + "'" + news['symbols'][0].lower() + "','" + str(dateTimeOBJ.date()) + "','" + str(dateTimeOBJ.time()) + "','" + news['title'].replace("'","") + "','" + news['url'] + "','" + news['source'] + "','" + news['summary'].replace("'","") + "'" + ''');'''
        cur.execute(sql)
        conn.commit()
        print(news['title'].replace("'","") + " commited, on page " + str(page))
 
    conn.close()
 
if __name__ == '__main__':
    main()