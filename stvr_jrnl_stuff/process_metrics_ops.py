'''
Author metrics for operations 
Akond Rahman 
April 05, 2019 
'''

import os, subprocess, numpy as np, operator
from  collections import Counter
from  scipy.stats import entropy
import pandas as pd 

monthDict            = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)


def getHgUniqueDevCount(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = "hg churn --diffstat  " + theFile + " | awk '{print $1}'  "
   command2Run = cdCommand + commitCountCmd 

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   author_count        = len(np.unique(author_count_output))

   return author_count

def getGitUniqueDevCount(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   author_count        = len(np.unique(author_count_output))

   return author_count

def getHgMinorContribCount(param_file_path, repo_path, sloc):
   minorList = []
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " hg annotate -u " + theFile + " | cut -d':' -f1 "
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']
   author_contrib = dict(Counter(blame_output))

   for author, contribs in author_contrib.items():
      if((float(contribs)/float(sloc)) < 0.05):
          minorList.append(author)
   return len(minorList)


def getGitMinorContribCount(param_file_path, repo_path, sloc):
   minorList = []
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']
   author_contrib = dict(Counter(blame_output))

   for author, contribs in author_contrib.items():
      if((float(contribs)/float(sloc)) < 0.05):
        minorList.append(author)
   return len(minorList)

def getHgHighestContribsPerc(param_file_path, repo_path, sloc):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " hg annotate -u " + theFile + " | cut -d':' -f1 "
   command2Run       = cdCommand + blameCommand

   blame_output     = subprocess.check_output(['bash','-c', command2Run])
   blame_output     = blame_output.split('\n')
   blame_output     = [x_ for x_ in blame_output if x_!='']
   if (len(blame_output) > 0):
       author_contrib   = dict(Counter(blame_output))
       highest_author   = max(author_contrib.iteritems(), key=operator.itemgetter(1))[0]
       highest_contr    = author_contrib[highest_author]
   else:
       highest_contr    = 0
   if(sloc > 0):
       val2ret = (round(float(highest_contr)/float(sloc), 5))*100
   else:
       val2ret = 0
   return val2ret


def getGitHighestContribsPerc(param_file_path, repo_path, sloc):
   owner_contrib = 0 
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output     = subprocess.check_output(['bash','-c', command2Run])
   blame_output     = blame_output.split('\n')
   blame_output     = [x_ for x_ in blame_output if x_!='']
   author_contrib   = dict(Counter(blame_output))

   if (len(author_contrib) > 0):
     highest_author   = max(author_contrib.iteritems(), key=operator.itemgetter(1))[0]
     highest_contr    = author_contrib[highest_author]
   else:
     highest_contr = 0
   if sloc <= 0 :
       sloc += 1
   owner_contrib = (round(float(highest_contr)/float(sloc), 5))
   return owner_contrib

def calculateMonthDiffFromTwoDates(early, latest):
    from datetime import datetime
    early_year   = early.split('-')[0]
    latest_year  = latest.split('-')[0]
    early_month  = early.split('-')[1]
    latest_month = latest.split('-')[1]
    early_day    = early.split('-')[-1]
    latest_day   = latest.split('-')[-1]

    early_dt     = datetime(int(early_year), int(early_month), int(early_day))
    latest_dt    = datetime(int(latest_year), int(latest_month), int(latest_day))

    return (latest_dt.year - early_dt.year)*12 + latest_dt.month - early_dt.month


def getHgAge(param_file_path, repo_path):
   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = " hg churn --dateformat '%Y-%m-%d' " +  theFile +    " | awk '{print $1 }' "
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   monthAndYeatList = [x_ for x_ in dt_churn_output if x_!='']
   
   monthAndYeatList.sort()
   
   earliesttMonth  = monthAndYeatList[0]
   latesttMonth    = monthAndYeatList[-1]
   age = calculateMonthDiffFromTwoDates(earliesttMonth, latesttMonth)
   
   return age


def getGitAge(param_file_path, repo_path):
   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   
   monthList = [dob[0:3] for dob in  dt_churn_output]
   yearist = [dob[-4:] for dob in  dt_churn_output]
   monthAndYeatList = [dob[-4:] + '-' + monthDict[dob[0:3]] for dob in dt_churn_output]
   monthAndYeatList.sort()
   
   earliesttMonth  = monthAndYeatList[0]
   latesttMonth    = monthAndYeatList[-1]
   age = str(calculateMonthDiffFromTwoDates(earliesttMonth, latesttMonth))
   
   return age

def getProcessMetrics(file_path_p):
    LOC          = sum(1 for line in open(file_path_p))
    splitted_file_path = file_path_p.split('/') 
    splitted_file_path = splitted_file_path[0:6] 
    repo_path = '/'.join(splitted_file_path) 
    repo_path_p = repo_path + '/'

    if('mozilla' in file_path_p):
        DEV          = getHgUniqueDevCount(file_path_p, repo_path_p)
        MINOR        = getHgMinorContribCount(file_path_p, repo_path_p, LOC)
        OWNER_LINES  = getHgHighestContribsPerc(file_path_p, repo_path_p, LOC)
        AGE          = getHgAge(file_path_p, repo_path_p) 
    else:
        DEV          = getGitUniqueDevCount(file_path_p, repo_path_p)
        MINOR        = getGitMinorContribCount(file_path_p, repo_path_p, LOC)
        OWNER_LINES  = getGitHighestContribsPerc(file_path_p, repo_path_p, LOC)
        AGE          = getGitAge(file_path_p, repo_path_p)         

    all_process_metrics = str(DEV) + ',' + str(MINOR) + ',' + str(OWNER_LINES) + ',' + str(AGE) 

    return all_process_metrics 

if __name__=='__main__':
    # OPS_MAP_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/LABELED_MIRANTIS_OPERATION_MAPPING_DATASET.csv'
    # OPS_MAP_OUT = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/PROCESS_MIRANTIS_OPERATION_DATASET.csv'

    # OPS_MAP_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/LABELED_MOZILLA_OPERATION_MAPPING_DATASET.csv'
    # OPS_MAP_OUT = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/PROCESS_MOZILLA_OPERATION_DATASET.csv'

    # OPS_MAP_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/LABELED_OPENSTACK_OPERATION_MAPPING_DATASET.csv'
    # OPS_MAP_OUT = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/PROCESS_OPENSTACK_OPERATION_DATASET.csv'    

    # OPS_MAP_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/LABELED_WIKIMEDIA_OPERATION_MAPPING_DATASET.csv'
    # OPS_MAP_OUT = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/PROCESS_WIKIMEDIA_OPERATION_DATASET.csv'    

    ALL_DF = pd.read_csv(OPS_MAP_FIL)   
    ALL_FILES = ALL_DF['FILE_PATH'].tolist() 
    full_out_str  = ''
    for indi_file in ALL_FILES:
        #FILE_FLAG	USER_FLAG	DB_FLAG	WEB_FLAG	ANAL_FLAG
        FILE_OPS_FLAG = ALL_DF[ALL_DF['FILE_PATH']==indi_file]['FILE_FLAG'].tolist()[0] 
        USER_OPS_FLAG = ALL_DF[ALL_DF['FILE_PATH']==indi_file]['USER_FLAG'].tolist()[0] 
        
        DBAS_OPS_FLAG = ALL_DF[ALL_DF['FILE_PATH']==indi_file]['DB_FLAG'].tolist()[0] 
        WEBS_OPS_FLAG = ALL_DF[ALL_DF['FILE_PATH']==indi_file]['WEB_FLAG'].tolist()[0] 
        ANAL_OPS_FLAG = ALL_DF[ALL_DF['FILE_PATH']==indi_file]['ANAL_FLAG'].tolist()[0]     

        per_file_metrics = getProcessMetrics(indi_file) 
        # print indi_file, per_file_metrics, FILE_OPS_FLAG, USER_OPS_FLAG, DBAS_OPS_FLAG, WEBS_OPS_FLAG, ANAL_OPS_FLAG  
        full_out_str = full_out_str + indi_file + ',' + per_file_metrics + ',' + str(FILE_OPS_FLAG) + ',' + str(USER_OPS_FLAG) + ',' + str(DBAS_OPS_FLAG) + ',' + str(WEBS_OPS_FLAG) + ',' + str(ANAL_OPS_FLAG) + '\n'
    
    dumpContentIntoFile(full_out_str, OPS_MAP_OUT) 