import pycurl
import json
import os
import psycopg2
from pandas import DataFrame
import pycurl
from io import BytesIO 
from bs4 import BeautifulSoup
from bs4.element import Comment
import pickle
from dotenv import dotenv_values

# load secret environment variables
config = dotenv_values(".env")

 
def main():
    company = ["aapl", "amzn", "brk.a", "fb", "goog", "jnj", "msft", "tsla", "v", "wmt"]
    for ticker in company:
        print("Start " + ticker)
        getTickerNewsContent(ticker)
 
def getTickerNewsContent(ticker:str):
    if ticker == 'brk.a':
        ticker = ticker.replace(".","_")
    
    db(ticker)

def db(ticker:str):
 
    # Make database connection
    try:
        conn = psycopg2.connect(database = config['DBNAME'], user = config['DBUSER'], password = config['DBPASSWORD'], host = config['DBHOST'], port = config['DBPORT'])
        cur = conn.cursor()
        sql = '''SELECT * FROM polygon_ticker_news.''' + ticker
        cur.execute(sql)
        df = DataFrame(cur.fetchall())
        print("The number of news: ", cur.rowcount)

        for row in df.iterrows():
            print(row[1].values[4]) # get link
            html = getContent(row[1].values[4]) # get HTML
            cur2 = conn.cursor()
            jar = pickle.dumps(cleanHTML(html),pickle.HIGHEST_PROTOCOL) 
            #pickle.dump(html, open( "html.pickle", "wb" ), pickle.HIGHEST_PROTOCOL)
            #eatPickle = pickle.load(open( "html.pickle", "rb" ))
            print(jar)
            sql2 =  '''UPDATE polygon_ticker_news.''' + ticker + ''' SET content =''' + "'" + html + "'" + '''WHERE ticker = ''' + "'" + row[1].values[0] + "'" + ''' and tickerdate = ''' + "'" + row[1].values[1] +"'" + ''' and tickertime = ''' + "'" + row[1].values[2] + "'" + ''' and title = ''' + "'" + row[1].values[3] + "'"
            cur.execute(sql2)
            conn.commit()
            #if (row[1].values[5] == 'CNBC'):
            #    cur2 = conn.cursor()
            #    sql2 = '''SELECT ticker, tickerdate, tickertime, title FROM polygon_ticker_news.''' + ticker
            #    cur.execute(sql2)
            #    record = cur.fetchall()

            #    print(CNBC(html))
            #    print("")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    conn.close()
    
def getContent(url:str):
    b_obj = BytesIO() 
    crl = pycurl.Curl() 
    crl.setopt(crl.URL, url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform() 
    crl.close()
    # Get the content stored in the BytesIO object (in byte characters) 
    get_body = b_obj.getvalue()
    # Decode the bytes stored in get_body to HTML and print the result 
    return get_body.decode('utf8')

def CNBC(html:str):
    soup = BeautifulSoup(html,features="html.parser")
    texts = soup.find_all("div", class_="group")
    res = ""
    for t in texts:
        res = res + " " + t.text
    return res

def cleanHTML(html:str):
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

if __name__ == '__main__':
    main()