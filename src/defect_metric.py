'''
Akond Rahman
Feb 26, 2017
thsi file defect-based metrics needed for the paper
'''
import file_mapper, collections, numpy as np



def getShareOfDefects(topicToDefectParam):
   al_defect_per_topic, as_defect_per_topic , b_defect_per_topic, c_defect_per_topic  = 0, 0, 0, 0
   d_defect_per_topic,  f_defect_per_topic,   i_defect_per_topic, t_defect_per_topic  = 0, 0, 0, 0
   o_defect_per_topic = 0
   tot_defect = 0
   dict_={}
   topic_defect_share_dict={}
   for topic_, defectList in topicToDefectParam.items():
     tot_defect_per_top = 0
     if 'AL' in defectList:
       al_defect_per_topic = defectList['AL']
     elif 'AS' in defectList:
       as_defect_per_topic = defectList['AS']
     elif 'B' in defectList:
       b_defect_per_topic  = defectList['B']
     elif 'C' in defectList:
       c_defect_per_topic  = defectList['C']
     elif 'D' in defectList:
       d_defect_per_topic  = defectList['D']
     elif 'F' in defectList:
       f_defect_per_topic  = defectList['F']
     elif 'I' in defectList:
       i_defect_per_topic  = defectList['I']
     elif 'O' in defectList:
       o_defect_per_topic  = defectList['O']
     elif 'T' in defectList:
       t_defect_per_topic  = defectList['T']
     ### now sum up
     tot_defect_per_top  = (
                            al_defect_per_topic + as_defect_per_topic + b_defect_per_topic + c_defect_per_topic +
                            d_defect_per_topic  + f_defect_per_topic  + i_defect_per_topic + o_defect_per_topic +
                            t_defect_per_topic
                            )
     tot_defect = tot_defect + tot_defect_per_top
     dict_[topic_] = tot_defect_per_top

   for topic_, defect_share_topic in dict_.items():
     topic_defect_share_dict[topic_] = float(defect_share_topic)/float(tot_defect)

   return topic_defect_share_dict





def getDensityOfDefectsForTopic(topicToDefectParam):
    topic_to_defect_categ_dict = {}
    topic_to_defect_density_   = {}
    allPuppFiles   = file_mapper.getPuppetFileList()
    puppetFileDict = file_mapper.getPuppetFileDetails()
    for topic_, mappedFiles in topicToDefectParam.iteritems():
       for file_index in mappedFiles:
         file_ = allPuppFiles[file_index]
         defect_categ =  puppetFileDict[file_]
         #print defect_categ
         if topic_ not in topic_to_defect_categ_dict:
            topic_to_defect_categ_dict[topic_] = [defect_categ]
         else:
            topic_to_defect_categ_dict[topic_] = topic_to_defect_categ_dict[topic_] + [defect_categ]
    ## convert list of lists to one single list
    ## this dictionary holds topic to category mapping
    tmp_dict={}
    for k_, v_ in topic_to_defect_categ_dict.items():
        tmp_=[]
        for elem_list in v_:
            for elem in elem_list:
                if elem !='N':
                  tmp_.append(elem)
        tmp_dict[k_] = dict(collections.Counter(tmp_))
    ## we extracted thec ategories per each topic, lets use them to get the defetc density metric
    for topic_, mappedFiles in topicToDefectParam.iteritems():
       loc_per_topic    = 0
       defect_per_topic = 0
       for file_index in mappedFiles:
         file_          = allPuppFiles[file_index]
         sloc_file_     = sum(1 for line in open(file_))
         loc_per_topic  = loc_per_topic + sloc_file_
       categories = tmp_dict[topic_]
       ## this is the dictioanry of categories only: each ket is a category
       for k_, v_ in categories.items():
          defect_per_topic = defect_per_topic + v_
       topic_to_defect_density_[topic_] = float(defect_per_topic) / float(loc_per_topic)
    return topic_to_defect_density_


def getMatchedTopics(fileIndexParam, topicFileDictParam):
    matchedTopicList = []
    for topic_, fileList in topicFileDictParam.items():
      for file_ in fileList:
        if file_==fileIndexParam:
          matchedTopicList.append(file_)
    return matchedTopicList



def getStatofValueDict(dictOfValues):
    tmp_ = []
    for k_, v_ in dictOfValues.items():
      tmp_.append(v_)
    return np.median(tmp_), np.mean(tmp_)
def getNDTForFile(defect_density_, topic_file_dict_, count_of_files_in_corpus):
  dict_file_NDT    = {}
  median_, mean_   = getStatofValueDict(defect_density_)
  allPuppFiles     = file_mapper.getPuppetFileList()
  for file_index in xrange(count_of_files_in_corpus):
    file_name      = allPuppFiles[file_index]
    matchingTopics = getMatchedTopics(file_index)
    tmp_ndt_holder = []
    for mTop in matchingTopics:
        density_of_topic = defect_density_[mTop]
        if (density_of_topic > mean_):
          tmp_ndt_holder.append(mTop)
    dict_file_NDT[file_name] = tmp_ndt_holder

  return dict_file_NDT
