import os

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def main():
    sentiment_scores()

def sentiment_scores():

    # Get Data
    df = pd.read_csv('SourceCode/Datasets/SandersCorpus/full-corpus.csv')
    #url = 'https://drive.google.com/file/d/1m6M0uUhM90I1rVsRutg5P-4BuI-nEqkC/view?usp=sharing'
    #url2='https://drive.google.com/uc?id=' + url.split('/')[-2]
    #df = pd.read_csv(url2, names=['Sentiment', 'TweetID', 'Date', 'Query', 'User', 'Tweet'])
    print(df.head())

    #capture VADER Data
    VADERscore = []
    VADERcompound = []
    VADERclassification = []

    count = 0


    for index, row in df.iterrows():
        if(row.Sentiment != "irrelevant"):
            print(index)
            sentence = row.TweetText
            print(sentence)
            # Create a SentimentIntensityAnalyzer object.
            sid_obj = SentimentIntensityAnalyzer()
        
            # polarity_scores method of SentimentIntensityAnalyzer
            # oject gives a sentiment dictionary.
            # which contains pos, neg, neu, and compound scores.
            sentiment_dict = sid_obj.polarity_scores(sentence)

            VADERscore.append(sentiment_dict)
            VADERcompound.append(sentiment_dict['compound'])
            
            print("Overall sentiment dictionary is : ", sentiment_dict)
            #print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
            #print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
            #print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
        
            print("Sentence Overall Rated As", end = " ")
        
            # decide sentiment as positive, negative and neutral
            if 0.05 <= sentiment_dict['compound'] <= 1:
                print("Positive")
                VADERclassification.append("Positive")
            elif -0.05 <= sentiment_dict['compound'] <= 0.05:
                print("Neutral")
                VADERclassification.append("Neutral")
            else:
                print("Negative")
                VADERclassification.append("Negative")
            print("")

    df["VADER_Score"] = VADERscore
    df["VADER_Compound"] = VADERcompound
    df["VADER_Sentiment"] = VADERclassification
    print(df.head())
    print(df.info())
    df.to_csv ("SourceCode/Datasets/SandersCorpus/full-corpus.csv", index = False, header=True)


if __name__ == '__main__':
    main()