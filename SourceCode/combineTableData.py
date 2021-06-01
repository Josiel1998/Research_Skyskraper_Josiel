import pandas as pd

def main():
    df = pd.read_csv("SourceCode/Datasets/SandersCorpus/full-corpus.csv")
    #df1 = pd.read_csv("SourceCode/Datasets/StanfordSentimentTreebank/SST1_PhrasesAndSentiments1.csv")
    print(df.shape)

    df2 = df[df['Sentiment'] != 'irrelevant']
    print(df2.shape)

    #df['BERTSentiment2'] = df1['BERTSentiment2'].astype(str)
    #df['BERTDetails2'] = df1['BERTDetails2'].astype(str)

    print(df2.info())
    df2.to_csv("SourceCode/Datasets/SandersCorpus/full-corpus-clean.csv", index = False, header=True)


if __name__ == '__main__':
    main()