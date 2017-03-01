'''
Akond Rahman
Feb 28, 2017
bag of words technique
'''
import csv, utility, tokenization_preprocessor
from sklearn.feature_extraction.text import CountVectorizer


def getTokensForTokenization(datasetParam):
   completeLabels    = []
   completeCorpus    = [] ## a list of lists with tokens from defected and non defected files
   with open(datasetParam, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row in reader_:
       defectStatus = row[20]
       fileToRead   = row[1]
       fileContentAsStr = utility.giveCommentFreeFileContent(fileToRead)
       #print "!"*75
       #print fileContentAsStr
       filtered_str_from_one_file = tokenization_preprocessor.processTokensOfOneFile(fileContentAsStr)
       #print len(filtered_str_from_one_file)
       #print "="*75
       completeCorpus.append(filtered_str_from_one_file)
       ### after getting the text , getthe labels
       completeLabels.append(defectStatus)
   return completeCorpus, completeLabels


def executeTokenization(tokenTuple):
  iac_vectorizer = CountVectorizer(min_df=1)
  all_features  = iac_vectorizer.fit_transform(tokenTuple)
  ###print fitted_model
  ## get feature names
  feature_names = iac_vectorizer.get_feature_names()
  print "The words are:", feature_names

print "Started at", utility.giveTimeStamp()
print "-"*125
dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
### this is a lsit of strings ... each string si pre-processed , and correpsonds to all tokens of a file
unfilteredTokensFromFile, defectLabels = getTokensForTokenization(dataset_file)
#print "tokens:{}, labels:{}".format(unfilteredTokensFromFile, defectLabels)
executeTokenization(unfilteredTokensFromFile)
print "Ended at", utility.giveTimeStamp()
print "-"*125
