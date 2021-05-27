import os

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def main():
    sentiment_scores()

def sentiment_scores():

    # Get Data
    #df = pd.read_csv(str(os.path.dirname(__file__)) + "/data/TwitterDataset.csv")
    #df = pd.read_csv('/Users/josieldelgadillo/Documents/GitHub/Research_Skyskraper_Josiel/SourceCode/Datasets/SemEval_2017_Task4_TestSplit_BERT_Senti.csv')
    url = 'https://drive.google.com/file/d/112gfs3JqG6yMogLiGDIFUSkaH-68uLzo/view?usp=sharing'
    url2='https://drive.google.com/uc?id=' + url.split('/')[-2]
    df = pd.read_csv(url2)
    print(df.head())

    #capture VADER Data
    VADERscore = []
    VADERcompound = []
    VADERclassification = []

    count = 0


    for index, row in df.iterrows():
        print(count)
        sentence = row.Tweet
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
        count = count + 1

    df["VADER_Score"] = VADERscore
    df["VADER_Compound"] = VADERcompound
    df["VADER_Classification"] = VADERclassification
    print(df.head())
    df.to_csv ("//Users/josieldelgadillo/Documents/GitHub/Research_Skyskraper_Josiel/SourceCode/Datasets/SemEval_2017_Task4_TestSplit_BERT_Senti_VADER.csv", index = False, header=True)


if __name__ == '__main__':
    main()