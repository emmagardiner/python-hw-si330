__author__ = 'emmagardiner'

# -*- coding: utf-8 -*-
#!/usr/bin/python -tt

import json
import tweepy
import time
import nltk
import pandas
import vincent
import io
import re
import csv

stemmer = nltk.stem.PorterStemmer()

from nltk.stem.wordnet import WordNetLemmatizer
lm = WordNetLemmatizer()

#nltk.download()

consumer_key = "Fay6kXfGcALGAjaRpKH6FYZVW"
consumer_secret = "9M2XWbRvGaVhzfwxz5dYkE8qho4zUyYIR1NectOAHIuJyk7soP"
access_token = "2275236163-Kdduy1tBjNjOPRZCMtAZV6InTORwc2M3FYDbI4q"
access_token_secret = "SxpyiJYAymWZNK6VBbhOyLC04oVCstByzzBZnUtsGC5ES"

keyword_list = ['winter'] #hashtag list

start_time = time.time() #grabs the system time

#Step 1: Download Streaming Tweets
#This is the listener, responsible for receiving data
class listener(tweepy.StreamListener):
    def __init__(self, start_time, time_limit):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []

    def on_data(self, data):
        save = open('SI330_egard_rawtweets.json', 'w')
        while (time.time() - self.time) < self.limit:
            try:
#Twitter returns tweets in JSON format - we need to #decode it first. The tweets are contained in the #variable data
#From the tweet json string, save only the 'created_at' #and 'text' attributes

                decoded = json.loads(data)
                data_write = json.dumps({'user': decoded['user']['screen_name'], 'time': decoded['created_at'], 'tweet': decoded['text']}).encode('utf-8')
                self.tweet_data.append(data_write)
                self.tweet_data.append("\n")
                return True #Don't kill the Twitter stream, keep listenin
            except BaseException, e:
                print 'failed on_data,', str(e)
                print decoded
                return True

# If rate limit notice, then make sure you filter it out # from your final outputs
#		return True

        #Write data to json file
        save.writelines(self.tweet_data)
        save.close()
        return False # Kill the Twitter stream

    def on_error(self, status):
        print status



# Step 2: Preprocessing Tweets
# Tweets usually have a lot redundant text that may not be useful. Before we can process the tweets,
# we need to clean the data first.

def pre_processing(line):
    # Convert the tweets to lower case.
    pre_txt = line.lower()
    # Replace URLs with the word URL
    pre_txt = re.sub(r'\bhttps?://[\w|\.|/]+\b', 'URL', pre_txt)
    # Replace @username with the word AT_USER
    pre_txt = re.sub(r'\0[A-Za-z0-9_]*', 'AT_USER', pre_txt)
    pre_txt = re.sub(r'\@\w+', 'AT_USER', pre_txt)
    # Replace #hashtag with the exact same word without the hash. E.g. #winter replaced with 'winter'.
    pre_txt = re.sub(r'\#', ' ', pre_txt)
    # Remove any excessive punctuations such as multiple white spaces or punctuations at the end of the tweet such !!!!!?
    pre_txt = re.sub(r'\!+', ' ! ', pre_txt)
    pre_txt = re.sub(r'\?+',' ? ', pre_txt)
    # Any other transformations you deem fit
    pre_txt = re.sub(r'[^A-Za-z0-9#\?\!\'\"\@\(\)\:\$\%]+', ' ', pre_txt)
    pre_txt = re.sub(r'\(', ' ( ', pre_txt)
    pre_txt = re.sub(r'\)', ' ) ', pre_txt)
    pre_txt = re.sub(r'\:', ' : ', pre_txt)
    pre_txt = re.sub(r'\"', ' " ', pre_txt)
    pre_txt = re.sub(r'\%', ' % ', pre_txt)
    pre_txt = re.sub(r'\$',  ' $ ', pre_txt)
    pre_txt = re.sub(r' [ ]*', ' ', pre_txt)
    return pre_txt


f = open('SI330_egard_rawtweets.json', 'r')

file = open('SI330_egard_cleanedtweets.json', 'w')

for line in f:
    decode = json.loads(line)
    text = decode['tweet']
    clean_tweet = pre_processing(text)
    output = json.dumps(clean_tweet)
    file.writelines(output)
    file.writelines('\n')

file.close()



# Step 3: Training Classifiers


def extract_feature(feat):
    token = nltk.word_tokenize(feat)
    count = {}
    for word in token:
        stem = lm.lemmatize(word)
        if stem in count:
            count[stem] += 1
        else:
            count[stem] = 1
    #bigrams
    for index in range(0, len(token)-1):
        word1 = lm.lemmatize(token[index])
        word2 = lm.lemmatize(token[index+1])
        bigram = '+'.join([word1, word2])
        if bigram in count:
            count[bigram] += 1
        else:
            count[bigram] = 1
    return count



# Load csv file
def load_class_data():

    read_csv = csv.reader(open('class_tweet_data.csv', 'rb'), delimiter=',')
    read_csv.next()
    labeled_set = []

    # For each tweet in training data:
    # i) Preprocessing, get rid of irrelevant characters and take care of stemming.
    # ii) Extract features from each tweet. Call extract_features function

    for tweet in read_csv:
        feat = pre_processing(tweet[0])
        feature = extract_feature(feat)
        #print feature

        if feature != None:
            labeled_set.append((feature, tweet[2]))


    # Train and evaluate classifier - NaiveBayes classifier
    #(use first 800 as training, rest as test to evaluate)
    train, test = labeled_set[:800], labeled_set[800:]

    # Train final classifier using all labelled dataset.
    classifier = nltk.NaiveBayesClassifier.train(labeled_set)
    return classifier

# Part 4: Sentiment Analysis
# Read cleaned tweets from stream file,
# Apply trained classifiers, and generate label.
# Output to json file.

def sentiment_analysis(classifier):
    #(Insert code here)
    f = io.open('si_330_egard_labelledtweets.json', 'w')
    f2 = open('SI330_egard_cleanedtweets.json', 'r')
    for line in f2:
        tweet = json.loads(line)
        feat = extract_feature(pre_processing(tweet['tweet']))
        if feat != None:
            x = classifier.classify(feat)
        else:
            x = "Neutral"

        sentiment_data = json.dumps({'time': tweet['time'], 'tweet': tweet['tweet'], 'sentiment': x})
        f.write(u''.join(sentiment_data))
        f.write(u'\n')
    f.close()

#Part 5:
#Trends in Tweets:
#1) Quantity of tweets in time
#2) Sentiments in time

#The following code uses pandas to generate the frequencies that can be plotted by Vincent.
def time_series_tweets():
    with open('si_330_egard_labelledtweets.json') as graph_file:
        d = dict()
        time_array = []
        for line in graph_file:
            data = json.loads(line)
            time_array.append(data['time'])
        # a list of "1" to count the dates
        ones = [1]*len(time_array)
        # the index of the series
        idx = pandas.DatetimeIndex(time_array)
        #print idx
        # the actual series (at series of 1s for the moment)
        t_array = pandas.Series(ones, index=idx)
        #print t_array

        # Resampling / bucketing
        t_array = t_array.resample('5s', how='sum').fillna(0)
        time_chart = vincent.Line(t_array)
        time_chart.axis_titles(x='Time', y='Freq')
        time_chart.to_json('term_freq.json')

def time_series_sents():
    with open('si_330_egard_labelledtweets.json') as graph_file:
        d = dict()
        time_array = []
        for line in graph_file:
            data = json.loads(line)
            if (data['sentiment']=="Positive"):
                time_array.append(data['time'])
        # a list of "1" to count the dates
        ones = [1]*len(time_array)
        # the index of the series
        idx = pandas.DatetimeIndex(time_array)
        #print idx
        # the actual series (at series of 1s for the moment)
        t_array = pandas.Series(ones, index=idx)
        #print t_array

        # Resampling / bucketing
        t_array = t_array.resample('5s', how='sum').fillna(0)
        time_chart = vincent.Line(t_array)
        time_chart.axis_titles(x='Time', y='Freq')
        time_chart.to_json('sent_freq.json')



if __name__ == '__main__':
    #Will listen Twitter stream for 1200 seconds
    # l = listener(start_time, time_limit=1200)
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    #
    # # In this example follow #sunday tag
    # # Listen to Twitter streaming data for the given keyword. Narrow it down to English.
    #
    # stream = tweepy.Stream(auth, l)
    # stream.filter(track=keyword_list, languages=['en'])

    file = open('SI330_egard_rawtweets.json', 'r')
    outputfile = open('SI330_egard_cleanedtweets.json', 'w')

    for line in file:
        decode = json.loads(line)
        text = decode['tweet']
        clean_tweet = pre_processing(text)
        output = json.dumps({'time': decode['time'], 'tweet': clean_tweet}).encode('utf-8')
        outputfile.writelines(u''.join(output).encode('utf-8'))
        outputfile.writelines(u'\n')
    outputfile.close()

    classifier = load_class_data()
    sentiment_analysis(classifier)
    time_series_tweets()
    time_series_sents()