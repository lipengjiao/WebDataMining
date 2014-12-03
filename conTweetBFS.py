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
    x = x.encode('utf8')
    # remove url, punctuation, \t, \n
    x = ' '.join(re.sub("((@[A-Za-z0-9]+)|[^0-9A-Za-z \t])|(\w+:\/\/\S+)|[\n \t]"," ",x).split())
    #x = re.sub(r'(\w+:\/\/\S+)|(\n)|(\s)|[{}]', ' ', x)
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F680-\U0001F6FF'
            u'\u2600-\u26FF\u2700-\u27BF]+', 
            re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'[\u2600-\u26FF\u2700-\u27BF])+', 
            re.UNICODE)

    return myre.sub(' ', x)

# The recursive function to bulid a tree of tweets, root is the topic, and all the chidren are replies. 
def getTreeBFS(root_id): 
    tweet = api.get_status(root_id)
    name = '@' + tweet.user.screen_name
    print cleanTweet(tweet.text)
    q = []
    q.append([root_id, name])

    while(len(q)>0):
        [parent_id, parent_name] = q.pop(0)
        for reply in tweepy.Cursor(api.search, q=parent_name, 
            count = 100, 
            since_id = parent_id, # specifying the since_id will speed up the searching speed.
            include_entities= True,
            lang="en").items():
        
            if reply.in_reply_to_status_id == parent_id:
                name2 = '@' + reply.user.screen_name
                print cleanTweet(reply.text)
                q.append([reply.id, name2])
                            

#q_id = int(sys.argv[1])
#tweet_id = 526572433948819456
q_id = 526847512485715968
getTreeBFS(q_id)

