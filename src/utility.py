'''
utility file for
topic modeling in IaC scripts
Akond Rahman
Feb 26, 2017
'''
import time, datetime, os, sys


def giveCommentFreeFileContent(fileNameParam):
  str2ret=""
  for line_ in open(fileNameParam, 'rU'):
    li=line_.strip()
    if not li.startswith("#"):
      #print line.rstrip()
      str2ret = str2ret + line_.rstrip()

  return str2ret

def giveTimeStamp():

  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret
def readKeywordFile(fileName):
    listToRet = [] ;
    fileO = open(fileName, 'r');
    for line in fileO:
        line = line.strip('\n');
        line = line.strip('\t');
        listToRet.append(line);
    return listToRet ;
