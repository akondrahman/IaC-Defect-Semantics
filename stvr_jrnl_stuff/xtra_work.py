'''
Akond Rahman 
April 04, 2019 
get operation mapping 
'''
import pandas as pd 
import os 
import csv 

def getKeywordList(pd_df): 
    file_kws = pd_df['FILE'].tolist()
    user_kws = pd_df['USER'].tolist()
    db_kws   = pd_df['DB'].tolist()
    web_kws  = pd_df['WEB'].tolist()
    ana_kws  = pd_df['ANALYTICS'].tolist()

    return file_kws, user_kws, db_kws, web_kws, ana_kws

def getCommonList(moz, ost, wik):
    inter  = set(moz).intersection(ost) 
    output = set(inter).intersection(wik)     
    return list(output)

def getOperationFrequency(str_lis, ops_kw_lis):
    if (len(str_lis) <= 0):
        str_lis =  str_lis + ['DUMMY'] 
    # print str_lis
    ops_kw_lis = [y_ for y_ in ops_kw_lis if isinstance(y_, basestring) ]
    # print ops_kw_lis
    common_words = [x_ for x_ in str_lis if any(z_ in x_ for z_ in ops_kw_lis) ]

    kw_perc =  (float(len(common_words)) / float(len(str_lis)) ) * 100 
    return kw_perc


def getOperationMapping(file_name, file_kws, user_kws, db_kws, web_kws, ana_kws):
    full_df   = pd.read_csv(file_name)
    file_list = full_df['file_'].tolist() 
    whole_list = []
    for file_path in file_list: 
        if(os.path.exists(file_path)):
            defect_status = full_df[full_df['file_']==file_path]['defect_status'].tolist()[0]
            with open(file_path, 'rU') as file_:
                file_content = file_.readlines()
                file_content = [x_ for x_ in file_content if x_[0] != '#' ]
                file_content = [x_.replace('\n', '') for x_ in file_content  ]
                # print len(file_content ) 
                file_ops_freq = getOperationFrequency(file_content, file_kws) 
                user_ops_freq = getOperationFrequency(file_content, user_kws) 
                dbas_ops_freq = getOperationFrequency(file_content, db_kws) 
                webs_ops_freq = getOperationFrequency(file_content, web_kws) 
                anal_ops_freq = getOperationFrequency(file_content, ana_kws) 

                tup = (file_path, defect_status, file_ops_freq, user_ops_freq, dbas_ops_freq, webs_ops_freq, anal_ops_freq)
                whole_list.append(tup) 
    df_output = pd.DataFrame(whole_list)
    return df_output

def printOpsFreq(file_name):
    mapping_df = pd.read_csv(file_name)
    r_, c_     = mapping_df.shape 
    file_ops_values = mapping_df[mapping_df['FILE_FLAG']>0]['FILE_FLAG'].tolist() 	
    user_ops_values = mapping_df[mapping_df['USER_FLAG']>0]['USER_FLAG'].tolist() 	
    
    dbas_ops_values = mapping_df[mapping_df['DB_FLAG']>0]['DB_FLAG'].tolist() 	
    webs_ops_values = mapping_df[mapping_df['WEB_FLAG']>0]['WEB_FLAG'].tolist() 	
    anal_ops_values = mapping_df[mapping_df['ANAL_FLAG']>0]['ANAL_FLAG'].tolist() 	

    print 'File operations:', (float(len(file_ops_values)) / float(r_))*100
    print 'User operations:', (float(len(user_ops_values)) / float(r_))*100    

    print 'Database operations:', (float(len(dbas_ops_values)) / float(r_))*100
    print 'Website operations:', (float(len(webs_ops_values)) / float(r_))*100  
    print 'Analytical operations:', (float(len(anal_ops_values)) / float(r_))*100          
    print 'Infra provisioning operations:', (float(len(dbas_ops_values) + len(webs_ops_values) + len(anal_ops_values)) / float(r_))*100


if __name__=='__main__':
    kw_list_moz_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/MOZILLA_GT_KW.csv'
    kw_list_ost_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/OPENSTACK_GT_KW.csv'
    kw_list_wik_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/WIKIMEDIA_GT_KW.csv'    

    moz_pd_ = pd.read_csv(kw_list_moz_file)
    ost_pd_ = pd.read_csv(kw_list_ost_file)    
    wik_pd_ = pd.read_csv(kw_list_wik_file)    

    moz_file_list, moz_user_list, moz_db_list, moz_web_list, moz_ana_list = getKeywordList(moz_pd_)
    ost_file_list, ost_user_list, ost_db_list, ost_web_list, ost_ana_list = getKeywordList(ost_pd_)    
    wik_file_list, wik_user_list, wik_db_list, wik_web_list, wik_ana_list = getKeywordList(wik_pd_)    

    mir_file_list = getCommonList(moz_file_list, ost_file_list, wik_file_list)
    mir_user_list = getCommonList(moz_user_list, ost_user_list, wik_user_list)  
    
    mir_db_list = getCommonList(moz_db_list, ost_db_list, wik_db_list)
    mir_web_list = getCommonList(moz_web_list, ost_web_list, wik_web_list)        
    mir_ana_list = getCommonList(moz_ana_list, ost_ana_list, wik_ana_list)        

    # print 'FILE=>', mir_file_list
    # print 'USER=>', mir_user_list
    # print 'DBAS=>', mir_db_list
    # print 'WEB==>', mir_web_list
    # print 'ANAL=>', mir_ana_list 
    # 
    cols = ['FILE_PATH', 'DEFECT_STATUS', 'FILE_PERC', 'USER_PERC', 'DB_PERC', 'WEB_PERC', 'ANAL_PERC']

    # MIR_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/MIRANTIS_FULL_DATASET.csv'
    # MIR_OUTPUT_DF = getOperationMapping(MIR_FIL, mir_file_list, mir_user_list, mir_db_list, mir_web_list, mir_ana_list)  
    # MIR_OUTPUT_DF.to_csv('/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/MIRANTIS_OPERATION_MAPPING_DATASET.csv')

    # MOZ_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/SYNTHETIC_MOZ_FULL_DATASET.csv'
    # MOZ_OUTPUT_DF = getOperationMapping(MOZ_FIL, moz_file_list, moz_user_list, moz_db_list, moz_web_list, moz_ana_list)   
    # MOZ_OUTPUT_DF.to_csv('/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/MOZILLA_OPERATION_MAPPING_DATASET.csv')    

    # OST_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/SYNTHETIC_OPENSTACK_FULL_DATASET.csv'
    # OST_OUTPUT_DF = getOperationMapping(OST_FIL, ost_file_list, ost_user_list, ost_db_list, ost_web_list, ost_ana_list)     
    # OST_OUTPUT_DF.to_csv('/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/OPENSTACK_OPERATION_MAPPING_DATASET.csv')    

    # WIK_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/SYNTHETIC_WIKI_FULL_DATASET.csv'
    # WIK_OUTPUT_DF = getOperationMapping(WIK_FIL, wik_file_list, wik_user_list, wik_db_list, wik_web_list, wik_ana_list)    
    # WIK_OUTPUT_DF.to_csv('/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/WIKIMEDIA_OPERATION_MAPPING_DATASET.csv')     

    # OPS_MAP_MIR_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/LABELED_MIRANTIS_OPERATION_MAPPING_DATASET.csv'
    # OPS_MAP_MOZ_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/LABELED_MOZILLA_OPERATION_MAPPING_DATASET.csv'
    # OPS_MAP_OST_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/LABELED_OPENSTACK_OPERATION_MAPPING_DATASET.csv'
    # OPS_MAP_WIK_FIL = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/LABELED_WIKIMEDIA_OPERATION_MAPPING_DATASET.csv'

    print OPS_MAP_MIR_FIL
    printOpsFreq(OPS_MAP_MIR_FIL)
    print '='*50
    print OPS_MAP_MOZ_FIL
    printOpsFreq(OPS_MAP_MOZ_FIL)
    print '='*50
    print OPS_MAP_OST_FIL
    printOpsFreq(OPS_MAP_OST_FIL)
    print '='*50
    print OPS_MAP_WIK_FIL
    printOpsFreq(OPS_MAP_WIK_FIL)
    print '='*50            
