'''
Akond Rahman
March 4, 2017
place holder for corpus comparisons
'''
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
import numpy as np, math, utility, scipy
from scipy.special import entr
from gensim import corpora, models, matutils
def getEntropy_ForTerm(wordParam, corpus2SearchParam):
    tokenProbHolder = []
    for indiDoc in corpus2SearchParam:
       appearanceCount = 0
       splitted_strs   = indiDoc.split(' ')
       totTokenCount   = len(splitted_strs)
       for str_ in splitted_strs:
          if wordParam==str_:
             appearanceCount = appearanceCount + 1
       tokenProb = float(appearanceCount) / float(totTokenCount)
       tokenProbHolder.append(tokenProb)
    return entr(tokenProb)


def getNormalizedOccurences_ForTerm(wordParam, corpus2SearchParam):
    appearanceCount  = 0
    tokensInDocCount = 0
    for indiDoc in corpus2SearchParam:
        if wordParam in indiDoc:
            appearanceCount = appearanceCount + 1
        tokensInDocCount = tokensInDocCount + len(indiDoc.split(' '))
    return float(appearanceCount)/float(tokensInDocCount)


def getInverseDocumentMetric_ForTerm(wordParam, corpus2SearchParam):
    val2ret = 0
    total_no_of_docs = len(corpus2SearchParam)
    appearanceCount  = 0
    for indiDoc in corpus2SearchParam:
        if wordParam in indiDoc:
            appearanceCount = appearanceCount + 1
    if (appearanceCount > 0):
        val2ret = float(total_no_of_docs)/float(appearanceCount)
        val2ret = math.log(val2ret) ## exponential log
    else:
        val2ret = float(0)
    return val2ret



def getRawOccurences_ForTerm(wordParam, corpus2SearchParam):
    appearanceCount  = 0
    for indiDoc in corpus2SearchParam:
        if wordParam in indiDoc:
            appearanceCount = appearanceCount + 1
    return float(appearanceCount)


def getTFIDF_ForTerm(wordParam, corpus2SearchParam):
    tf_, idf_ = getNormalizedOccurences_ForTerm(wordParam, corpus2SearchParam), getInverseDocumentMetric_ForTerm(wordParam, corpus2SearchParam)
    val2ret = round(tf_ * idf_, 5)
    return val2ret


def statisticallyCompareTF(def_corpus, non_def_corpus, complete_corpus, file_to_save):
  '''
  vectors to hold outptu values
  '''
  defected_occurences     = []
  non_defected_occurences = []

  defected_idfs           = []
  non_defected_idfs       = []

  defected_raw_occurences           = []
  non_defected_raw_occurences       = []

  defected_tfidf = []
  non_defected_tfidf = []

  defected_entropies            = []
  non_defected_entropies        = []
  '''
  vectorizer intitialization
  '''
  def_tfidf_vectorizer       = TfidfVectorizer(min_df=1)
  non_def_tfidf_vectorizer   = TfidfVectorizer(min_df=1)
  complete_tfidf_vectorizer  = TfidfVectorizer(min_df=1)
  '''
  lets fit them
  '''
  tf_idf_compelte_corpus_features        = complete_tfidf_vectorizer.fit_transform(complete_corpus)
  tf_idf_defect_corpus_features          = def_tfidf_vectorizer.fit_transform(def_corpus)
  tf_idf_non_defect_corpus_features      = non_def_tfidf_vectorizer.fit_transform(non_def_corpus)
  '''
  get tokens from complete corpus
  '''
  feature_names = complete_tfidf_vectorizer.get_feature_names()
  # Step-1: convert to array
  tf_idf_compelte_corpus_features = tf_idf_compelte_corpus_features.toarray()
  # Sum up the counts of each vocabulary word
  dist_all_features = np.sum(tf_idf_compelte_corpus_features, axis=0)
  '''
  iterate over compelte corpus to get tf, idf etc. for defected and non defected corpus
  '''
  for word_, count_ in zip(feature_names, dist_all_features):
      #print "word:[{}]--->count:[{}]".format(word_, count_)
      '''
      first get normalized occurences
      '''
      defected_occ_for_word     = getNormalizedOccurences_ForTerm(word_, def_corpus)
      defected_occurences.append(defected_occ_for_word)

      non_defected_occ_for_word = getNormalizedOccurences_ForTerm(word_, non_def_corpus)
      non_defected_occurences.append(non_defected_occ_for_word)

      defected_occ_for_word, non_defected_occ_for_word = 0, 0
      '''
      then get inverse 'normalized' docuemnt occurences
      '''
      defected_idf_for_word     = getInverseDocumentMetric_ForTerm(word_, def_corpus)
      defected_idfs.append(defected_idf_for_word)

      non_defected_idf_for_word = getInverseDocumentMetric_ForTerm(word_, non_def_corpus)
      non_defected_idfs.append(non_defected_idf_for_word)

      defected_idf_for_word, non_defected_idf_for_word = 0, 0
      '''
      then get raw occurences
      '''
      defected_raw_occurences_for_word     = getRawOccurences_ForTerm(word_, def_corpus)
      defected_raw_occurences.append(defected_raw_occurences_for_word)

      non_defected_raw_occurences_for_word = getRawOccurences_ForTerm(word_, non_def_corpus)
      non_defected_raw_occurences.append(non_defected_raw_occurences_for_word)

      defected_raw_occurences_for_word, non_defected_raw_occurences_for_word = 0, 0

      '''
      then get tf-idf: added July 23, 2017, 8:00 PM
      '''
      defected_tf_idf_for_word     = getTFIDF_ForTerm(word_, def_corpus)
      defected_tfidf.append(defected_tf_idf_for_word)

      non_defected_tf_idf_for_word     = getTFIDF_ForTerm(word_, non_def_corpus)
      non_defected_tfidf.append(non_defected_tf_idf_for_word)

      defected_tf_idf_for_word, non_defected_tf_idf_for_word = 0, 0

      '''
      finally get raw entropies
      '''
      defected_entropies_for_word     = getEntropy_ForTerm(word_, def_corpus)
      defected_entropies.append(defected_entropies_for_word)

      non_defected_entropies_for_word = getEntropy_ForTerm(word_, non_def_corpus)
      non_defected_entropies.append(non_defected_entropies_for_word)

      defected_entropies_for_word, non_defected_entropies_for_word = 0, 0
  '''
  a quick sanity check of the normalized occurences
  '''
  print "nomralized occurences ..."
  print "D: {}, ND:{}, C:{}".format(np.mean(defected_occurences), np.mean(non_defected_occurences), len(feature_names))
  print "="*100
  '''
  a quick sanity check of the inverse dcouemnt metric
  '''
  print "inver document metric ..."
  print "D: {}, ND:{}, C:{}".format(np.mean(defected_idfs), np.mean(non_defected_idfs), len(feature_names))
  print "="*100

  '''
  a quick sanity check of the raw occurences
  '''
  print "raw occurences ..."
  print "D: {}, ND:{}, C:{}".format(np.mean(defected_raw_occurences), np.mean(non_defected_raw_occurences), len(feature_names))
  # print "D: {}, ND:{}, C:{}".format(len(defected_raw_occurences), len(non_defected_raw_occurences), len(feature_names))
  print "="*100

  '''
  a quick sanity check of TFIDF
  '''
  print "tf-idf ..."
  print "D: {}, ND:{}, C:{}".format(np.mean(defected_tfidf), np.mean(non_defected_tfidf), len(feature_names))
  # print "D: {}, ND:{}, C:{}".format(len(defected_tfidf), len(non_defected_tfidf), len(feature_names))
  print "="*100

  '''
  a quick sanity check of entropies
  '''
  print "entropies ..."
  print "D: {}, ND:{}, C:{}".format(np.mean(defected_entropies), np.mean(non_defected_entropies), len(feature_names))
  # print "D: {}, ND:{}, C:{}".format(len(defected_entropies), len(non_defected_entropies), len(feature_names))
  print "="*100


  list2Dump = [  feature_names, defected_occurences, non_defected_occurences,
                                defected_idfs, non_defected_idfs,
                                defected_raw_occurences, non_defected_raw_occurences,
                                defected_tfidf, non_defected_tfidf,  
                                defected_entropies, non_defected_entropies  ]
  utility.dumpComparisonMetrics(list2Dump, len(feature_names), file_to_save)

'''
genesim zone
'''

def processTokensForGensimCorpora(tokenListP):
    list_to_ret = []
    for strs_ in tokenListP:
        splitted_str = strs_.split(' ')
        list_to_ret.append(splitted_str)
    return list_to_ret




def getTFIDFDist(tokenListParam, labelParam):
    ## first clean up previously created files
    theMMFile        = labelParam + ".mm"
    theDictFile      = labelParam + ".dict"
    theMMIndexFile   = labelParam + ".mm.index"
    utility.performCleanUp(theMMFile)
    utility.performCleanUp(theDictFile)
    utility.performCleanUp(theMMIndexFile)

    dictionary = corpora.Dictionary(tokenListParam)
    utility.performCleanUp(theDictFile)
    dictionary.save(theDictFile)

    raw_corpus = [dictionary.doc2bow(t) for t in tokenListParam]
    corpora.MmCorpus.serialize(theMMFile, raw_corpus)
    dictionary = corpora.Dictionary.load(theDictFile)

    corpus = corpora.MmCorpus(theMMFile)
    # Transform Text with TF-IDF
    tfidf = models.TfidfModel(corpus)
    # corpus tf-idf
    corpus_tfidf = tfidf[corpus]
    return corpus_tfidf

def compareCorpusesViaSimilarity(defectCorpus, nonDefectCorpus):
   ##reff: https://gist.github.com/clemsos/7692685
   defect_tokenList = processTokensForGensimCorpora(defectCorpus)
   defect_dis = getTFIDFDist(defect_tokenList, 'DEFECTED')
   print "Defect distribution:", defect_dis
   non_defect_tokenList = processTokensForGensimCorpora(nonDefectCorpus)
   non_defect_dis = getTFIDFDist(non_defect_tokenList, 'NONDEFECTED')
   print "Non defect distribution:", non_defect_dis
   similarity_score = matutils.cossim(defect_dis, non_defect_dis)
   print "Similarity score is:", similarity_score
   print "*"*75
   return similarity_score
