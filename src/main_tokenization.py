'''
Akond Rahman
Feb 28, 2017
bag of words technique
'''
import csv, utility, tokenization_preprocessor, numpy as np, tokenization_predictor
from sklearn.feature_extraction.text import CountVectorizer


def getTokensForTokenization(datasetParam):
   completeLabels    = []
   completeCorpus    = [] ## a list of lists with tokens from defected and non defected files
   with open(datasetParam, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row in reader_:
       defectStatus = int(row[20])  ### need to convert to int , otherwise gives error for sklearn.are_under_roc
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


def executeTokenization(tokenTuple, labels):
  iac_vectorizer = CountVectorizer(min_df=1)
  all_features  = iac_vectorizer.fit_transform(tokenTuple)
  ###print fitted_model
  ## get feature names
  feature_names = iac_vectorizer.get_feature_names()
  #print "The words are:", feature_names
  print "Total number fo features used:", len(feature_names)
  print "="*100
  '''
  check the freequnecy of each word ... needed for sanity check
  '''
  # Step-1: convert to array
  all_features = all_features.toarray()
  # Step-2:Sum up the counts of each vocabulary word
  dist = np.sum(all_features, axis=0)
  # Step-3: For each, print the vocabulary word and the number of times it
  # appears in the training set
  #for word_, count_ in zip(feature_names, dist):
  #  print "word:[{}]--->count:[{}]".format(word_, count_)
  tokenization_predictor.performPrediction(all_features, labels)
  print "="*100



print "Started at", utility.giveTimeStamp()
print "-"*125
dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
### this is a lsit of strings ... each string si pre-processed , and correpsonds to all tokens of a file
unfilteredTokensFromFile, defectLabels = getTokensForTokenization(dataset_file)
#print "tokens:{}, labels:{}".format(unfilteredTokensFromFile, defectLabels)
executeTokenization(unfilteredTokensFromFile, defectLabels)
print "Ended at", utility.giveTimeStamp()
print "-"*125
