# system/attachment imports
import os, csv, string

# sklearn imports
from sklearn.cluster import KMeans
from sklearn.metrics import v_measure_score
import sklearn.metrics as metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer

# calculation imports
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math
#%matplotlib inline

# feature extraction / NLTK imports
import nltk
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer
nltk.download('punkt')
nltk.download('stopwords')

# vectorization / Word2Vec imports
from gensim.models import Word2Vec

def main():
    # get data
    df = pd.read_csv(str(os.path.dirname(__file__)) + "/TwitterDataset.csv")
    print(df.head())

    # clean data
    clean = []

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
        reconstruct = reconstruct.replace("https", "")
        clean_tokens = nltk.word_tokenize(reconstruct)
        # assigning clean list to new attribute
        clean.append(clean_tokens)
    df['Clean'] = clean
    print(df.head())
    print("")

if __name__ == '__main__':
    main()