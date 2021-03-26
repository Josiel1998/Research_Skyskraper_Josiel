import json, psycopg2, os, csv
import pandas as pd

#feature extraction
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
import string
from nltk.tokenize.treebank import TreebankWordDetokenizer
nltk.download('punkt')
nltk.download('stopwords')

# vectorization
from gensim.models import Word2Vec 
from sklearn.cluster import KMeans


def main():
    createCSV()
    readCSV()


def createCSV():
    # Make database connection
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    
    conn = psycopg2.connect(database=DATABASE_CRED["database"], user = DATABASE_CRED["user"], password = DATABASE_CRED["password"], host = DATABASE_CRED["host"], port = DATABASE_CRED["port"])
    print("Connected to " + conn.dsn)
    cur = conn.cursor()

    sql = "SELECT * FROM tweets_by_handle.barronsonline;"
    cur.execute(sql)
    row = cur.fetchall()

    #Convert dictionary to a pandas dataframe
    df = pd.DataFrame().append(row, ignore_index=True)
    fieldName = ['tweet_id', 'tweet_date', 'tweet_time', 'tweet_text', 'likes', 'retweets', 'parent_tweet_id', 'username', 'tweet_url']
    df.columns = fieldName
    
    #Clean text for comma - this impacts CSV readability
    for index, row in df.iterrows():
        row.tweet_text = row.tweet_text.replace(row.tweet_text,row.tweet_text.replace(",",""))

    path = str(os.path.dirname(__file__)) + '/data/barronsonline_tweets.csv'
    #Convert dataframe to CSV file
    df.to_csv(path)

    conn.close()
# https://machinelearningmastery.com/clean-text-machine-learning-python/
def readCSV():
    path = str(os.path.dirname(__file__)) + '/data/barronsonline_tweets.csv'
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        tokens = nltk.word_tokenize(row.tweet_text)
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        # remove punctuation from each word
        reconstruct = TreebankWordDetokenizer().detokenize(tokens)
        new = reconstruct.translate(str.maketrans('', '', string.punctuation))
        stripped = nltk.word_tokenize(new)
        # remove remaining tokens that are not alphabetic
        words = [word for word in stripped if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        reconstruct = TreebankWordDetokenizer().detokenize(words)
        print(reconstruct)

def wordToVector():
    w2v_model = Word2Vec(min_count=3,
                     window=4,
                     size=300,
                     sample=1e-5, 
                     alpha=0.03, 
                     min_alpha=0.0007, 
                     negative=20)
    


    model = KMeans(n_clusters=2, max_iter=1000, random_state=True, n_init=50).fit(X=word_vectors.vectors)
    positive_cluster_center = model.cluster_centers_[0]
    negative_cluster_center = model.cluster_centers_[1]

if __name__ == '__main__':
    main()