'''
Akond Rahman
Feb 26, 2017
thsi file defect-based metrics needed for the paper
'''




def getShareOfDefects(topicToDefectParam):
   as_defect_per_topic , b_defect_per_topic, c_defect_per_topic, d_defect_per_topic  = 0, 0, 0, 0
   f_defect_per_topic,   i_defect_per_topic, o_defect_per_topic, t_defect_per_topic  = 0, 0, 0, 0
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
