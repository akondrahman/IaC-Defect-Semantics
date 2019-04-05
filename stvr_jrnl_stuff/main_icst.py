'''
Akond Rahman
Feb 28, 2017
bag of words technique
'''
import csv, utility, tokenization_preprocessor, numpy as np, tokenization_predictor
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import cPickle as pickle

'''
ICST: GT:TABLE:EXAMPLES
'''
def getICSTFilesForExa(datasetParam, kw_param):
   completeLabels    = []
   completeCorpus    = [] ## a list of lists with tokens from defected and non defected files
   with open(datasetParam, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row in reader_:
       # defectStatus = int(row[20])  ### need to convert to int , otherwise gives error for sklearn.are_under_roc
       defectStatus = int(row[-1])  ### need to convert to int , otherwise gives error for sklearn.are_under_roc
       fileToRead   = row[1]
       fileContentAsStr = utility.giveCommentFreeContentFromFile(fileToRead)
       #print "!"*75
       #print fileContentAsStr
       filtered_str_from_one_file = tokenization_preprocessor.processTokensOfOneFile(fileContentAsStr)
       #print len(filtered_str_from_one_file)
       #print "="*75
       if ((kw_param in filtered_str_from_one_file) and (defectStatus==1)):
           print '-'*25
           print fileToRead
           print '-'*25
           print filtered_str_from_one_file
           print '-'*25

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

def getCommitLevelTokensForTokenization(categ_file_param, the_flag):
   completeLabels    = []
   completeCorpus    = [] ## a list of lists with tokens from defected and non defected files
   with open(categ_file_param, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row in reader_:
       id_ = row[0]
       repo_path = row[1]
       catgeg_ = row[3]
       if catgeg_=='N':
           defectStatus = 0
       else:
           defectStatus = 1
       if repo_path[-1]!='/':
           repo_path = repo_path + '/'
       fileToRead = repo_path + 'diffs/' + str(id_) + '.txt'
       commitContentAsStr = utility.giveCommentFreeContentFromFile(fileToRead, the_flag)
       #print commitContentAsStr
       #print "!"*75
       filtered_str_from_one_commit = tokenization_preprocessor.processTokensOfOneFile(commitContentAsStr)
       #print filtered_str_from_one_commit
       #print "="*75
       completeCorpus.append(filtered_str_from_one_commit)
       ### after getting the text , getthe labels
       completeLabels.append(defectStatus)
   #print len(completeCorpus), len(completeLabels)
   return completeCorpus, completeLabels

def executeTokenizationAndPred(iterDumpDir, tokenTuple, labels, reproc_dump_output_file, count_vec_flag_param=True):
  if  count_vec_flag_param:
      iac_vectorizer        = CountVectorizer(min_df=1)
      transformed_features   = iac_vectorizer.fit_transform(tokenTuple)
      feature_names = iac_vectorizer.get_feature_names()
  else:
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
  tokenization_predictor.performPrediction(iterDumpDir, all_features, labels, feature_names, count_vec_flag_param)
  print "="*100

if __name__=='__main__':
    print "Started at", utility.giveTimeStamp()
    print "-"*125
    dir2save='/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/output/'

    # dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/MIRANTIS_FULL_DATASET.csv"
    # reproc_dump_output_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_MIR.dump'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
    # reproc_dump_output_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_MIR.csv'

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

    '''
    prediction time!
    '''
    count_vec_flag = False   # when set to False TF-IDF will occur
    executeTokenizationAndPred(dir2save, unfilteredTokens, defectLabels, reproc_dump_output_file, count_vec_flag)
    print "The dataset was:", dataset_file
    print "-"*100
    print "Ended at", utility.giveTimeStamp()
    print "-"*100
