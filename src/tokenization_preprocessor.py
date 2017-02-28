'''
Akond Rahman
tokenization
Feb 28, 2017
'''
from nltk.corpus import stopwords
import re


def processTokensOfOneFile( oneFileContent ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(oneFileContent).get_text()
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
    #
    # 6. Join the words back into one string separated by space,
    # and return the result.
    return( " ".join( meaningful_words ))




def giveMeOneString(listOfStrs):
    str2Ret=''
    for single_str in listOfStrs:
        if len(single_str) > 0:
            str2Ret = str2Ret + single_str
    return str2Ret

def processTokensOfFullCorpus( fullCorpusParam ):
    processed_corpus2ret = []
    for single_file_as_list in fullCorpusParam:
      singleFileAsOneStr = giveMeOneString(single_file_as_list)
      print "the one single str:", singleFileAsOneStr
      print "="*100
      processed_single_file = processTokensOfOneFile(singleFileAsOneStr)
      print "after processing a file looks like:", processed_single_file
      print "="*100
      processed_corpus2ret.append(processed_single_file)
