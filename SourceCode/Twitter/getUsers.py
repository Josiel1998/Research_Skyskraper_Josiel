import requests
import json
import os
from getpass import getpass
import psycopg2

def main():
    getTwitterUsers()

def prodDB(data:object):
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    print("Connected to " + conn.dsn)
    cur = conn.cursor()

    # Iterate through twitter data and execute insert statements
    for u in data:
        sql = '''INSERT INTO josiel_project.twitter_users(twitter_id,name,username,follower_count,creation_timestamp,description,verified) VALUES(%s,%s,%s,%s,%s,%s,%s);'''
        values = (u['id'], u['name'], u['username'], u['public_metrics']['followers_count'], u['created_at'], u['description'], u['verified'])
        cur.execute(sql, values)
        conn.commit()
        print(cur.rowcount, " record inserted.")

    conn.close()

def getTwitterUsers():

    twitter_users = ["tomwarren","matty_mogal", "neilcybart", "jon_prosser","reformedBroker","LizAnnSonders", "charliebilello", "awealthofcs",
                    "michaelbatnick", "hmeisler", "raoulGMI", "zacksresearch", "barronsonline", "benzinga", "marketwatch", "igsquawk",
                    "northmantrader", "jimcramer", "jonnajarian", "grassosteve", "ewhispers", "tmfjmo", "bnkinvest", "thestreet"]

    last_user = twitter_users[len(twitter_users)-1]
    url = "https://api.twitter.com/2/users/by?usernames="
    BEARER_TOKEN = json.loads(os.getenv("TWITTER_CREDS"))["bearer"]

    # create URL target
    for user in twitter_users:
        if user != last_user:
            url = url + user + ","
        else:
            url = url + user
    
    # append the rest of the Twitter API body
    url = url + "&user.fields=id,name,username,public_metrics,created_at,description,verified"


    # variables for Twitter API request
    payload = {}
    headers = {"Authorization": "Bearer " + BEARER_TOKEN }

    # make Twitter API request
    response = requests.request("GET", url, headers = headers, data = payload)

    # store, format, and print JSON results from API request
    json_data = json.loads(response.text)
    print(json_data)

    # Call PostgreSQL databse and pass Twitter results
    prodDB(json_data['data'])

if __name__ == '__main__':
    main()