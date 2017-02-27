'''
Akond Rahman
Feb 26, 2017
thsi file defect-based metrics needed for the paper
'''




def getShareOfDefects(topicToDefectParam):
   tot_defect = 0
   dict_={}
   topic_defect_share_dict={}
   for topic_, defectList in topicToDefectParam.items():
     tot_defect_per_top = 0
     al_defect_per_topic = defectList['AL']
     as_defect_per_topic = defectList['AS']
     b_defect_per_topic  = defectList['B']
     c_defect_per_topic  = defectList['C']
     d_defect_per_topic  = defectList['D']
     f_defect_per_topic  = defectList['F']
     i_defect_per_topic  = defectList['I']
     o_defect_per_topic  = defectList['O']
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
