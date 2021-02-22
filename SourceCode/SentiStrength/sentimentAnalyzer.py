from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples


# Resource
# https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk

def main():
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    #print(pos_tag(tweet_tokens[0]))
    print(lemmatize_sentence(tweet_tokens[0]))


# normalizes words - make words singular and in its canonical 
def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence



if __name__ == '__main__':
    main()