from senti_client import sentistrength
senti = sentistrength('EN')
res = senti.get_sentiment('I love using sentistrength!')
print(res)