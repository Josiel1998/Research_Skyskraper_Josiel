import requests
r = requests.get('https://finnhub.io/api/v1/stock/transcripts?id=AAPL_162777&token=c0icmgf48v6qfc9dhq70')
print(r.json())