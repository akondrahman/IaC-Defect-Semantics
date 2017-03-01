'''
Akond Rahman
Tokenization based predcition
Feb 28, 2017
'''
from sklearn import decomposition
import numpy as np, sklearn_models
pca_comp = 200
for_feature_selection = 141
### as output: Prin. comp#141, ( indi) explained variance:0.000172766505915, total explained variance:0.990101958387
topComponentCount = 5 ### top five components for the time being

def printPCAInsights(pcaParamObj, no_feat_param, featureNamesParam):
    counter= 0
    top_components_index = np.abs(pcaParamObj.components_[no_feat_param]).argsort()[::-1][:no_feat_param]
    for index_ in top_components_index:
      counter = counter + 1
      print "Componet#{} is {} (index:[{}])".format(counter, featureNamesParam[index_], index_)

def performPrediction(allFeatures, allLabels, featureNames):
    '''
    first do PCA
    '''
    selected_features = None ## initialization
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
    lets start prediction , now that we ahve feature selection otu of the way
    '''
    sklearn_models.performModeling(selected_features, allLabels, 10)
