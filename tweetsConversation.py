#getTweets.py
'''
Author: Peng 
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


api = tweepy.API(auth, wait_on_rate_limit=True)
#api = tweepy.API(auth)



def cleanTweet(x):
    # convert to ascii
    x = x.encode('ascii', 'xmlcharrefreplace')
    # remove url, punctuation, \t, \n
    x = ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)|[\n \t]"," ",x).split())
    #x = re.sub(r'(\w+:\/\/\S+)|(\n)|(\s)|[{}]', ' ', x)
    return "\""+ x + "\""


def get_Tree(id): 
    tweet = api.get_status(id)
    user = '@' + tweet.user.screen_name
    dt = str(tweet.created_at).split()[0];

    for reply in tweepy.Cursor(api.search, q=user, count = 100, since_id = id, include_entities= True).items():
        if reply.in_reply_to_status_id == id:
            print '{'
            print reply.text
            get_Tree(reply.id)
            print '}'
                            

#tweet_id = int(sys.argv[1])
tweet_id = 526572433948819456
myTweet = api.get_status(tweet_id)


#print myTweet.created_at
tweet_txt = myTweet.text

print cleanTweet(tweet_txt)
get_Tree(tweet_id)

