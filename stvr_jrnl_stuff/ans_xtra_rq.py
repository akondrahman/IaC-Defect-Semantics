'''
Answer to extra RQs 
Akond Rahman 
April 05, 2019 
'''
import pandas as pd 
import numpy as np 
import os 
import csv 

def getSummary(lis, type_):
    print '-'*25
    print 'Type:{}, Median:{}'.format(type_ , np.median(lis) )
    print 'Type:{}, Mean:{}'.format(type_ , np.median(lis) )
    print 'Type:{}, Max:{}'.format(type_ , max(lis) )
    print '-'*25

def getDatasetSummaries(ds_list):
    OPS_LIST = [ 'FILE_FLAG', 'USER_FLAG', 'DB_FLAG', 'WEB_FLAG', 'ANAL_FLAG']
    for ds_file in ds_list:
        print ds_file
        df_ = pd.read_csv(ds_file)
        for operation in OPS_LIST:
            print operation

            per_op_files  = df_[df_[operation]==1]['FILE_PATH'].tolist() 	
            per_op_devs   = df_[df_[operation]==1]['DEVS'].tolist() 	
            per_op_minors = df_[df_[operation]==1]['MINORS'].tolist() 	
            per_op_owner  = df_[df_[operation]==1]['OWNER_LINES'].tolist() 	
            per_op_age    = df_[df_[operation]==1]['AGE'].tolist() 	
            
            per_op_age    = [x_+1 for x_ in per_op_age if x_==0 ]
            per_op_sloc   = [sum(1 for line in open(y_)) for y_ in per_op_files ]

            getSummary(per_op_devs, 'DEVS')
            getSummary(per_op_minors, 'MINORS')   
            getSummary(per_op_owner, 'OWNER')
            getSummary(per_op_age, 'AGE')                        
            getSummary(per_op_sloc, 'LOC')                        
            print '*'*75
        print '='*100




if __name__=='__main__':
    MIR_OPS_MAP_OUT = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/PROCESS_MIRANTIS_OPERATION_DATASET.csv'
    MOZ_OPS_MAP_OUT = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/PROCESS_MOZILLA_OPERATION_DATASET.csv'
    OST_OPS_MAP_OUT = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/PROCESS_OPENSTACK_OPERATION_DATASET.csv'    
    WIK_OPS_MAP_OUT = '/Users/akond/Documents/AkondOneDrive/OneDrive/stvr/dataset/PROCESS_WIKIMEDIA_OPERATION_DATASET.csv'    

    getDatasetSummaries( [MIR_OPS_MAP_OUT, MOZ_OPS_MAP_OUT, OST_OPS_MAP_OUT, WIK_OPS_MAP_OUT] )

