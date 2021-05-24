import json, psycopg2, os
import urllib.request
from dotenv import dotenv_values

# load secret environment variables
config = dotenv_values(".env")

def main():
    #company = ["AXP", "AMGN", "AAPL", "BA", "CAT", "CSCO", "CVX", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "KO", "JPM", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "CRM", "VZ", "V", "WBA", "WMT", "DIS", "DOW", "FB","AMZN", "NFLX", "GOOG"]
    company = ["V", "WBA", "WMT", "DIS", "DOW", "FB","AMZN", "NFLX", "GOOG"]
    for ticker in company:
        getTranscript(ticker)

def getTranscript(ticker:str):
    print("Getting transcript detail: " + ticker)

    conn = psycopg2.connect(database = config['DBNAME'], user = config['DBUSER'], password = config['DBPASSWORD'], host = config['DBHOST'], port = config['DBPORT'])
    print("Connected to " + conn.dsn)
    cur = conn.cursor()

    sql = '''SELECT DISTINCT transcript_id, audio, title FROM finnhub_transcripts.''' + ticker
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        url = row[1]
        filename = row[2]
        tid = row[0]
        if (url == ''):
            print('No Download Available for ' + filename)
        else:
            print("Downloading File: " + filename)
            # edit location below for download location
            urllib.request.urlretrieve(url, '''/Users/josieldelgadillo/Downloads/Seagate/''' + filename + '''_x_''' + tid + '''.mp3''')

if __name__ == '__main__':
    main()
