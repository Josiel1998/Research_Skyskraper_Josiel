import requests
import json
import os
import csv
from io import StringIO
import psycopg2

def main():

    companies = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "TSLA", "BRK.A", "V", "WMT", "JNJ"]
    for ticker in companies:
        getHistorical(ticker)

def getHistorical(ticker:str):

    # SLICE
    # Two years of minute-level intraday data contains over 2 million data points, which can take up to Gigabytes of memory. 
    # To ensure optimal API response speed, the trailing 2 years of intraday data is evenly divided into 24 "slices" - 
    # year1month1, year1month2, year1month3, ..., year1month11, year1month12, year2month1, year2month2, year2month3, ..., 
    # year2month11, year2month12. Each slice is a 30-day window, with year1month1 being the most recent and year2month12 being the farthest from today. 
    # By default, slice=year1month1.

    if ticker == "TSLA":
        # Built API URL
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=" + ticker + "&interval=15min&slice=year1month1&apikey=" + os.getenv("ALPHA_VANTAGE_API_KEY")
        
        # variables for Twitter API request
        payload = {}
        headers = {}

        # make Twitter API request
        response = requests.request("GET", url, headers = headers, data = payload)

        # store, format, and print JSON results from API request
        #print(response.text)
        csvFile = StringIO(response.text)
        reader = csv.reader(csvFile, delimiter=',')
        data = []
        for row in reader:
            data.append(row)
            #print('\t'.join(row))
        
        dictionary = {}
        json_arr = []
        for row in data:
            if data[0][0] != row[0]:
                dictionary = {data[0][0]: row[0], data[0][1]: row[1], data[0][2]: row[2], data[0][3]: row[3], data[0][4]: row[4], data[0][5]: row[5]}
                json_arr.append(dictionary)

        for item in json_arr:
            print(item['time'])



if __name__ == '__main__':
    main()