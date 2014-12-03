#getTweets.py
'''
Author: Peng 

Requirement: 
    1. Install tweepy: https://github.com/gmanual/Twitter-OAuth-GeekTool-Script/wiki/Installing-Tweepy-on-OSX 
    2. Only tested on Mac OSX, it may not be working on Windows

Usage: python getTweets.py <query> <size> <include retweets or not>
Example: python getTweets.py "Ebola" 1000 > Ebola.txt

Output: 
  Each line will be the tweet's relative link and the tweet's text seperated by \t
  Example: 
  /AlbaGoskova/status/528596294433255424  #TS1989 fave song of the album...

...
More: have to remove duplicate lines for the Output
sort Ebola.txt | uniq -u > Ebola.uniq.txt

'''

import tweepy
import time
import json
import sys
import re
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
size = 5000

for tweet_json in tweepy.Cursor(api.search,                   
                       q=query,
                       count=100,
                       since="2014-11-04", # can not be more than one week
                       #result_type="popular",
                       include_entities=True, # needed for id
                       lang="en").items(5000):
    if not hasattr(tweet_json, 'retweeted_status') and (tweet_json.in_reply_to_status_id is None): #filter out the tweets that is reply or retweet     
      tweet_txt = tweet_json.text.encode('utf8')
      tweet_txt = tweet_txt.replace('\t', ' ') # replace tab with space
      tweet_txt = tweet_txt.replace('\n', ' ') # replace newline with space
      #tweet_txt = ' '.join(re.sub("(\w+:\/\/\S+)"," ",tweet_txt).split())
      #print str(tweet_json.id)+'\t'+'@' + tweet_json.user.screen_name +'\t'+tweet_txt
      print '/'+ tweet_json.user.screen_name + '/status/' + str(tweet_json.id) + '\t' + tweet_txt




