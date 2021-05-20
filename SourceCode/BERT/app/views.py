from re import A
from app import app

from flask import render_template
from flask import request

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

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/", methods=['POST'])
def server():
  print(request.form['text'])
  if request.form['text'] != '':
    if request.method == 'POST':
      text = request.form['text']
      bert_model_response = model_b(text)
      bert_model_response_raw = model_b_raw(text)
      return render_template("public/index.html", text = text, results = bert_model_response, raw = bert_model_response_raw)
  else:
    return render_template("public/index.html")

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
    model.load_state_dict(torch.load('/Users/josieldelgadillo/Documents/GitHub/Research_Skyskraper_Josiel/SourceCode/BERT/app/resources/SE2017T4_BERT_base_cased_model.bin', map_location=torch.device("cpu")))
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
  print("BERT PREDICTION: " + str(prediction))
  return class_names[prediction]

def model_b_raw(text:str):
  model.load_state_dict(torch.load('/Users/josieldelgadillo/Documents/GitHub/Research_Skyskraper_Josiel/SourceCode/BERT/app/resources/SE2017T4_BERT_base_cased_model.bin', map_location=torch.device("cpu")))
  return predict_raw(text)

def predict_raw(tweet):
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