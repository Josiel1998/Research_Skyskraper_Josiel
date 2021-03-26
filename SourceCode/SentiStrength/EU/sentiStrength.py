import subprocess
import shlex
import os
import psycopg2
import json
import pandas as pd


def main():
    db()

def RateSentiment(sentiString):

    # Get relative path
    dirname = os.path.dirname(__file__)

    getJar = "java -jar " + dirname + "/SentiStrengthCom.jar"
    getData = "stdin sentidata " + dirname + "/SentStrength_Data_Sept2011/"
    option = "scale"
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split(getJar + " " + getData + " " + option),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    #Can't send string in Python 3, must send bytes
    b = bytes(sentiString.replace(" ","+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)
    #convert from byte
    stdout_text = stdout_byte.decode("utf-8") 
    #replace the tab with a space between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t"," ")
    classification = stdout_text.split()
    positive = int(classification[0])
    negative = int(classification[1])
    overall = int(classification[2])

    # Switch/Casing classification definition
    if(-4 == overall):
        sentiment = "Strong Negative"
    elif(-3 == overall):
        sentiment = "Negative"
    elif(0 > overall):
        sentiment = "Weak Negative"
    elif(0 == overall):
        sentiment = "Neutral"
    elif(3 > overall):
        sentiment = "Weak Positive"
    elif(3 == overall):
        sentiment = "Positive"
    else:
        sentiment = "Strong Positive"

    print("Sentiment result is " + sentiment + " " + str(overall))
    return str(overall)


def db():
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    
    try:
        conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
        print("Connected to " + conn.dsn)
        cur = conn.cursor()

        # list all tables with tweets
        tweets_by_handle = ["nytimesbusiness", "washingtonpost", "yahoofinance", "reutersbiz", "bbcbusiness", "wsjmarkets", "nypostbiz", "sfchronicle", "markets" "awealthofcs", "barronsonline", "benzinga", "bnkinvest", "charliebilello", "ewhisper", "grassosteve", "hmeisler", "igsquawk", "jimcramer", "jon_prosser", "jonnajarian", "marketwatch", "michaelbatnick", "neilcybart", "northmantrader", "raoulgmi", "reformedbroker", "thestreet", "tmfjmo", "tomwarren", "zacksresearch"]

        # loop through tables on database and get sentiment of tweet
        for tbl in tweets_by_handle:
            sql =  "SELECT * FROM tweets_by_handle." + tbl
            df = pd.read_sql(sql, conn)

            for row in df.iterrows():
                print(str(row[0]) + ": " + str(row[1].tweet_text))
                RateSentiment(row[1].tweet_text)

    except Exception as e: print(e)

if __name__ == '__main__':
    main()