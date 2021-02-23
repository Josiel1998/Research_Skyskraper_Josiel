import requests
import json
import os
import psycopg2
import datetime
 
def main():
 
    company = ["TSLA", "AAPL", "MSFT", "AMZN", "GOOG", "FB", "BRK.A", "V", "WMT", "JNJ"]
    for ticker in company:
        getStockTrade(ticker)
 
def getStockTrade(ticker:str):
 
    API_KEY = os.getenv("POLYGON_API_KEY")
 
    # Iterate through everyday
    start_date = datetime.date(2005, 1, 1)
    end_date = datetime.date(2021, 1, 31)
    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        print("Starting batch for " + str(start_date))
 
        # Build API URL
        url = "https://api.polygon.io/v2/ticks/stocks/trades/" + ticker + "/" + str(start_date) + "?reverse=true&limit=50000&apiKey=" + API_KEY

        # headers for Polygon API request
        payload = {}
        headers = {}
 
        # make Polygon Aggregates (Bar) API request
        try:
            response = requests.request("GET", url, headers = headers, data = payload)
            if(response.status_code == 200):
                res = json.loads(response.text)
                if(res['results_count'] != 0):
                    print(res)
                #db(response.text, ticker.upper())

            # Proceed to the next date
            start_date += delta
        except Exception as e: print(e)
        except:
            print(response.status_code)
            print(response.raise_for_status)
        
        
 
def db(data:str, ticker:str):
 
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    cur = conn.cursor()
 
    conn.close()
 
if __name__ == '__main__':
    main()