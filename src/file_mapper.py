'''
Feb 26, 2017
Akond Rahman
for all file to defect to topic mapping
'''
import csv, collections
theCompleteCategFile = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/New.Categ.csv'
#dataset_file         = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Prediction-Project/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv"

def mapTopicToFile(file2TopicProb):
  topic_and_file_dict = {}
  for cnt_ in xrange(len(file2TopicProb)):
    topicProbTuple = file2TopicProb[cnt_]
    for entry_ in topicProbTuple:
       topic_index = entry_[0]   ## gives topic number e.g. 0 to 49
       topic_prob = entry_[1]    ## gives topic probaility
       if topic_prob >= 0.10:
         if topic_index not in topic_and_file_dict:
            topic_and_file_dict[topic_index] = [cnt_]
         else:
            topic_and_file_dict[topic_index] = topic_and_file_dict[topic_index] + [cnt_]
  return topic_and_file_dict


def getPuppetFileList(dataset_file):
  list2ret = []
  with open(dataset_file, 'rU') as f:
     reader_ = csv.reader(f)
     next(reader_, None)
     for row_ in reader_:
       list2ret.append(row_[1])
  return list2ret


def getPuppetFileDetails():
    dictOfAllFiles={}
    with open(theCompleteCategFile, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
        categ_of_file      = row_[3]
        full_path_of_file  = row_[4]
        if full_path_of_file not in dictOfAllFiles:
            dictOfAllFiles[full_path_of_file] = [ categ_of_file ]
        else:
            dictOfAllFiles[full_path_of_file] = dictOfAllFiles[full_path_of_file] + [ categ_of_file ]

    return dictOfAllFiles

def mapTopic2Defects(topic_file_param, datasetFileParam):
    topic_to_defect_categ_dict = {}
    topic_to_categ_to_ret = {}
    allPuppFiles = getPuppetFileList(datasetFileParam)
    puppetFileDict = getPuppetFileDetails()
    for topic_, mappedFiles in topic_file_param.iteritems():
       for file_index in mappedFiles:
         file_ = allPuppFiles[file_index]
         defect_categ =  puppetFileDict[file_]
         #print defect_categ
         if topic_ not in topic_to_defect_categ_dict:
            topic_to_defect_categ_dict[topic_] = [defect_categ]
         else:
            topic_to_defect_categ_dict[topic_] = topic_to_defect_categ_dict[topic_] + [defect_categ]
    ## convert list of lists to one single list
    for k_, v_ in topic_to_defect_categ_dict.items():
        tmp_=[]
        for elem_list in v_:
            for elem in elem_list:
                tmp_.append(elem)
        topic_to_categ_to_ret[k_] = dict(collections.Counter(tmp_))
    return topic_to_categ_to_ret



def getTopicProbOfTheTopic(topic_, topicProbTuple_, fileIndex_):
  probToRet = 0
  for cnt_ in xrange(len(topicProbTuple_)):
     #print "lol: \n", topicProbTuple_[cnt_]
     if(cnt_ == fileIndex_):
        topicTuple = topicProbTuple_[cnt_]
        for elems in topicTuple:
          topicIndex = elems[0]
          topicProb  = elems[1]
          if(topicIndex==topic_):
            probToRet = topicProb
            probToRet = round(probToRet, 5)
  return probToRet
