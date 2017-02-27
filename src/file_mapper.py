'''
Feb 26, 2017
Akond Rahman
for all file to defect to topic mapping
'''




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
