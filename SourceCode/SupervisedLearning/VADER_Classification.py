import os

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def main():
    sentiment_scores()

def sentiment_scores():

    # Get Data
    df = pd.read_csv(str(os.path.dirname(__file__)) + "/data/TwitterDataset.csv")
    print(df.head())

    #capture VADER Data
    VADERscore = []
    VADERcompound = []
    VADERclassification = []


    for index, row in df.iterrows():
        sentence = row.tweet_text
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
    df["VADER_Classification"] = VADERclassification
    print(df.head())
    df.to_csv ("/Users/josieldelgadillo/Documents/GitHub/Research_Skyskraper_Josiel/SourceCode/SupervisedLearning/data/TwitterDatasetVADERLabel.csv", index = False, header=True)


if __name__ == '__main__':
    main()