import pandas as pd

def main():
    extractDictNSentimentLabel()

def extractDictNSentimentLabel():

    # Extract and seperate columns
    dictionary = pd.read_csv("SourceCode/Datasets/StanfordSentimentTreebank/dictionary.txt",sep="|")
    dictionary.columns= ["Phrase", "PhraseID"]
    print(dictionary.head())
    print(dictionary.shape)

    # Extract and seperate columns
    sentimentLabel = pd.read_csv("SourceCode/Datasets/StanfordSentimentTreebank/sentiment_labels.txt",sep="|")
    sentimentLabel.columns= ["PhraseID", "SentimentLabel"]
    print(sentimentLabel.head())
    print(sentimentLabel.shape)

    # Provide Fine-grained Sentiment and Trinary Sentiment Labels
    fg_senti = []
    tri_senti = []

    for index, row in sentimentLabel.iterrows():
        print(index)

        if row.SentimentLabel > 0 and row.SentimentLabel <= 0.2:
            fg_senti.append("Very Negative")
            tri_senti.append("Negative")
        elif row.SentimentLabel > 0.2 and row.SentimentLabel <= 0.4:
            fg_senti.append("Negative")
            tri_senti.append("Negative")
        elif row.SentimentLabel > 0.4 and row.SentimentLabel <= 0.6:
            fg_senti.append("Neutral")
            tri_senti.append("Neutral")
        elif row.SentimentLabel > 0.6 and row.SentimentLabel <= 0.8:
            fg_senti.append("Positive")
            tri_senti.append("Positive")
        else:
            fg_senti.append("Very Positive")
            tri_senti.append("Positive")
    sentimentLabel["FineGrainSentiment"] = fg_senti
    sentimentLabel["TrinarySentiment"] = tri_senti

    SST1 = pd.merge(dictionary, sentimentLabel,left_on='PhraseID', right_on="PhraseID", how="left")
    SST1.to_csv("SourceCode/Datasets/StanfordSentimentTreebank/SST1_PhrasesAndSentiments.csv")


if __name__ == '__main__':
    main()