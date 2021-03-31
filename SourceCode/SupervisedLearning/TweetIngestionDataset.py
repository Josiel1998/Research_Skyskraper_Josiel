import json, psycopg2, os, csv
import pandas as pd
from dotenv import load_dotenv
#load_ext dotenv
#%reload_ext dotenv
#%dotenv

#global dataframe
col = ["tweet_id", "tweet_date", "tweet_time", "tweet_text", "likes", "retweets", "parent_tweet_id", "username", "tweet_url"]
df = pd.DataFrame()

def main():
    accounts = ["amazon", "barronsonline", "bbcbusiness", "benzinga", "bnkinvest", "igsquawk", "markets", "marketwatch", "nypostbiz", "nytimesbusiness", "reutersbiz", "sfchronicle", "theeconomist", "thestreet", "washingtonpost", "wsjmarkets", "yahoofinance", "zachsresearch","awealthofcs", "carlquintanilla", "charliebilello", "ewhispers", "grassosteve", "jimcramer", "jon_prosser", "jonajarian", "lizannsonders", "neilcybart", "northmantrader", "raoulgmi", "reformedbroker", "thestalwart", "tmfjmo", "tomwarren"]
    for acc in accounts:
        createCSV(acc)
    global df
    df.to_csv ("/Users/josieldelgadillo/Documents/GitHub/Research_Skyskraper_Josiel/SourceCode/SupervisedLearning/data/", index = False, header=True)
        
def createCSV(acc:str):
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    
    try:
        conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
        print("Connected to " + conn.dsn)
        #df = pd.DataFrame()
        global df
        print("Starting " + acc)

        cur = conn.cursor()
        sql = '''SELECT * FROM tweets_by_handle.''' + acc + ''';'''
        cur.execute(sql)
        row = cur.fetchall()
        for rec in row:
            dictionary = {
                "tweet_id": rec[0], 
                "tweet_date": rec[1], 
                "tweet_time": rec[2], 
                "tweet_text": rec[3].replace(",", ""), 
                "likes": rec[4], 
                "retweets": rec[5], 
                "parent_tweet_id": rec[6], 
                "username": rec[7], 
                "tweet_url": rec[8]
                }
            df = df.append(dictionary,ignore_index=True)
        print(df.shape)
        print(df.head())
    except Exception as e:
        print(e)
    
    # close database connection
    conn.close()

if __name__ == '__main__':
    main()