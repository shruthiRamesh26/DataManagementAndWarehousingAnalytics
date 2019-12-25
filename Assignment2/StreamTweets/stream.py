import tweepy as tw
from tweepy import Stream
from tweepy.streaming import StreamListener
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


class MyListener(StreamListener):
    def cleanData(self,text):
        # remove ascii characters
        str(text).encode('ascii', 'ignore')
        # remove url
        text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', str(text))
        # to accept only alpha-numeric characters with white space
        text = re.sub(r'([^a-zA-Z0-9\s]|_)+', '', str(text))
        # removing new lines metacharacter
        text = re.sub(r'[\n]', ' ', text)
        # removing non-printable characters like emoticons
        printable = set(string.printable)
        text = list(filter(lambda x: x in printable, text))
        return ''.join(text)

    def on_data(self, data):

        try:
            streamData = json.loads(data)
            rtwttext=""
            rtwtloc=""
            if "retweeted_status" in streamData:
                rtwttext=''.join(self.cleanData(streamData["retweeted_status"]["extended_tweet"]["full_text"]))
                rtwtloc=''.join(self.cleanData(streamData["retweeted_status"]["user"]["location"]))
            # to select the full text which is in under "extended_tweet" in the streamData else take "text"
            if "extended_tweet" in streamData:
                text= self.cleanData(streamData["extended_tweet"]["full_text"])
            else:
                text=self.cleanData(streamData["text"])

                # dictionary tostore in JSON file
                data = {
                    'id': streamData["id_str"],
                    'text': text,
                    'date_time': streamData["created_at"].__str__(),
                    'retweettext': rtwttext,
                    'retweetloc' : rtwtloc,
                    'location': self.cleanData(streamData["user"]["location"])
                }
                # Append the dictionary to 'search.json' file
                with open('stream.json', 'a') as json_file:
                     json.dump(data, json_file)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True


    def on_error(self, status):
        print(status)
        return True

#authorization to twitter developer account to access streaming data in extended mode (to get full text)
twitter_stream = Stream(auth, MyListener(),tweet_mode='extended')
#collect tweets which have the follwing words
twitter_stream.filter(track=['Canada','Canada AND import','Canada AND export','Canada AND vehicle AND sales','Canada AND Education'])