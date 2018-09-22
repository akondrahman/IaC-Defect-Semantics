'''
Akond Rahman
March 04, 2017
Compare corpuses: defected and non-defected
'''



import compare_corpus
import csv, utility, tokenization_preprocessor, numpy as np
from sklearn.feature_extraction.text import CountVectorizer


def getTokensForTokenization(datasetParam):
   defectedCorpus       = [] ## a list of lists with tokens from defected files
   nonDefectedCorpus    = [] ## a list of lists with tokens from non defected files
   completeCorpus       = [] ## a list of lists with tokens from all files
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
       if (defectStatus==1):
          defectedCorpus.append(filtered_str_from_one_file)
       else:
          nonDefectedCorpus.append(filtered_str_from_one_file)

   return defectedCorpus, nonDefectedCorpus, completeCorpus



print "Started at", utility.giveTimeStamp()
print "-"*125
# dataset_file = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
# file_to_save = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/results/with.tfidf.corp.comp.three.datasets/moz_corpus_diff_metric.csv'

# dataset_file   = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_OPENSTACK_FULL_DATASET.csv"
# file_to_save = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/results/with.tfidf.corp.comp.three.datasets/ost_corpus_diff_metric.csv'

# dataset_file   = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
# file_to_save = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/results/with.tfidf.corp.comp.three.datasets/wik_corpus_diff_metric.csv'

defCorpus, nonDefCorpus, fullCorpus = getTokensForTokenization(dataset_file)
###print len(fullCorpus)
####output_similarity = compare_corpus.compareCorpusesViaSimilarity(defCorpus, nonDefCorpus)
####print "Based on tf-idf the similarity score between two corpuses:", output_similarity
print "-"*125
compare_corpus.statisticallyCompareTF(defCorpus, nonDefCorpus, fullCorpus, file_to_save)
print "-"*125
print "Ended at", utility.giveTimeStamp()
print "-"*125
print "The dataset was:", dataset_file
print "-"*125
