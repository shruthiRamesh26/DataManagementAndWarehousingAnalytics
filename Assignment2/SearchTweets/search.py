import tweepy as tw
import pandas as pd
import json
import string
import re

#twitter developer account credentials
consumer_key= 'UvAT7r4Lb2m7OgKFEM1286uKy'
consumer_secret= 'AQRDmOqyRujnQmMTZ25IOlSHy5CAfSS0r29pe2sO7kcJYEJvea'
access_token= '1140651374516027392-tML0vwVXbIWW71DpM81yH9pBoPBQKJ'
access_token_secret= 'EQpmhkVpfkG8bi0AnwbNzJXE5xO4u1NJTXMv78K7fKsCV'

#Access to twitter using tweepy library
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
#collect tweets which have the follwing words
search_words = '"Canada" OR \"Canada import\"  OR \"Canada export\" OR \"Canada vehicle sales\" OR \"Canada Education\"'
#search API to collect 2000 search tweets
tweets = tw.Cursor(api.search,
              q=search_words,tweet_mode='extended',lang="en",
             ).items(2000)


def cleanData(text):
	#remove ascii characters
    text.encode('ascii', 'ignore')
	#remove metacharacters
    text=text.rstrip()
	#to remove url
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
	#to accept only alpha-numeric characters with white space
    text = re.sub(r'([^a-zA-Z0-9\s]|_)+', '', text)
	#removing new lines metacharacter
    text=re.sub(r'[\n]', ' ',text)
	#removing non-printable characters like emoticons
    printable = set(string.printable)
    text = list(filter(lambda x: x in printable, text))
    return ''.join(text)


for tweet in tweets:
    rtwttext = ""
    rtwtloc=""
    #clean the twitter text
    tweettext=cleanData(tweet.full_text)
    #check if the tweet is retweeted, if yes,collect the retweeted text and location
    if "retweeted_status"  in tweet._json :
        rtwttext=cleanData(tweet.retweeted_status.full_text)
        rtwtloc=cleanData(tweet.retweeted_status.user.location)
    #dictionary to store in JSON file
    data={
        'id' :tweet.id_str,
        'text': tweettext,
        'metadata': tweet.metadata,
        'date_time': tweet.created_at.__str__(),
        'retweettext': rtwttext,
        'location' : cleanData(tweet.user.location),
        'retweetloc' : rtwtloc
        }
    #Append the dictionary to 'search.json' file
    with open('search.json', 'a') as json_file:
        json.dump(data, json_file)



