import requests, os, itertools, json, datetime, psycopg2
import pandas as pd

def main():
    #company = ["AAPL", "TSLA", "MSFT", "AMZN", "GOOG", "FB", "BRK.A", "V", "WMT", "JNJ"]
    company = ["AMZN"]
    for ticker in company:
        print("Starting " + ticker)
        getTranscriptList(ticker)
        getTranscriptDetails(ticker)


# get list of transcripts for ticker symbol
def getTranscriptList(ticker:str):
    print("Getting transcript list: " + ticker)
    API_KEY = os.getenv("FINNHUB_API_KEY")

    # headers for Polygon API request
    payload = {}
    headers = {}
 
    # make Tickers API request
    try:
        # Build API URL and iterate numbers starting from 1
            url = '''https://finnhub.io/api/v1/stock/transcripts/list?symbol=''' + str(ticker) + '''&token=''' + API_KEY
            response = requests.request("GET", url, headers = headers, data = payload)
            if(response.status_code == 200):
                # for each ticker response, send DB list of transcripts
                db(ticker, response.text)
    except Exception as e: print(e)
    except:
        print(response.status_code)
        print(response.raise_for_status)

# Get details of the transcript call (id)
def getTranscriptDetails(ticker:str):
    print("Getting transcript detail: " + ticker)
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    print("Connected to " + conn.dsn)
    cur = conn.cursor()

# Create SQL code to see if table for ticker exist

    if ticker == "BRK.A":
        exists = '''SELECT EXISTS (SELECT FROM information_schema.tables WHERE  table_schema = 'finnhub_transcripts' AND table_name = ''' +  "'" + "brk_a" + '''');'''
    else:
        exists = '''SELECT EXISTS (SELECT FROM information_schema.tables WHERE  table_schema = 'finnhub_transcripts' AND table_name = ''' +  "'" + ticker.lower() + '''');'''
    cur.execute(exists)
    row = cur.fetchone()


    # Check if table exist
    if (not row[0]):
        print("Table does not exist.")
        
        if ticker == "BRK.A":
            createSQL ='''
            CREATE TABLE finnhub_transcripts.''' + "brk_a" + '''
            (
                transcript_id character varying NOT NULL,
                audio character varying,
                transcript_date date,
                transcript_time time without time zone,
                ticker character varying,
                title character varying,
                speaker character varying,
                speaker_text character varying
            );

            ALTER TABLE finnhub_transcripts.''' + ticker.lower() + '''
                OWNER to jkd5377;'''
        else:
        # Create table
            createSQL ='''
            CREATE TABLE finnhub_transcripts.''' + ticker.lower() + '''
            (
                transcript_id character varying NOT NULL,
                audio character varying,
                transcript_date date,
                transcript_time time without time zone,
                ticker character varying,
                title character varying,
                speaker character varying,
                speaker_text character varying
            );

            ALTER TABLE finnhub_transcripts.''' + ticker.lower() + '''
                OWNER to jkd5377;'''
        
        cur.execute(createSQL)
        conn.commit()
    else:
        print("Table does exist.")

    # Get list of transcripts
    if ticker == "BRK.A":
        sql = '''SELECT * FROM finnhub_transcripts_meta.''' + "brk_a" + ''';'''
    else:
        sql = '''SELECT * FROM finnhub_transcripts_meta.''' + ticker.lower() + ''';'''
    cur.execute(sql)
    row = cur.fetchall()
        
    API_KEY = os.getenv("FINNHUB_API_KEY")
    # headers for Polygon API request        
    payload = {}
    headers = {}

    # Get id from transcript list and get transcript details
    for item in row:
        print(item[0])
        print("Getting transcript detail: " + item[0])

        # make Finnhub API request
        try:
            # Build API URL for transcript details
                url = '''https://finnhub.io/api/v1/stock/transcripts/list?id=''' + str(item[0]) + '''&token=''' + API_KEY
                res = requests.request("GET", url, headers = headers, data = payload)
                if(res.status_code == 200):
                    # for each ticker response, send DB list of transcripts
                    data = json.loads(res.text)
                    for speech in data['transcript']:
                        timestampD = datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
                        for sentence in speech['speech']:
                            text = sentence.replace("'", "")
                            name = speech['name'].replace("'","")
                            try:
                                # Create INSERT query
                                if ticker == "BRK.A":
                                    sql = '''INSERT INTO finnhub_transcripts.''' + "brk_a" + '''(transcript_id, audio, ticker, transcript_date, transcript_time, title, speaker, speaker_text) VALUES( ''' + "'" + str(data['id']) + "','" + str(data['audio']) + "','" + ticker.lower() + "','" + str(timestampD.date()) + "','" + str(timestampD.time()) + "','" + data['title'] + "','" + name + "','" + text + "'" + ''');'''
                                else:
                                    sql = '''INSERT INTO finnhub_transcripts.''' + ticker.lower() + '''(transcript_id, audio, ticker, transcript_date, transcript_time, title, speaker, speaker_text) VALUES( ''' + "'" + str(data['id']) + "','" + str(data['audio']) + "','" + ticker.lower() + "','" + str(timestampD.date()) + "','" + str(timestampD.time()) + "','" + data['title'] + "','" + name + "','" + text + "'" + ''');'''
                                cur.execute(sql)
                                conn.commit()
                            except Exception as e: 
                                sql = '''rollback;'''
                                cur.execute(sql)
                                conn.commit()
                                print(e)
        except Exception as e: print(e)
        except:
            print(res.status_code)
            print(res.raise_for_status)


def db(ticker:str, response:requests.models.Response):
    print("DB for " + ticker)
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    print("Connected to " + conn.dsn)
    cur = conn.cursor()

    # Create SQL code to see if table for ticker exist
    if ticker == "BRK.A":
        exists = '''SELECT EXISTS (SELECT FROM information_schema.tables WHERE  table_schema = 'finnhub_transcripts_meta' AND table_name = ''' +  "'" + "brk_a" + '''');'''
    else:
        exists = '''SELECT EXISTS (SELECT FROM information_schema.tables WHERE  table_schema = 'finnhub_transcripts_meta' AND table_name = ''' +  "'" + ticker.lower() + '''');'''
    cur.execute(exists)
    row = cur.fetchone()

    # Check if table exist
    if (not row[0]):
        print("Table does not exist.")
        
        # Create table
        if ticker == "BRK.A":
            createSQL ='''
            CREATE TABLE finnhub_transcripts_meta.''' + "brk_a" + '''
            (
                transcript_id character varying NOT NULL,
                ticker character varying,
                quarter character varying,
                transcript_time time without time zone,
                transcript_date date,
                title character varying,
                year integer,
                PRIMARY KEY (transcript_id)
            );

            ALTER TABLE finnhub_transcripts_meta.''' + "brk_a" + '''
                OWNER to jkd5377;'''
        else:
            createSQL ='''
            CREATE TABLE finnhub_transcripts_meta.''' + ticker.lower() + '''
            (
                transcript_id character varying NOT NULL,
                ticker character varying,
                quarter character varying,
                transcript_time time without time zone,
                transcript_date date,
                title character varying,
                year integer,
                PRIMARY KEY (transcript_id)
            );

            ALTER TABLE finnhub_transcripts_meta.''' + ticker.lower() + '''
                OWNER to jkd5377;'''
        
        cur.execute(createSQL)
        conn.commit()
    else:
        print("Table does exist.")
    
    # Convert data into JSON
    res = json.loads(response)
    for trans in res['transcripts']:
        
        timestamp = datetime.datetime.strptime(trans['time'], '%Y-%m-%d %H:%M:%S')
        try:
            # Create INSERT query
            if ticker == "BRK.A":
                sql = '''INSERT INTO finnhub_transcripts_meta.''' + "brk_a" + '''(transcript_id, quarter, ticker, transcript_date, transcript_time, title, year) VALUES( ''' + "'" + str(trans['id']) + "'," + str(trans['quarter']) + ",'" + ticker.lower() + "','" + str(timestamp.date()) + "','" + str(timestamp.time()) + "','" + trans['title'] + "'," + str(trans['year']) + ''');'''
            else:
                sql = '''INSERT INTO finnhub_transcripts_meta.''' + ticker.lower() + '''(transcript_id, quarter, ticker, transcript_date, transcript_time, title, year) VALUES( ''' + "'" + str(trans['id']) + "'," + str(trans['quarter']) + ",'" + ticker.lower() + "','" + str(timestamp.date()) + "','" + str(timestamp.time()) + "','" + trans['title'] + "'," + str(trans['year']) + ''');'''
            cur.execute(sql)
            conn.commit()
        except Exception as e: print(e)
    conn.close()




if __name__ == '__main__':
    main()
