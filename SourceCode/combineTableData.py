import pandas as pd

def main():
    df = pd.read_csv("SourceCode/Datasets/StanfordSentimentTreebank/SST1_PhrasesAndSentiments.csv")
    df1 = pd.read_csv("SourceCode/Datasets/StanfordSentimentTreebank/SST1_PhrasesAndSentiments1.csv")

    df['BERTSentiment2'] = df1['BERTSentiment2'].astype(str)
    df['BERTDetails2'] = df1['BERTDetails2'].astype(str)

    print(df.info())
    df.to_csv("SourceCode/Datasets/StanfordSentimentTreebank/SST1_PhrasesAndSentiments.csv", index = False, header=True)


if __name__ == '__main__':
    main()