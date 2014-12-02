'''

Author: Darian Pazgan-Lorenzo

Generates a graph based on tweet data by reply level, topic similarity, and
estimated sentiment polarity. The input file should be a list of tweets with
similarity and sentiment appended.

This script uses the Matplotlib graphing library for python:
http://www.matplotlib.org

Usage: python graphSentiment.py <input_file> 

'''

import numpy as np
import matplotlib.pyplot as plt

import sys

#right now we collected tweets down to 3 levels deep
levels = 3

#collect array of similarities and sentiment for each reply level; average them
#returns 2-tuple: first value is average similarity, second is average sentiment
def getMetrics(input_filename):
    similarities = []
    sentiments = []
    input_file = open(input_filename)

    for line in input_file:
        #get the similarity and sentiment
        #encode text
        line = unicode(line, 'utf-8')
        similarity = float(line.split()[-2])
        sentiment = float(line.split()[-1])
        similarities.extend([similarity])
        sentiments.extend([sentiment])

    total_similarity = 0
    total_sentiment = 0
    for similar in similarities:
        total_similarity += similar
    for sent in sentiments:
        total_sentiment += sent

    return (total_similarity/len(similarities), total_sentiment/len(sentiments))

def getMetricsBinary(input_filename):
    similarities = []
    sentiments = []
    input_file = open(input_filename)

    for line in input_file:
        #get the similarity and sentiment
        #encode text
        line = unicode(line, 'utf-8')
        similarity = float(line.split()[-2])
        sentiment = line.split()[-1]
        similarities.extend([similarity])
        sentiments.extend([sentiment])

    total_similarity = 0
    total_sentiment = 0
    for similar in similarities:
        total_similarity += similar
    for sent in sentiments:
        if sent == "pos":
            total_sentiment += float(1)
        else:
            total_sentiment -= float(1)

    return (total_similarity/len(similarities), total_sentiment/len(sentiments))
    

def main():
    #get number of args (first one is script name itself)
    n = len(sys.argv) - 1

    similarity_means = []
    sentiment_means = []
    for i in range(1, n+1):
        averages = getMetricsBinary(sys.argv[i])
        similarity_means.extend([averages[0]])
        sentiment_means.extend([averages[1]])
    
    ind = np.arange(n)
    #width of bars
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, similarity_means, width, color='b')
    rects2 = ax.bar(ind+width, sentiment_means, width, color='g')

    #add label text
    ax.set_ylabel('similarity/polarity')
    ax.set_xticks(ind+width)

    ax.legend( (rects1[0], rects2[0]), ('Similarity','Sentiment Polarity') )

    plt.show()

main()
