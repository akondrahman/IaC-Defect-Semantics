'''
Akond Rahman
Tokenization based predcition
Feb 28, 2017
'''
from sklearn import decomposition
import numpy as np, sklearn_models, utility
import operator

def getPCAsToExplore(dataset_length, count_vec_flag_param):
    if count_vec_flag_param:
       explore_dict={1383:500, 580:200, 296:150, 180:100, 66:50, 165:100, 286:150, 1142:500, 294:150}

       use_dict={1383:400, 580:140, 296:130, 180:50, 66:16, 165:50, 286:130, 1142:400, 294:150}

    else:
       explore_dict={1383:500, 580:200, 296:150, 180:100, 66:50, 165:100, 286:150, 1142:500, 294:150}

       use_dict={1383:400, 580:140, 296:130, 180:50, 66:16, 165:50, 286:130, 1142:400, 294:150}

    return explore_dict[dataset_length], use_dict[dataset_length], 10

def getPCAsForHashVec(dataset_length):
    explore_dict={1383:500, 580:200, 296:150, 180:125, 66:50, 165:100, 286:150, 1142:500, 294:150}
    use_dict={1383:400, 580:140, 296:130, 180:125, 66:16, 165:50, 286:130, 1142:400, 294:150}
    
    return explore_dict[dataset_length], use_dict[dataset_length], 10

def printPCAInsights(pcaParamObj, no_of_pca_comp_to_see, featureNamesParam):
    '''
    icst work
    '''
    non_zerocontrib_tokens = []
    print '+'*25
    print 'PCA metric importance zone  ...'
    print '+'*25
    counter= 0
    token_contrib_dict = {}
    for comp_index in xrange(no_of_pca_comp_to_see):
        all_metric_value_in_one_component =  np.abs(pcaParamObj.components_[comp_index])
        non_zero_metric_cnt = len([x_ for x_ in all_metric_value_in_one_component if x_ > 0])
        print 'Number of non-zero metrics:{}, of {}'.format(non_zero_metric_cnt, len(all_metric_value_in_one_component))
        print '$'*15
        sorted_all_metric_index_in_one_component = all_metric_value_in_one_component.argsort()[::-1]
        for token_index in sorted_all_metric_index_in_one_component:
            token_name = featureNamesParam[token_index]
            token_score = all_metric_value_in_one_component[token_index]
            token_score_norm = token_score / float(no_of_pca_comp_to_see)
            #print 'Token index:{}, token name:{}, token score:{}'.format(token_index, token_name, token_score)
            if token_name not in token_contrib_dict:
                token_contrib_dict[token_name] = [token_score_norm]
            else:
                token_contrib_dict[token_name] = token_contrib_dict[token_name] + [token_score_norm]
    sorted_contrib_list = sorted(token_contrib_dict.items(), key=operator.itemgetter(1))
    for tup_ in sorted_contrib_list:
        contrib_ = round(sum(tup_[1]), 2)
        if contrib_ > 0:
             print 'Token#{}#Contrib#{}'.format(tup_[0], contrib_)
    print "+"*25
    # #top_components_index = np.abs(pcaParamObj.components_[no_feat_param]).argsort()[::-1][:no_feat_param]
    # for index_ in top_components_index:
    #   counter = counter + 1
    #   print "Componet#{} is {} (index:[{}])".format(counter, featureNamesParam[index_], index_)
    #   print "#"*50
def dumpPredPerfValuesToFile(iterations, predPerfVector, fileName):
   str2write=''
   headerStr='AUC,PRECISION,RECALL,'
   for cnt in xrange(iterations):
     auc_   = predPerfVector[0][cnt]
     prec_  = predPerfVector[1][cnt]
     recal  = predPerfVector[2][cnt]
     str2write = str2write + str(auc_) + ',' + str(prec_) + ',' + str(recal) + ',' + '\n'
   str2write = headerStr + '\n' + str2write
   bytes_ = utility.dumpContentIntoFile(str2write, fileName)
   print "Created {} of {} bytes".format(fileName, bytes_)




def performPrediction(iterDumpDir, allFeatures, allLabels, featureNames, count_vec_flag_param):
    '''
    first do PCA
    '''
    selected_features = None ## initialization
    pca_comp, for_feature_selection, topComponentCount = getPCAsToExplore(len(allFeatures), count_vec_flag_param)
    pcaObj = decomposition.PCA(n_components=pca_comp)
    pcaObj.fit(allFeatures)
    # variance of features
    variance_of_features = pcaObj.explained_variance_
    # how much variance is explained each component
    variance_ratio_of_features = pcaObj.explained_variance_ratio_
    totalvarExplained = float(0)
    for index_ in xrange(len(variance_ratio_of_features)):
       var_exp_ = variance_ratio_of_features[index_]
       totalvarExplained = totalvarExplained + var_exp_
       print "Prin. comp#{}, ( indi) explained variance:{}, total explained variance:{}".format(index_+1, var_exp_, totalvarExplained)

    no_features_to_use = for_feature_selection
    print "Of all the features, we will use:", no_features_to_use
    print "-"*50
    pcaObj.n_components=no_features_to_use
    selected_features = pcaObj.fit_transform(allFeatures)
    print "Selected feature dataset size:", np.shape(selected_features)
    print "-"*50
    printPCAInsights(pcaObj, topComponentCount, featureNames)
    print "-"*50
    '''
    lets start prediction , now that we have feature selection otu of the way
    for single iteration
    '''
    #sklearn_models.performModeling(selected_features, allLabels, 10)
    '''
    for iterative runs of 10, deafult is 10, if you want to change then put the value after 10 as the last parameter
    '''
    sklearn_models.performIterativeModeling(iterDumpDir, selected_features, allLabels, 10, 10)


# for hash vectorizer 
def performPredictionForHashVectorizer(iterDumpDir, allFeatures, allLabels):
    selected_features = None ## initialization
    pca_comp, for_feature_selection, topComponentCount = getPCAsForHashVec(len(allFeatures))
    pcaObj = decomposition.PCA(n_components=pca_comp)
    pcaObj.fit(allFeatures)
    # variance of features
    variance_of_features = pcaObj.explained_variance_
    # how much variance is explained each component
    variance_ratio_of_features = pcaObj.explained_variance_ratio_
    totalvarExplained = float(0)
    for index_ in xrange(len(variance_ratio_of_features)):
       var_exp_ = variance_ratio_of_features[index_]
       totalvarExplained = totalvarExplained + var_exp_
       print "Prin. comp#{}, ( indi) explained variance:{}, total explained variance:{}".format(index_+1, var_exp_, totalvarExplained)

    no_features_to_use = for_feature_selection
    print "Of all the features, we will use:", no_features_to_use
    print "-"*50
    pcaObj.n_components=no_features_to_use
    selected_features = pcaObj.fit_transform(allFeatures)
    print "Selected feature dataset size:", np.shape(selected_features)
    print "-"*50

    sklearn_models.performIterativeModeling(iterDumpDir, selected_features, allLabels, 10, 10)