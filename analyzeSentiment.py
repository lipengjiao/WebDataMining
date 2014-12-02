#analyzeSentiment.py
'''
Author: Darian Pazgan-Lorenzo

Given a dataset of tweets, assign a sentiment value to each one based on its body text.
The sentiment analysis is currently drawn from the TextBlob python
library. The next step is to try a custom classifier with training data. 

Example usage: 
$python analyzeSentiment.py inputfile.txt > sentimentlabels.txt

'''

import sys
import os
import re
from textblob import TextBlob

def main():

    #must supply a filename argument
    if(len(sys.argv) != 2):
        print "Usage: python analyzeSentiment.py <input_file>"
        return
    
    input_file = open(str(sys.argv[1]))

    #list of sentiments
    #sent = []

    for line in input_file:

        #keep original line
        orig = line
        #strip newline artifacts
        orig = orig.replace("\n", "")

        #initialize a TextBlob from the tweet text
        #encode the input line (for Darian's computer this must be done)
        line = unicode(line, 'utf-8')
        #extract tweet text for sentiment analysis 
        tweet = line.split()[1:]
        line = " ".join(tweet)
        line_blob = TextBlob(line)
        sentiment = str(line_blob.sentiment.polarity)
        #print the original line with the sentiment attached to the end
        if (line.strip() != ""):
            print orig + "\t" + sentiment

main()
