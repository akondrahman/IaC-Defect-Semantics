'''
Akond Rahman
March 03, 2017
tokenization metrics
'''
import csv, utility, tokenization_preprocessor, numpy as np
from sklearn.feature_extraction.text import CountVectorizer


def getTokensForTokenization(datasetParam):
   defectedCorpus       = [] ## a list of lists with tokens from defected files
   nonDefectedCorpus    = [] ## a list of lists with tokens from non defected files
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
       if (defectStatus==1):
          defectedCorpus.append(filtered_str_from_one_file)
       else:
          nonDefectedCorpus.append(filtered_str_from_one_file)

   return defectedCorpus, nonDefectedCorpus




def executeTokenization(corpusParam, labelParam):
  str2write=''
  file2save_ = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/results/tokenization/wordCount_' + labelParam + '.csv'
  print "The labels:", labelParam
  print "="*100
  iac_vectorizer = CountVectorizer(min_df=1)
  all_features  = iac_vectorizer.fit_transform(corpusParam)
  ###print fitted_model
  ## get feature names
  feature_names = iac_vectorizer.get_feature_names()
  #print "The words are:", feature_names
  print "Total number of features used:", len(feature_names)
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
  for word_, count_ in zip(feature_names, dist):
    #print "word:[{}]--->count:[{}]".format(word_, count_)
    str2write = str2write + word_ + ',' + str(count_) + ',' + '\n'
  print "="*100
  stat_ = utility.dumpContentIntoFile(str2write, file2save_)
  print "Dumped a file of {} bytes".format(stat_)
  print "*"*100

print "Started at", utility.giveTimeStamp()
print "-"*125
dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
# dataset_file            = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
defCorpus, nonDefCorpus = getTokensForTokenization(dataset_file)
#print defCorpus
executeTokenization(defCorpus, "D-E-F-E-C-T-E-D C-O-R-P-U-S")
executeTokenization(nonDefCorpus, "N-O-N D-E-F-E-C-T-E-D C-O-R-P-U-S")
