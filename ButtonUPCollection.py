'''
Given a reply tweet's id, this script print out all its ancestors.

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

id1 = 532040146980732928

def buttomUpSearch(id):
	tweet = api.get_status(id)
	
	if tweet.in_reply_to_status_id is not None:
		buttomUpSearch(tweet.in_reply_to_status_id)

	tweet_txt = tweet.text
	user_name = tweet.user.screen_name
	tweet_id = tweet.id
	tweet_txt = re.sub('[\t\r\n]', ' ', tweet_txt).encode('utf8')
	output = '/'+ user_name + '/status/' + str(tweet_id)+'\t'+tweet_txt	
	print output

buttomUpSearch(id1)