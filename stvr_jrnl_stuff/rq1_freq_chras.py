'''
Akond Rahman
Oct 28, 2018
Wednesday
Frequnecy of chars, by loading dictionaries
'''
from collections import Counter
import os, csv
import utility 

def isDefective(file_param, dict_defect_status):
    defect_status_to_ret = False
    if(file_param in dict_defect_status):
        defect_status = dict_defect_status[file_param]
        if(defect_status==1):
            defect_status_to_ret = True
        else:
            defect_status_to_ret = False
    else:
        defect_status_to_ret = False
    return defect_status_to_ret



def getFreq(dict_file_param, defect_dict_p):
    dicts_from_file = []
    with open(dict_file_param,'r') as file_:
         for line in file_:
             dicts_from_file.append(eval(line))
    all_categ_files, categ_defect_files, categ_nondefect_files = [], [], []
    for dict_ in dicts_from_file:
        for file_, catges_ in dict_.iteritems():
            if(isDefective(file_, defect_dict_p)):
                categ_defect_files.append(catges_)
            else:
                categ_nondefect_files.append(catges_)
            #catges_ = catges_.rstrip()
            #for categ_ in catges_:
            all_categ_files.append(catges_)
    print '='*50
    print 'Frequency of operations:fulldictionary:', Counter(all_categ_files)
    print '='*50
    print 'Frequency of operations:defedictionary:', Counter(categ_defect_files)
    print '='*50
    print 'Frequency of operations:nonddictionary:', Counter(categ_nondefect_files)
    print '='*50


def getDefectDict(datasetParam):
    dict2ret={}
    with open(datasetParam, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row in reader_:
             defectStatus = int(row[20])  ### need to convert to int , otherwise gives error for sklearn.are_under_roc
             fileToRead   = row[1]
             dict2ret[fileToRead] = defectStatus
    return dict2ret

def getMirantisDefectiveContent():
    dataset_file="/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/MIRANTIS_FULL_DATASET.csv"
    str_ = ''
    with open(dataset_file, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row in reader_:
             defectStatus = int(row[-1])  ### need to convert to int , otherwise gives error for sklearn.are_under_roc
             fileToRead   = row[1]    
             if (defectStatus == 1):
                if (os.path.exists(fileToRead)):
                   with open(fileToRead, 'rU') as file_:
                        data_str = file_.read() 
                        str_ = str_ + fileToRead + '\n' + '='*100 + '\n' + data_str + '\n' + '='*100 + '\n' + '='*100 + '\n'
    utility.dumpContentIntoFile(str_, '../../../output/MIR_FOR_OPS.txt')


if __name__=='__main__':
    # dict_file   = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/results/gt/res-wiki-get-parsing.txt'
    # defect_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv'

    # dict_file   = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/results/gt/res-ost-get-parsing.txt'
    # defect_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_OPENSTACK_FULL_DATASET.csv'

    # dict_file   = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/results/gt/res-moz-get-parsing.txt'
    # defect_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Semantics/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv'

    # defect_dict = getDefectDict(defect_file)
    # getFreq(dict_file, defect_dict)
    # print 'THE DATASET WAS:', dict_file
    # print '='*100

    getMirantisDefectiveContent()
