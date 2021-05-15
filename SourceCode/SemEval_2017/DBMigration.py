import json, os
import psycopg2

def main():
    hl = "/Users/josieldelgadillo/Documents/GitHub/Research_Skyskraper_Josiel/SourceCode/SemEval_2017/Raw/Task 5/Headlines_Testdata_withscores.json"
    micro = "/Users/josieldelgadillo/Documents/GitHub/Research_Skyskraper_Josiel/SourceCode/SemEval_2017/Raw/Task 5/Microblogs_Testdata_withscores.json"
    
    # migrate headline data
    fi = open(hl,)
    data = json.load(fi)
    migrateHL(data)

    # migrate microblog data
    fi2 = open(micro,)
    data2 = json.load(fi2)
    migrateMicro(data2)

def migrateHL(obj:json):
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    print("Connected to " + conn.dsn)
    cur = conn.cursor()

    for item in obj:
        title = item['title'].replace("'", "")
        company = item['company'].replace("'", "")
        sql = '''INSERT INTO semeval_2017.task_5_microblogs_and_headlines(headline_unique_id, headline_id, text, raw_sentiment_score, company) VALUES( ''' + "'" + str(item['UniqueID']) + "'" + "," + str(item['id']) + "," + "'" + title + "'" + "," + str(item['sentiment score']) + "," + "'" + company + "'" + ''');'''
        cur.execute(sql)
        conn.commit()
        print("Committed INSERT for " + str(item['title']))

    conn.close()

def migrateMicro(obj:json):
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    print("Connected to " + conn.dsn)
    cur = conn.cursor()

    for item in obj:
        text = item['text'].replace("'", "")
        source = item['source'].replace("'", "")
        sql = '''INSERT INTO semeval_2017.task_5_microblogs_and_headlines(tweet_id, text, raw_sentiment_score, source, ticker) VALUES( ''' + "'" + str(item['id']) + "'" + ",'" + text + "'," + str(item['sentiment score']) + ",'" + source + "','" + str(item['cashtag']) + "'" + ''');'''
        cur.execute(sql)
        conn.commit()
        print("Committed INSERT for " + text)

    conn.close()

if __name__ == '__main__':
    main()