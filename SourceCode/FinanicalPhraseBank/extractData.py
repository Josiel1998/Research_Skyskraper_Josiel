import pandas as pd

def main():

    # create empty 2d array
    dataSplit = []

    # open text file and extract data
    with open('GitHub/Research_Skyskraper_Josiel/SourceCode/Datasets/Finances/FinancialPhrasebank/Sentences_AllAgree.txt', encoding = "ISO-8859-1") as f:
        lines = f.readlines() 
        for line in lines:
            split = line.split("@")
            split1 = split[1].replace('\n', '')
            dataSplit.append([split[0],split1])
    # convert 2d array into dataframe  
    df = pd.DataFrame(dataSplit, columns=["Text", "Sentiment"])
    print(df.head())

    # create csv of file
    df.to_csv("GitHub/Research_Skyskraper_Josiel/SourceCode/Datasets/Finances/FinancialPhrasebank/AllSentencesCSV.csv")

if __name__ == '__main__':
    main()