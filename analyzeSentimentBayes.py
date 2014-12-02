from textblob.classifiers import NaiveBayesClassifier

import sys

def main():

    #train classifier on subset of remarks
    with open('preppedtrain.csv', 'r') as fp:
        cl = NaiveBayesClassifier(fp, format="csv")

    #read input file and classify
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
        sentiment = str(cl.classify(line))
        #print the original line with the sentiment attached to the end
        if (line.strip() != ""):
            print orig + "\t" + sentiment

main()
