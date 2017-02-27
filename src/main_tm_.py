'''
Akond Rahman
Feb 26, 2017
'''
import csv, utility, corpCreator, file_mapper, defect_metric
topicCnt = 25
#reff: https://radimrehurek.com/gensim/models/ldamodel.html and https://radimrehurek.com/gensim/tut2.html


def getTokensForTopicModeling(datasetParam):
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
       #print "the list:\n", fileContentAsList
       if (defectStatus=='1'):
         defectedCorpus.append(fileContentAsList)
       else:
         defectFreeCorpus.append(fileContentAsList)
       completeCorpus.append(fileContentAsList)
       #print "="*75
   print "Summary: defected files:{}, defect free files: {}, all files:{}".format(len(defectedCorpus), len(defectFreeCorpus), len(completeCorpus))
   return defectedCorpus, defectFreeCorpus, completeCorpus




def executeTopicModeling(tokenTuple):
   indexCnt=0
   for tokenList in tokenTuple:
      indexCnt = indexCnt + 1
      print "Corpus index:", str(indexCnt)
      fully_processed_corpus = corpCreator.generateCorpus(tokenList)
      #print "Taking a peek", fully_processed_corpus[0]
      #print "="*100
      utility.createCorpusForLDA(fully_processed_corpus, str(indexCnt))
      lda_topic_distr, file_to_topic_prob = utility.performLDA(str(indexCnt), topicCnt)
      ## spit out which tokens constitue each topic
      #print lda_topic_distr
      #print "topic prob. dict=> \n", file_to_topic_prob
      print "*"*75
      topic_file_dict_for_this_corpus = file_mapper.mapTopicToFile(file_to_topic_prob)
      ## spit out legit association (prob >= 0.10) of each file with a topic
      #print topic_file_dict_for_this_corpus
      #print "entries in dict", len(topic_file_dict_for_this_corpus)
      top2defect = file_mapper.mapTopic2Defects(topic_file_dict_for_this_corpus)
      #print top2defect
      ### Metric-1 : Defect Share
      defect_share_of_topics   = defect_metric.getShareOfDefects(top2defect)
      #print defect_share_of_topics
      print "*"*75
      ### Metric-2 : Defect density
      defect_density_of_topics = defect_metric.getDensityOfDefectsForTopic(topic_file_dict_for_this_corpus)
      #print defect_density_of_topics
      ### Metric-3 : NDT for a file
      ndt_for_file = defect_metric.getNDTForFile(defect_density_of_topics, topic_file_dict_for_this_corpus, len(tokenList))
      ### Metric-4 : NT for a file
      nt_for_file = defect_metric.getNTForFile(topic_file_dict_for_this_corpus, len(tokenList))
      #print "lol:\n", nt_for_file
      ### Metric-5 : TM for a file
      tm_for_file = defect_metric.getTMForFile(topic_file_dict_for_this_corpus, len(tokenList), topicCnt, file_to_topic_prob)
      print "tm_for_file (as dict) \n", tm_for_file
      #print "entries in dict", len(top2defect)
      print "*"*75
      print "#"*100




print "Started at", utility.giveTimeStamp()
print "-"*125
dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"
#dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv"
all_three_corpuses = getTokensForTopicModeling(dataset_file)
# full_corpus        = all_three_corpuses[2]
print '-'*125
executeTopicModeling(all_three_corpuses)
# executeTopicModeling(full_corpus)
print '-'*125
print "Ended at", utility.giveTimeStamp()
