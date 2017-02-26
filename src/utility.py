'''
utility file for
topic modeling in IaC scripts
Akond Rahman
Feb 26, 2017
'''
def giveCommentFreeFileContent(fileNameParam):
  str2ret=""
  for line_ in open(fileNameParam, 'rU'):
    li=line_.strip()
    if not li.startswith("#"):
      #print line.rstrip()
      str2ret = str2ret + line_.rstrip()

  return str2ret




def giveTimeStamp():
  import time, datetime
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret
