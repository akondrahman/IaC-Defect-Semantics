'''
Akond Rahman 
Sep 22 2018 
Hash vectorizer for STVR 
'''
# reff: https://datascience.stackexchange.com/questions/22250/what-is-the-difference-between-a-hashing-vectorizer-and-a-tfidf-vectorizer

import csv, utility, tokenization_preprocessor, numpy as np, tokenization_predictor
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
import cPickle as pickle

def getTokensForTokenization(datasetParam):
   completeLabels    = []
   completeCorpus    = [] ## a list of lists with tokens from defected and non defected files
   '''
   token holders for manual/topic modeling
   '''
   defective_tokens, non_defective_tokens = [], []
   with open(datasetParam, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row in reader_:
       defectStatus = int(row[-1])  ### need to convert to int , otherwise gives error for sklearn.are_under_roc
       fileToRead   = row[1]
       fileContentAsStr = utility.giveCommentFreeContentFromFile(fileToRead)
       #print "!"*75
       #print fileContentAsStr
       filtered_str_from_one_file = tokenization_preprocessor.processTokensOfOneFile(fileContentAsStr)
       #print len(filtered_str_from_one_file)
       #print "="*75
       completeCorpus.append(filtered_str_from_one_file)
       ### after getting the text , getthe labels
       completeLabels.append(defectStatus)

   return completeCorpus, completeLabels

def executeTokenizationAndPred(iterDumpDir, tokenTuple, labels, reproc_dump_output_file ):

  hash_vectorizer = HashingVectorizer()
  transformed_features   = hash_vectorizer.fit_transform(tokenTuple) 

  all_features = transformed_features.toarray()
  print len(all_features)
  print '*'*50

  '''
  and then call prediction module
  '''
  tokenization_predictor.performPredictionForHashVectorizer(iterDumpDir, all_features, labels)
  print "="*100

if __name__=='__main__':
    print "Started at", utility.giveTimeStamp()
    print "-"*125
    dir2save='/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/output/'

    dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/MIRANTIS_FULL_DATASET.csv"
    reproc_dump_output_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_MIR.dump'
    theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
    reproc_dump_output_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_MIR.csv'

    # dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
    # reproc_dump_output_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_MOZILLA.dump'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
    # reproc_dump_output_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_MOZILLA.csv'

    # dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/SYNTHETIC_OPENSTACK_FULL_DATASET.csv"
    # reproc_dump_output_file='/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_OPENSTACK.dump'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.WithoutBadBoys.Final.Categ.csv'
    # reproc_dump_output_file='/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_OPENSTACK.csv'

    # dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'
    # reproc_dump_output_file='/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_WIKIMEDIA.dump'
    # reproc_dump_output_file='/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_WIKIMEDIA.csv'

    print "The dataset is:", dataset_file
    print "-"*100
    #getICSTFilesForExa(dataset_file, 'user')  ###for example

    unfilteredTokensFromFile, defectLabels = getTokensForTokenization(dataset_file)
    #print "tokens:{}, labels:{}".format(unfilteredTokensFromFile, defectLabels)
    ### this is a list of strings ... each string si pre-processed , and correpsonds to all tokens of a file
    data_dump = (unfilteredTokensFromFile, defectLabels)
    unfilteredTokens = unfilteredTokensFromFile
    '''
    dump corpus and defect labels as pickle
    '''
    pickle.dump( data_dump, open( reproc_dump_output_file, "wb" ) )

    executeTokenizationAndPred(dir2save, unfilteredTokens, defectLabels, reproc_dump_output_file)
    print "The dataset was:", dataset_file
    print "-"*100
    print "Ended at", utility.giveTimeStamp()
    print "-"*100
