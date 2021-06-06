import psycopg2
from dotenv import dotenv_values
import pandas as pd

# load secret environment variables
config = dotenv_values(".env")

# model imports
import torch
from torch import nn, optim
from transformers import BertModel, BertTokenizer

# model variables
class_names = ['Negative', 'Neutral', 'Positive']
PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
MAX_LEN = 80
device = torch.device("cpu")

def main():
  print("Choose between predicting tweets from a databse or file")
  #db()
  file()

def file():
    sentiment = []
    sentiment_details = []
    df = pd.read_csv("GitHub/Research_Skyskraper_Josiel/SourceCode/Datasets/Investigation/AllSentences_FSB.csv")
    print(df.head())
    print(df.info())

    for index, row in df.iterrows():
      print(index)
      print(row.Text)
      sentiment.append(predict(row.Text)) 
      sentiment_details.append(predict_d(row.Text))

    df["BERTSentiment_8020"] = sentiment
    df["BERTDetails_8020"] = sentiment_details

    df.to_csv("GitHub/Research_Skyskraper_Josiel/SourceCode/Datasets/Investigation/AllSentences_FSB.csv", index = False, header=True)

def db():
    try:
        # Connect to database and get all tables within scope of Skyskraper Twitter handles
        conn = psycopg2.connect(database = config['DBNAME'], user = config['DBUSER'], password = config['DBPASSWORD'], host = config['DBHOST'], port = config['DBPORT'])
        print("Connected to " + conn.dsn)
        cur = conn.cursor()

        # Create SQL query for Twitter handles within schema
        sql = "SELECT * FROM tweets_by_handle.amazon "
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            # Make prediction
            print(model_b(row[3]))
            # TO DO MORE
        conn.close()
    except Exception as e:
        print("Unable to connect to the database")
        print(e)
    print(model_b("THIS IS THE SAMPLE TEXT"))

class SentimentClassifier(nn.Module):
  def __init__(self, n_classes):
    super(SentimentClassifier, self).__init__()
    self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
    self.drop = nn.Dropout(p=0.3)
    self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
  def forward(self, input_ids, attention_mask):
    _, pooled_output = self.bert(
      input_ids=input_ids,
      attention_mask=attention_mask
    )
    output = self.drop(pooled_output)
    return self.out(output)

model = SentimentClassifier(len(class_names))



def model_b(text:str):
    model.load_state_dict(torch.load('GitHub/Research_Skyskraper_Josiel/SourceCode/BERT/model/SE2017T4_BERT_base_cased_model.bin', map_location=torch.device("cpu")))
    return predict(text)

def predict(tweet):
  encoded_review = tokenizer.encode_plus(
  tweet,
  max_length=MAX_LEN,
  add_special_tokens=True,
  return_token_type_ids=False,
  pad_to_max_length=True,
  return_attention_mask=True,
  return_tensors='pt',
  truncation=True
  )

  input_ids = encoded_review['input_ids'].to(device)
  attention_mask = encoded_review['attention_mask'].to(device)
  output = model(input_ids, attention_mask)
  _, prediction = torch.max(output, dim=1)
  print("BERT OUTPUT: " + str(output))
  print("BERT PREDICTION: " + class_names[prediction])
  return class_names[prediction]

def predict_d(tweet):
  encoded_review = tokenizer.encode_plus(
  tweet,
  max_length=MAX_LEN,
  add_special_tokens=True,
  return_token_type_ids=False,
  pad_to_max_length=True,
  return_attention_mask=True,
  return_tensors='pt',
  truncation=True
  )

  input_ids = encoded_review['input_ids'].to(device)
  attention_mask = encoded_review['attention_mask'].to(device)
  output = model(input_ids, attention_mask)
  _, prediction = torch.max(output, dim=1)
  return str(output)

if __name__ == '__main__':
    main()