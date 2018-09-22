'''
Akond Rahman
March 01, 2017
cross organization
defect prediction
with text mining
'''


import csv, utility, tokenization_preprocessor, numpy as np, cross_org_tokenization_predictor
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

def executeTokenizationAndModeling(tokenTuple, labels):
  iac_vectorizer = CountVectorizer(min_df=1)
  all_features  = iac_vectorizer.fit_transform(tokenTuple)
  ###print fitted_model
  ## get feature names
  feature_names = iac_vectorizer.get_feature_names()
  #print "The words are:", feature_names
  print "Total number of text features used:", len(feature_names)
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
  cross_org_tokenization_predictor.performPrediction(all_features, labels, feature_names)
  print "="*100




print "Started at", utility.giveTimeStamp()
print "-"*125
trainee_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
trainer_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
### this is a lsit of strings ... each string si pre-processed , and correpsonds to all tokens of a file
trainer_unfilteredTokensFromFile, trainer_defectLabels = getTokensForTokenization(trainer_file)
trainee_unfilteredTokensFromFile, trainee_defectLabels = getTokensForTokenization(trainee_file)
executeTokenizationAndModeling(trainer_unfilteredTokensFromFile, trainee_defectLabels)
print "The trainer dataset was:", trainer_file
print "-"*125
print "The trainee dataset was:", trainee_file
print "-"*125
print "Ended at", utility.giveTimeStamp()
print "-"*125
