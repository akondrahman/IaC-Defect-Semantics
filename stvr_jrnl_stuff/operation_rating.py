'''
Akond Rahman
Oct 10, 2017
Rate operation type in IaC
'''
import csv
import cPickle as pickle
import csv, utility, tokenization_preprocessor, numpy as np, tokenization_predictor

def getKWs(file_name_param):
    file_kws, user_kws, db_kws, web_kws, anal_kws = [], [], [], [], []
    with open(file_name_param, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row_ in reader_:
             file_kws.append(row_[0])
             user_kws.append(row_[1])
             db_kws.append(row_[2])
             web_kws.append(row_[3])
             anal_kws.append(row_[4])

    all_kws_tuple = (file_kws, user_kws, db_kws, web_kws, anal_kws)
    return all_kws_tuple

def getTokensForTokenization(datasetParam):
   completeLabels    = []
   completeCorpus    = [] ## a list of lists with tokens from defected and non defected files
   file_names        = []
   '''
   token holders for manual/topic modeling
   '''
   defective_tokens, non_defective_tokens = [], []
   with open(datasetParam, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row in reader_:
       defectStatus = int(row[20])  ### need to convert to int , otherwise gives error for sklearn.are_under_roc
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
       ### lsit of file names
       file_names.append(fileToRead)

   return completeCorpus, completeLabels, file_names


if __name__=='__main__':
    # theFile = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/WIKIMEDIA_GT_KW.csv'
    # ds_path = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv'
    # ds_name = 'WIKIMEDIA'

    # theFile = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/MOZILLA_GT_KW.csv'
    # ds_path = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv'
    # ds_name = 'MOZILLA'

    # theFile = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/OPENSTACK_GT_KW.csv'
    # ds_path = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_OPENSTACK_FULL_DATASET.csv'
    # ds_name = 'OPENSTACK'

    kws_tup = getKWs(theFile)
    type_li = ['FILE', 'USER', 'DB', 'WEB', 'ANALYTICS']
    counter = 0
    all_file_all_type =[]
    filesInDataset, labelsInDataset, file_names = getTokensForTokenization(ds_path)
    #print kws_tup[0]
    already_seen = []
    for kw_list in kws_tup:
        kw_list = [y_ for y_ in kw_list if len(y_) > 0]
        match_count = 0
        dict_ = {}
        #filesInDataset, labelsInDataset, file_names = getTokensForTokenization(ds_path)
        #print filesInDataset, labelsInDataset
        to_see = 0
        for file_ in filesInDataset:
            fileContentToLook = file_.split(' ')
            if (len(set(kw_list).intersection(set(fileContentToLook))) > 0):
                to_see += 1
        print 'Good luck, to see:', to_see
        print '='*25
        file_counter = 0
        match_count_manual = 0
        for file2Look in filesInDataset:
            fileContentToLook = file2Look.split(' ')
            #if(set(kw_list).issubset(file2Look)):  ### check all
            #print kw_list, fileContentToLook
            kw_list = [x_ for x_ in kw_list if len(x_) > 0]
            file_name = file_names[file_counter]
            if((len(set(kw_list).intersection(set(fileContentToLook))) > 0) and (file_counter < len(file_names)) and (file_name not in already_seen)):   ### check any
               match_count += 1
               print '='*25
               with open(file_name, 'r') as myfile_:
                    data_ = myfile_.read()
               print data_
               print '='*25
               already_seen.append(file_name)
               #print 'Is it related to:', type_li[counter]
               #print '='*25
               #type_rating = raw_input('Type in the first character for category (File:f, db:db, analytics:a, web:w, user:u, add + to idnictae multiple)=====>')
               #print '='*25
               #if (file2Look not in dict_):
               #   dict_[file_name] = type_rating
               #print 'LOCKED ANSWER=>FILE:{}, STATUS:{}, DEFECT?:{}'.format(file_name, type_rating, labelsInDataset[file_counter])
               #print '='*25
            file_counter += 1
        all_file_all_type.append(dict_)
        print dict_
        print '='*50
        print 'Matched files via keyword:', match_count
        print '='*50
        counter += 1
    file2save = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/results/' + ds_name + 'GT.DICT.DUMP'
    pickle.dump(all_file_all_type, open(file2save, 'wb'))
