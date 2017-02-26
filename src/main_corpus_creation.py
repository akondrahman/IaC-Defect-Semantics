'''
Akond Rahman
Feb 26, 2017
'''
import csv
def createCorpusForTopicModeling(datasetParam):
   with open(datasetParam, 'rU') as f:
   reader = csv.reader(f)
   for row in reader:
     fileToRead   = row[1]
     defectStatus = row[20]
     with open(fileToRead, 'rU') as myfile:
      fileContentAsStr  = myfile.read().replace('\n', ' ')
      fileContentAsList = fileContentAsStr.split(' ')
      print "the list:", fileContentAsList
      print "="*100



dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
#dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
createCorpusForTopicModeling(dataset_file)
