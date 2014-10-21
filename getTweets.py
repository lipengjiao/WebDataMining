#getTweets.py
'''
Author: Peng 

Requirement: 
    1. Install tweepy: https://github.com/gmanual/Twitter-OAuth-GeekTool-Script/wiki/Installing-Tweepy-on-OSX 
    2. Only tested on Mac OSX, it may not be working on Windows

Usage: python getTweets.py <query> <size> <include retweets or not>
Example: python getTweets.py "Ebola" 1000 Y > Ebola.txt

Output: 
    Each line is a tweet or retweets. Each tweet and its retweets are a paragraph. The first line of the paragraph is the tweet, and the following lines of the paragraph are its retweets. 
    Between two adjacent paragraph, there is another new line (a line of empty string)

Example: 
tweet1
retweet1_of_tweet1
retweet2_of_tweet1
...
<newline>
tweet2
retweet1_of_tweet1
retweet2_of_tweet1
...


More: have to remove duplicate lines for the Output
sort Ebola.txt | uniq -u > Ebola.uniq.txt

'''

import tweepy
import time
import json
import sys
# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = 'wDYCX7S5rkynzu80cBDQBfsbW'
consumer_secret = 'tq0vk9NV36kSAQQmQaLSy2si9Pp6rvZWYV4z2NMs1oifRdIqov'
access_token = '2795565154-2SbXZI5KcVIL01ahpAlkHIOqdHnqEGIkFfuklu0'
access_token_secret = 'awm4dQNrJwwDMifsN4Mdk0WrKTdJf6LFwkpPZsVi1wUaT'
# Create authentication token using our details
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


#api = tweepy.API(auth, wait_on_rate_limit=True)
api = tweepy.API(auth)


query = sys.argv[1]
size = int(sys.argv[2])
flag_include_retweets = sys.argv[3]
seen = set() 
for tweet_json in tweepy.Cursor(api.search,                   
                       q=query,
                       count=100,
                       result_type="recent",
                       include_entities=True, # needed for id
                       lang="en").items(size):

    if tweet_json.id not in seen: # check duplicates
        seen.add(tweet_json.id) 
        tweet_txt = tweet_json.text.encode('utf8')
        tweet_txt = tweet_txt.replace("\t", "\s") # replace tab with space
        tweet_txt = tweet_txt.replace("\n", "\s") # replace newline with space
        print tweet_txt

        if flag_include_retweets == "Y":
            retweets = api.retweets(tweet_json.id, count = 100) # get 100 retweets for each tweet
        
            if retweets is not None:
            
                for retweet in retweets: 
                    retweet = retweet.text.encode('utf8')
                    retweet = retweet.replace("\t", "\s") # replace tab with space
                    retweet = retweet.replace("\n", "\s") # replace newline with space
                    print retweet;   
               
            print




