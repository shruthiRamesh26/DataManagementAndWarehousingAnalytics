from pymongo import MongoClient
from pyspark import SparkContext
from pyspark import SparkConf
from operator import add
from pyspark.sql import SparkSession
import glob
import re
#connecting to mongoDB where serch and stream tweets are stored
client = MongoClient('0.0.0.0', 27017)
db = client['assignment2']

#search data from a collection "searchtweets"
searchData = db.searchtweets
#stream data from a collection "streamtweets"
streamData = db.streamtweets
#creating spark context
sc = SparkContext('local', 'Data Processing')
#spark session
ss = SparkSession.builder.appName("PythonWordCount").getOrCreate()
# input words to find the count for, using map reduce
to_find = ['oil', 'vehicle', 'university', 'dalhousie', 'expensive', 'good school', 'good schools', 'poor school',
           'poor schools', 'population', 'bus', 'buses', 'agriculture', 'economy']


def mapred(name, totalWords):
    #converting all words to string
    words = str(''.join(str(v) for v in totalWords))
    #removing all non-alpha-numeric characters.
    words = re.sub(r'([^a-zA-Z0-9\s]|_)+', '', words)
    #Creating a file to store the input
    f1 = open(name + "input.txt", "w")
    f1.write(words.lower())
    #map reduce process
    input = sc.textFile(name + "input.txt").flatMap(lambda line: line.split(" "))
    wordCounts = input.map(lambda word: (word, 1)).reduceByKey(add).collect()
    #Creating a file to store the output of map reduce process.
    f2 = open(name + 'output.txt', "w")
    #printing the category of data (Search tweets,Streat tweets or Articles)
    print("%s Map reduce" % name)
    for word, count in wordCounts:
        # selecting only the reuired words to print
        for find in to_find:
            #ignoring case for matching
            if word.lower() == find.lower():
                #printing words and their count
                print("%s \t %i \n" % (word, count))
                #Writing the result of map reduce process to output file
                f2.write("%s \t %i \n" % (word, count))


if __name__ == "__main__":
    articleWords = []
    path = './articles/*.txt'
    files = glob.glob(path)
    #looping through every text file i the "articles" older
    for file in files:
        #opening each text file
        with open(file) as f:
            #reading content of every file
            content = f.read()
            #converting the content to string and appending the content to an array
            articleWords.append((re.split(' ', str(content))))
    #invoking mapre function to perform map reduce process on the article text
    mapred('articles', articleWords)
    searchwords = []
    for data1 in searchData.find():
        # fetching content of every tweet stored on mongoDb in "searchTweets" collection
        # fetching tweet text
        searchwords.append((re.split(' ', str(data1["text"]))))
        # fetching tweet retweet text
        searchwords.append((re.split(' ', str(data1["retweettext"]))))
    # invoking mapre function to perform map reduce process on the search text
    mapred("search", searchwords)
    streamwords = []
    for data2 in streamData.find():
        # reading content of every tweet stored on mongoDb in "streamTweets" collection
        #fetching tweet text
        streamwords.append((re.split(' ', str(data2["text"]))))
        # fetching tweet retweet text
        streamwords.append((re.split(' ', str(data2["retweettext"]))))
    # invoking mapre function to perform map reduce process on the stream text
    mapred("stream", streamwords)





