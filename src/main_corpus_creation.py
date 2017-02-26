'''
Akond Rahman
Feb 26, 2017
'''
import csv, utility
def createCorpusForTopicModeling(datasetParam):
   completeCorpus    = [] ## a list of lists with tokens from defected and non defected files
   defectedCorpus    = [] ## a list of lists with tokens from defected files
   defectFreeCorpus  = [] ## a list of lists with tokens from defect free files
   with open(datasetParam, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row in reader_:
       fileToRead   = row[1]
       defectStatus = row[20]
       fileContentAsStr = utility.giveCommentFreeFileContent(fileToRead)
       fileContentAsList = fileContentAsStr.split(' ')
       print "the list:\n", fileContentAsList
       if (defectStatus=='1'):
         defectedCorpus.append(fileContentAsList)
       else:
         defectedCorpus.append(fileContentAsList)
       completeCorpus.append(fileContentAsList)
       print "="*75
   print "Summary: defected files:{}, defect free files: {}, all files:{}".format(len(defectedCorpus), len(defectFreeCorpus), len(completeCorpus))
   return defectedCorpus, defectFreeCorpus, completeCorpus



print "Started at", utility.giveTimeStamp()
print "-"*125
dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
#dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
createCorpusForTopicModeling(dataset_file)
print '-'*125
print "Ended at", utility.giveTimeStamp()
