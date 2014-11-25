#ForestBFS.py
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



fname = sys.argv[1]

# read inputs 
with open(fname, "r") as f:
    lines = [line.rstrip() for line in f]
f.close();

l0 = open ('trees.leve0.txt', 'a')
l1 = open ('trees.leve1.txt', 'a')
l2 = open ('trees.leve2.txt', 'a')
l3 = open ('trees.leve3.txt', 'a')


def nLevelBFS(root_id, name):
    n = 3
    
    #tweet = api.get_status(root_id)
    #name = tweet.user.screen_name
    #print tweet.text
    level = 0;
    q=[]
    q.append([int(root_id), name, level])

    while(len(q)>0):
        [p_id, p_name, p_level] = q.pop(0)
        
        if p_level > n:
            continue
        
        for child in tweepy.Cursor(api.search, q='@'+p_name, 
            count = 100, 
            since_id = p_id,
            # specifying the since_id will speed up the searching speed.
            include_entities= True,
            lang= 'en').items():

            if child.in_reply_to_status_id == p_id:
                level = p_level+1
                output = '/'+ child.user.screen_name + '/status/' + str(child.id)+'\t'+child.text
                output = output.encode('utf8')
                if level ==1:
                    #output to file1
                    l1.write('%s\n' % output)
                elif level ==2:
                    l2.write('%s\n' % output)
                else:
                    l3.write('%s\n' % output)
                
                q.append([child.id, child.user.screen_name, level])

for line in lines:
    link, txt = line.split('\t')
    e, uName, s,tid  = link.split('/')
    nLevelBFS(tid, uName)
    l0.write('%s\n' % line )



                
            
'''           
# The BFS function to bulid a tree of tweets, root is the topic, and all the chidren are replies. 
def getTreeBFS(root_id, name): 
    #tweet = api.get_status(root_id)
    #name = '@' + tweet.user.screen_name
    name = '@'+name
    #print cleanTweet(tweet.text)
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
'''
                    
