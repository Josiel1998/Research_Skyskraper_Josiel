import requests
import json
import os
import psycopg2
import pandas as pd
from dotenv import dotenv_values

# load secret environment variables
config = dotenv_values(".env")

table = []

def main():
    getTweets('619950566786113536')

def getScope():
    global table

    try:
        # Connect to database and get all tables within scope of Skyskraper Twitter handles
        conn = psycopg2.connect(database = config['DBNAME'], user = config['DBUSER'], password = config['DBPASSWORD'], host = config['DBHOST'], port = config['DBPORT'])
        print("Connected to " + conn.dsn)
        cur = conn.cursor()

        # Create SQL query for Twitter handles within schema
        sql = "SELECT table_name FROM information_schema.tables WHERE  table_schema = 'tweets_by_handle'"
        cur.execute(sql)
        rows = cur.fetchall()
        for tbl in rows:
            # store list of tables in global variable
            table.append(tbl[0])
        conn.close()
    except Exception as e:
        print("Unable to connect to the database")
        print(e)

def getTweets(id:str):

    # Create HTTP (API) Request to get tweet for twitter username and starting at oldest tweet
    url = "https://api.twitter.com/2/tweets/" + id
    # BEARER_TOKEN = json.loads(os.getenv("TWITTER_CREDS"))["bearer"]
    BEARER_TOKEN = config['TWITTER_BEARER']

    payload={}
    headers = {"Authorization": "Bearer " + BEARER_TOKEN }

    try:
        response = requests.request("GET", url, headers = headers, data = payload)
        print(response.text)
        getScope()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()