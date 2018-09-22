'''
Akond Rahman
tokenization
Feb 28, 2017
'''
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re
from nltk.stem.snowball import SnowballStemmer
thres_low, thres_up = 3, 7




def processTokensOfOneFile( oneFileContent ):
    stemmer_obj  = SnowballStemmer("english")
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(oneFileContent, "lxml").get_text()
    #
    # 2. Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", oneFileContent)
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))
    #
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]
    # 6. Remove puppet specific keywords
    #pupp_specific_ = ['mozilla', 'include', 'package', 'class', 'user', 'ensure', 'file', 'python', 'default', 'puppet']
    #pupp_specific_ = ['role', 'class', 'mediawiki', 'include']
    #pupp_specific_ = ['mozilla', 'lol', 'hive', 'oozie', 'varnish', 'wiki', 'mediawiki', 'neutron', 'keystone', 'openstack', 'nova', 'contrail']
    #pupp_specific_ = ['rabbit', 'mapreduce', 'wiki', 'mediawiki', 'phabric']
    pupp_specific_ = ['lol', 'change', 'mozilla', 'neutron', 'keystone', 'openstack', 'nova', 'contrail', 'rabbit', 'right', 'temp', 'full', 'tempperm', 'wiki', 'mediawiki']
    filtered_words = [w for w in meaningful_words if not w in pupp_specific_]
    #
    # 7. Only inlcude words at least of length 5 and less than 10
    #valid_len_words = [w for w in filtered_words if (len(w) >= thres_low and len(w) <= thres_up)]
    valid_len_words = [w for w in filtered_words if w >= thres_low ]
    #
    # 8. convert words to utf
    utf_words = [token.decode('utf-8', 'ignore') for token in valid_len_words]
    # 8. convert words to utf
    stemmed_words = [stemmer_obj.stem(token) for token in utf_words]
    # 8. Join the words back into one string separated by space,
    # and return the result
    return( " ".join( stemmed_words ))
