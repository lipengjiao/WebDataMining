#cleanInput.py

'''

Author: Darian Pazgan-Lorenzo

This is a corpus pre-processing script to do some cleanup on twitter data.
The primary goal is to remove URLs and emoticons from tweets. Currently the URL removal is pretty solid, will be implementing emoticon removal soon.

Usage: python cleanInput.py <infile> > <outfile>
Example: python cleanInput.py input.txt > output.txt

'''

import os
import re

def main():

    pre_output = []
    output = []

    input = open("Data/Ebola.uniq.txt")
    for line in input:
        #replace urls with regex matching
        linkRemoved = re.sub(r'(https?://.*?[ "])?(https?://.*$)?', "", line)
        if(len(linkRemoved) > 0):
            pre_output.append(linkRemoved)

    #remove empty lines in output
    for line in pre_output:
        if not line.strip():
            #line is empty
            continue
        else:
            output.append(line)
            
    #print output
    print "".join(output)

main()
