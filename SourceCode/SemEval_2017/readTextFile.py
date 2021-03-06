# import pandas library as pd
import pandas as pd
  
def main():
    tweet_id = []
    sentiment =[]
    tweet = []

    tweet_id_gold = []
    sentiment_gold =[]
    tweet_gold = []

    # create an Empty DataFrame object
    df = pd.DataFrame()
    df_gold = pd.DataFrame()
    count = 0

    with open('SourceCode/SemEval_2017/Raw/Task 4/SemEval2017-task4-dev.subtask-A.english.INPUT.txt') as f1:
        lines1 = [line.rstrip() for line in f1]
        for line1 in lines1:
            if(not(line1 == '' or line1 == '"')):
                res = line1.split("\t")
                tweet_id.append(res[0])
                sentiment.append(res[1])
                tweet.append(res[2])

        df['Tweet ID'] = tweet_id
        df['Sentiment'] = sentiment
        df['Tweet'] = tweet
        print(df.shape)            
        print(df.head())

        df.to_csv('SourceCode/SemEval_2017/Raw/Task 4/SUBTASK_DATASET.csv')

        with open('SourceCode/SemEval_2017/Raw/Task 4/twitter-2016test-A-English.txt') as f2:
            lines2 = [line2.rstrip() for line2 in f2]
            for line2 in lines2:
                if(not(line2 == '' or line2 == '"')):
                    res2 = line2.split("\t")
                    tweet_id_gold.append(res2[0])
                    sentiment_gold.append(res2[1])

                    #for index, row in df.iterrows():
                    #    if(row.values[0] == res2[0]):
                    #        tweet_gold.append(row.values[2])
                    #        count = count + 1
                    #        print(str(count) + " " + str(res2[0]) + " " + str(row.values[2]))

            df_gold['Tweet ID'] = tweet_id_gold
            df_gold['Sentiment'] = sentiment_gold
            #df_gold['Tweet'] = tweet_gold
            print(df_gold.shape)            
            print(df_gold.head())

            df_gold.to_csv('SourceCode//GOLD-DATASET.csv')


if __name__ == '__main__':
    main()