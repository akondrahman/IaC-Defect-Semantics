'''
Akond Rahman 
Sep 22 2018 
Hash vectorizer for STVR 
'''

#  vectorizer = HashingVectorizer(stop_words='english', alternate_sign=False, n_features=opts.n_features)

import csv, utility, tokenization_preprocessor, numpy as np, tokenization_predictor
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
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
  iac_tfidf_vectorizer  = TfidfVectorizer(min_df=1)
  transformed_features   = iac_tfidf_vectorizer.fit_transform(tokenTuple)
  feature_names = iac_tfidf_vectorizer.get_feature_names()


  print "Total number of features used:", len(feature_names)
  print "*"*50
  # Step-1: convert to array
  all_features = transformed_features.toarray()
  print len(all_features)
  print '*'*50
  # Step-2:Sum up the counts of each vocabulary word
  dist = np.sum(all_features, axis=0)   #interesting but not used
  '''
  convert fitted matrix to pandas dataframe: not using CSV, dumping list of strings as pickle in line#80
  '''
  # df_ = utility.dumpTransformedTokenMatrixToCSV(transformed_features, feature_names, reproc_dump_output_file)
  # print df_.shape
  # print 'Dumping completed ...'

  '''
  and then call prediction module
  '''
  tokenization_predictor.performPredictionForHashVectorizer(iterDumpDir, all_features, labels, feature_names)
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
