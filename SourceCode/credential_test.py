import os
import json

def main():
    TWITTER_BEARER = json.loads(os.getenv("TWITTER_CREDS"))["bearer"]
    ALPHA_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    DATABASE_CRED = json.loads(os.getenv("DATABASE_CREDS"))
    print(DATABASE_CRED["database"])


if __name__ == '__main__':
    main()