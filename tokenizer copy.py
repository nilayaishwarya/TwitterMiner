import re
import json
import nltk
from collections import Counter
from nltk.corpus import stopwords
import string
import operator
import sys
import pandas
from collections import defaultdict
import vincent


#import nltk
#from nltk.tokenize import word_tokenize
#nltk.download()

p_t = {}
p_t_com = defaultdict(lambda : defaultdict(int))
pmi = defaultdict(lambda : defaultdict(int))

punctuation = list(string.punctuation)
com = defaultdict(lambda : defaultdict(int))
stop = stopwords.words('english') + punctuation + ['rt', 'RT', 'via', '…'] +  stopwords.words('french') +  stopwords.words('spanish')

#print("Write search word")
search_word = 'Madrid' #sys.argv[1] # passing a term as a command-line argument
count_search = Counter()

dates_bale = []

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)

def ascii_check(y):
    for x in y:
        if (64 < ord(x) and ord(x) < 91) or ( 96< ord(x) and ord(x) < 123 ) :
            return True
        else:
            return False

 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
 
print("w1")

with open('laliga.json', 'r') as f:
    count_all = Counter()
    for line in f:
        try:  
            tweet = json.loads(line)    
            if True : #tweet['lang']=='en' :  
            #tokens = preprocess(tweet['text']) 
            #terms_single = set(terms_all)
                #terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
                terms_only = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@')) and (term != '#LaLiga') and ascii_check(term)] 
                count_all.update(terms_only)
                #count_all.update(terms_hash)
                #count_all.update(terms_single)

                #Time series analysis of mentioning 'Bale'
                if 'Bale' in terms_only:
                    dates_bale.append(tweet['created_at'])

                for i in range(len(terms_only)-1):            
                    for j in range(i+1, len(terms_only)):
                        w1, w2 = sorted([terms_only[i], terms_only[j]])                
                        if w1 != w2:
                            com[w1][w2] += 1
                
                if search_word in terms_only:
                    count_search.update(terms_only)
                
            else:
                pass
        #do_something_else(tokens)
            #print(tokens)
        except:
            continue

com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:5])

print("Co-occurrence for %s:" % search_word)
print(count_search.most_common(20))

#print(count_all.most_common(5))

## Time Series Visualization of 'Bale' using pandas

# a list of "1" to count the hashtags
ones = [1]*len(dates_bale)
# the index of the series
idx = pandas.DatetimeIndex(dates_bale)
# the actual series (at series of 1s for the moment)
bale = pandas.Series(ones, index=idx)
 
# Resampling / bucketing
per_minute = bale.resample('60Min', how='sum').fillna(0)

time_chart = vincent.Line(per_minute)
time_chart.axis_titles(x='Time', y='Freq')
#time_chart.to_json('time_chart.json')
time_chart.to_json('time_chart.json', html_out=True, html_path='chart.html')

## Visualization Vega
#word_freq = count_all.most_common(20)
#labels, freq = zip(*word_freq)
#data = {'data': freq, 'x': labels}
#bar = vincent.Bar(data, iter_idx='x')
#bar.to_json('term_freq.json')


#save the HTML template
#bar.to_json('term_freq.json', html_out=True, html_path='vega_visualization.html')

#
for term, n in count_stop_single.items():
p_t[term] = n / n_docs
for t2 in com[term]:
p_t_com[term][t2] = com[term][t2] / n_docs
print(p_t_com[term][t2]