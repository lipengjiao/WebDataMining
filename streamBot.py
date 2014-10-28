import tweepy
import json
import re
# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = 'wDYCX7S5rkynzu80cBDQBfsbW'
consumer_secret = 'tq0vk9NV36kSAQQmQaLSy2si9Pp6rvZWYV4z2NMs1oifRdIqov'
access_token = '2795565154-2SbXZI5KcVIL01ahpAlkHIOqdHnqEGIkFfuklu0'
access_token_secret = 'awm4dQNrJwwDMifsN4Mdk0WrKTdJf6LFwkpPZsVi1wUaT'

#this is the file to be written 
fo = open('Halloween.txt','a')

fill = ""
# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        
	if decoded['lang'] == "en":
            x = decoded['text'].encode('ascii', 'xmlcharrefreplace')
            x = re.sub(r'(\w+:\/\/\S+)|(\n)|(\s)', ' ', x)
            fo.write( '%s\t@%s\t%s' % (decoded['created_at'], decoded['user']['screen_name'], x))
            fo.write( '\n')
            
        return True
    
    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "Collecting all new tweets for  Halloween:"

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['Halloween'])
