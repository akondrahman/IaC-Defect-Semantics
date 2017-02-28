'''
Akond Rahman
Feb 28, 2017
bag of words technique
'''
import csv, utility, tokenization_preprocessor



def getTokensForTokenization(datasetParam):
   completeCorpus    = [] ## a list of lists with tokens from defected and non defected files
   with open(datasetParam, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row in reader_:
       fileToRead   = row[1]
       fileContentAsStr = utility.giveCommentFreeFileContent(fileToRead)
       fileContentAsList = fileContentAsStr.split(' ')
       #print "the list:\n", fileContentAsList
       completeCorpus.append(fileContentAsList)
       #print "="*75
   return completeCorpus


def executeTokenization(tokenTuple):
   indexCnt=0
   for tokenList in tokenTuple:
      indexCnt = indexCnt + 1
      #print "Corpus index:", str(indexCnt)
      fully_processed_corpus = tokenization_preprocessor.processTokensOfFullCorpus(tokenList)
      #print "Taking a peek", fully_processed_corpus[0]
      #print "="*100


print "Started at", utility.giveTimeStamp()
print "-"*125
# dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
unfilteredTokensFromFile = getTokensForTokenization(dataset_file)
executeTokenization(unfilteredTokensFromFile)
print "Ended at", utility.giveTimeStamp()
print "-"*125
