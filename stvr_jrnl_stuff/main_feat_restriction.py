'''
Akond Rahman
Oct 18 2018 
STVR Journal Work 
'''
import csv, utility, tokenization_preprocessor, numpy as np, tokenization_predictor
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import cPickle as pickle
import os 

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

def xformForSelectiveFeature(feat_list, sel_feat_count):
    out_lis = []
    end_ptr = sel_feat_count + 1
    for file_list in feat_list:
      ls_   = list(file_list)
      ls_.sort(reverse=True)
      #print len(ls_)
      if len(ls_) > end_ptr:
         tmp_lis = ls_[0: end_ptr]
         out_lis.append(tmp_lis)

    return out_lis

def executeTokenizationAndPred(iterDumpDir, tokenTuple, labels, reproc_dump_output_file, sel_cnt, count_vec_flag_param=True):
  if  count_vec_flag_param:
      iac_vectorizer        = CountVectorizer(min_df=1)
      transformed_features   = iac_vectorizer.fit_transform(tokenTuple)
      feature_names = iac_vectorizer.get_feature_names()
  else:
      iac_tfidf_vectorizer  = TfidfVectorizer(min_df=1)
      transformed_features   = iac_tfidf_vectorizer.fit_transform(tokenTuple)
      feature_names = iac_tfidf_vectorizer.get_feature_names()


  print "Total number of features in the dataset:", len(feature_names)
  print "*"*50
  # Step-1: convert to array
  all_features = transformed_features.toarray()
  #print all_features   ### list of list: each entry is the tfidf
  #print len(all_features)
  #print '*'*50
  # Step-2:Sum up the counts of each vocabulary word
  dist = np.sum(all_features, axis=0)   #interesting but not used
  '''
  convert fitted matrix to pandas dataframe: not using CSV, dumping list of strings as pickle in line#80
  '''
  # df_ = utility.dumpTransformedTokenMatrixToCSV(transformed_features, feature_names, reproc_dump_output_file)
  # print df_.shape
  # print 'Dumping completed ...'
  '''
  for feature selection experience 
  '''
  all_features = xformForSelectiveFeature(all_features, sel_cnt)
  #print all_features
  #print '*'*50
  '''
  and then call prediction module
  '''
  all_learner_res = tokenization_predictor.performPrediction(iterDumpDir, all_features, labels, feature_names, count_vec_flag_param)
  print "="*100
  return all_learner_res

def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)

def printResult(learner_res, top_cnt, learner_name):
    str2ret = ''
    perf_ = {0:'AUC', 1:'PRE', 2:'REC', 3:'FME', 4:'ACC',  5:'GMN'}
    for ind_ in xrange(len(learner_res)):
        perf_list = learner_res[ind_]
        print '*'*25
        print learner_name
        print 'PERFORMANCE MEASURE:{}, MEDIAN VALUES:{}'.format(perf_[ind_], np.median(perf_list))
        print '*'*25
        str2ret = str2ret + str(top_cnt) + ',' + learner_name + ',' + perf_[ind_] + ',' + str(np.median(perf_list)) + '\n'
    return str2ret
    

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
    # reproc_dump_output_file= '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/reproc/TFIDF_MOZILLA_AUG31.csv'

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
    '''
    ICST STUFF
    '''
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
    count_vec_flag = False # when set to False TF-IDF will occur, True will make BOW occur 
    '''
    for getting the top X features 
    '''
    full_str = ''
    # selective_top_count_list = [100, 250, 500, 750, 1000, 1250, 1500] ## MIR, MOZ
    # selective_top_count_list = [100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500]  ## OST 
    # selective_top_count_list = [100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250]  ## WIK    

    for selective_top_count in selective_top_count_list:
        all_learner_res = executeTokenizationAndPred(dir2save, unfilteredTokens, defectLabels, reproc_dump_output_file, selective_top_count, count_vec_flag)
        dt_res, knn_res, rf_res, sv_res, lr_res, nb_res = all_learner_res
        print '='*75 
        print 'Number of features selcted:', selective_top_count
        cart_res_str = printResult(dt_res,  selective_top_count, 'CART')
        knn_res_str_ = printResult(knn_res, selective_top_count, 'KNN')
        lr_res_str_  = printResult(lr_res,  selective_top_count, 'LR')
        nb_res_str_  = printResult(nb_res,  selective_top_count, 'NB')
        rf_res_str_  = printResult(rf_res,  selective_top_count, 'RF')
        svm_res_str  = printResult(sv_res,  selective_top_count, 'SVM')
        print '='*75
        full_str = full_str + cart_res_str + knn_res_str_ + lr_res_str_ + nb_res_str_ + rf_res_str_ + svm_res_str
    
    print "The dataset was:", dataset_file
    print "-"*100
    dumpContentIntoFile(full_str, dir2save + 'FINAL_FEAT_RESTRICTION.csv')
    print "Ended at", utility.giveTimeStamp()
    print "-"*100
