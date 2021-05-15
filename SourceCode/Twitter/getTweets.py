import requests
import json
import os
import psycopg2
import pandas as pd

table = []

def main():
    getScope()

    global table
    getTweets(table)

def getScope():
    global table

    # Connect to database and get all tables within scope of Skyskraper Twitter handles
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
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

def getTweets(tables:list):
    for t in tables:
        # Connect to database to get current user account oldest tweet for reference point
        DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
        conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
        print("Connected to " + conn.dsn)
        cur = conn.cursor()

        # Create SQL query for oldest stored tweet within the database for username
        sql = '''SELECT * from tweets_by_handle.''' + t + ''' order by tweet_id asc;'''
        cur.execute(sql)
        row = cur.fetchone()
        old_tweet_id = row[0]

        # Create HTTP (API) Request to get tweet for twitter username and starting at oldest tweet
        url = "https://api.twitter.com/2/tweets/search/all?query=from:" + t + "&max_results=100&until_id=" + str(old_tweet_id)
        # BEARER_TOKEN = json.loads(os.getenv("TWITTER_CREDS"))["bearer"]
        BEARER_TOKEN = os.getenv("TWITTER_RESEARCH_BEARER")

        payload={}
        headers = {"Authorization": "Bearer " + BEARER_TOKEN }

        try:
            response = requests.request("GET", url, headers = headers, data = payload)
            print(response.text)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()