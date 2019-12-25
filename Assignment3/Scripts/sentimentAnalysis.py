import json
import json
import string
import re
positive=[]
#opening file with list of positive words
with open("positive_words.txt",'r') as p:
    for line in p:
        positive.append(line.rstrip().lower())
negative=[]
#opening file with list of negative words
with open("negative_words.txt",'r') as n:
    for line in n:
        negative.append(line.rstrip().lower())

stopwords=[]
#opening file with list of stopwords
with open("stopwords.txt",'r') as n:
    for line in n:
        stopwords.append(line.rstrip().lower())
#opening file with list of tweets
with open("tweets.json", 'r') as f:
    datastore = json.load(f)
data=[]
for line in datastore:
    arrayWords=line["text"].split()
    #bag to store words and their count
    bag={}
    #list to store matched positive words
    positive_match=[]
    # list to store matched positive words
    negative_match=[]
    #count of positive words
    countPos=0
    #count of negative words
    countNeg=0
    for word in arrayWords:
        #converting word to lower case for comparison with stopwods, positive words and negative words
        word=word.lower()
        sentiment=""
        if word not in stopwords:
            if word in positive:
                #count of positive words is increased for every positive word matched
                countPos+=1
                #storing matched positive words
                positive_match.append(word)
            if word in negative:
                #count of negative words is increased for every negative word matched
                countNeg+=1
                # storing matched negative words
                negative_match.append(word)
        #determining the polarity
        sentiment= "Positive" if countPos>countNeg else "Negative"
        sentiment= "Neutral" if countPos == countNeg else sentiment
        bag.update({word: arrayWords.count(word)})
    element={}
    element.update({"tweet":line["text"],"bag":bag,"matches":{"positive":positive_match,"negative":negative_match},"positive":countPos,"negative":countNeg,"Polarity":sentiment})
    data.append(element)
# output file
with open('sentimentOutput.json', 'w+') as json_file:
    json.dump(data, json_file)





