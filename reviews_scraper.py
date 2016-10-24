# first go at scraping reviews - 15/10/2016 
from __future__ import division, unicode_literals
from bs4 import BeautifulSoup
import requests
import urllib2
import httplib
import re
import math
from textblob import TextBlob as tb
from stop_words import get_stop_words
from textblob.sentiments import NaiveBayesAnalyzer


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'


# reviews are displayed in batches of 10. url/reviews?start=0, start=10, ....
# div_id = tn15content has all the reviews
# title at <h2>
bloblist = []
lst = []
stop_words = get_stop_words('english')
stemEndings = [ "-s", "-es", "-ed", "-er", "-ly" "-ing", "-'s", "-s'" ]
punctuation = ".,:;!?"
remove = '|'.join(stop_words)

def remove_punctuation(input_string):
    for item in punctuation:
        input_string = input_string.replace(item, '')
    return input_string

def remove_stopwords(input_string):
    regex = re.compile(r'\b('+remove+r')\b', flags=re.IGNORECASE)
    out = regex.sub("", input_string)
    return out



def do_stuff():
    for p2 in xrange(0, 2):
        url1 = 'http://www.imdb.com/title/tt1668746/reviews?start='
        url = url1 + str(p2*10)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        whole_review_block = soup.find('div', {'id': 'tn15content'})
        # lst = []
        # titles = whole_review_block.find('b', string='Author:')
        # print titles.next_sibling.next_sibling  # this has the a href tag with the author details - link & name - store it in a class maybe
        # reviews are enclosed in <p> mostly. False positives need to be filtered out.

        i = 0
        for review in whole_review_block.find_all('p')[: -1]:
            cleaned_review = re.sub("<.*?>", "", str(review).decode('utf-8'))  # removes all unnecessary tags from the reviews
            cleaned_review = cleaned_review.lower()
            print 'Review %s' % i
            print
            print tb(cleaned_review)
            print
            cleaned_review = remove_punctuation(cleaned_review)
            cleaned_review = remove_stopwords(cleaned_review)
            rev_tb = tb(cleaned_review)
            bloblist.append(rev_tb)
            i += 1
            blob = tb(cleaned_review, analyzer=NaiveBayesAnalyzer())
            print blob.sentiment
            print
        
    full_st = ''
    for i, blob in enumerate(bloblist):
        # print 'Top words in review %s' % i
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        out_filename = 's01e02_tf_idf_full.txt'
        st = '\n\nReview {}\nWord\tTF-IDF\n'.format(i)

        for word, score in sorted_words:
            st += '{}\t{}\n'.format(word, round(score, 5))
        full_st += st + '------------------------------------'

    with open(out_filename, 'w') as f:
        f.write(full_st.encode('utf-8'))

if __name__ == '__main__':
    do_stuff()