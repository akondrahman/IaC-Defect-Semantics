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

    print 'FILE=>', mir_file_list
    print 'USER=>', mir_user_list
    print 'DBAS=>', mir_db_list
    print 'WEB==>', mir_web_list
    print 'ANAL=>', mir_ana_list                