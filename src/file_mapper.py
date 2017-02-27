'''
Feb 26, 2017
Akond Rahman
for all file to defect to topic mapping
'''
theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/New.Categ.csv'



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
            dictOfAllFiles[full_path_of_file][0] = dictOfAllFiles[full_path_of_file] + [ categ_of_file ]

    return dict2Ret

def mapTopic2DefectDensity(topic_file_param):
    topic_to_defect_categ_dict = {}
    puppetFileDict = getPuppetFileDetails()
    for topic_, mappedFiles in topic_file_param.iteritems():
       for file_ in mappedFiles:
         defect_categ =  puppetFileDict[file_]
         if topic_ not in topic_to_defect_categ_dict:
            topic_to_defect_categ_dict[topic_] = [defect_categ]
         else:
            topic_to_defect_categ_dict[topic_] = topic_to_defect_categ_dict[topic_] + [defect_categ]
    return topic_to_defect_categ_dict        
