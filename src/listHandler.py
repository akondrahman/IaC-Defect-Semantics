'''
enhanced pre-processing
to handle list oflists
Feb 27, 2017

'''

from nltk.stem.porter import PorterStemmer

def get_stop_words():
  lisToRet =  ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
  'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
  'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
  'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
  'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
  'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
  'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
  'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
  'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
  'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
  'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
  'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
  return lisToRet

#stopWordList =  get_stop_words()




def removeNumeralsFromList(listParam):
    tempList=[]
    finalList=[]
    for list_ in listParam:
        for tokenStr in list_:
            modifiedTokenStr =  wordConverter.removeNumeralsFromWord(tokenStr)
            tempList.append(modifiedTokenStr)
        finalList.append(tempList)
        #print "List after numeral handling: ", tempList
        tempList = []
    return finalList



def removeSpecialCharsFromList(listParam):
    tempList=[]
    finalList=[]
    for list_ in listParam:
        for tokenStr in list_:
            modifiedTokenStr =  wordConverter.removeSpecialCharsFromWord(tokenStr)
            tempList.append(modifiedTokenStr)
        finalList.append(tempList)
        #print "List after special character handling: ", tempList
        tempList = []
    return finalList


def removeDelimitersFromList(listParam):
    tempList=[]
    finalList=[]
    for list_ in listParam:
        for tokenStr in list_:
            modifiedTokenStr =  wordConverter.removeDelimitersFromWord(tokenStr)
            tempList.append(modifiedTokenStr)
        finalList.append(tempList)
        #print "List after special character handling: ", tempList
        tempList = []
    return finalList


def splitUnderscores(listParam):
    tempList=[]
    finalList=[]
    underscoreStr="_"
    splittedTokenList = []
    for list_ in listParam:
        #print "List before underscore handling: ", listO
        for tokenStr in list_:
            if tokenStr is not None  and underscoreStr in tokenStr:
                splittedTokenList = wordConverter.splitUnderscores(tokenStr)
                tempList.extend(splittedTokenList)
            else:
                tempList.append(tokenStr)
        finalList.append(tempList)
        #print "List after underscore handling: ", tempList
        tempList = []
    return finalList



def splitSpaces(listParam):
    tempList=[]
    finalList=[]
    spaceStr=" "
    splittedTokenList = []
    for list_ in listParam:
        #print "List before space handling : ", listO ;
        for tokenStr in list_:
            if tokenStr is not None  and spaceStr in tokenStr:
                splittedTokenList = wordConverter.splitSpaces(tokenStr)
                tempList.extend(splittedTokenList)
            else:
                tempList.append(tokenStr)
        finalList.append(tempList)
        #print "List after space handling: ", tempList
        tempList = []
    return finalList



def handleCamelNPascalCaseInList(listParam):
    tempList=[]
    finalList=[]
    for list_ in listParam:
        for tokenStr in list_:
            modifiedTokenStr = wordConverter.splitCamelNPascalCase(tokenStr)
            tempList.append(modifiedTokenStr)
        finalList.append(tempList)
        #print "List after camel case handling: ", tempList
        tempList = []
    return finalList


def removeSmallLenghtedTokens(listParam, thresP):
    tempList=[]
    finalList=[]
    for list_ in listParam:
        for tokenStr in list_:
            if type(tokenStr) is str:
               if len(tokenStr) > thresP:
                  tempList.append(tokenStr)
        finalList.append(tempList)
        #print "List after removing small lenghted tokens: ", tempList
        tempList = []
    return finalList

def removeStopWords(listParam):
    #this method removes tokens that are basically stop words from the list
    tempList=[]
    finalList=[]
    for list_ in listParam:
        for tokenStr in list_:
            if tokenStr not in get_stop_words():
                tempList.append(tokenStr)
        finalList.append(tempList)
        #print "List after removing stop words : ", tempList
        tempList = []
    return finalList


def removePuppKeywords(listParam):
    #this method removes tokens that are Java keywords, from the list
    tempList=[]
    finalList=[]
    for list_ in listParam:
        for tokenStr in list_:
            if tokenStr not in JavaKeywordList :
                tempList.append(tokenStr)
        finalList.append(tempList)
        #print "List after removing Java keywords: ", tempList
        tempList = []
    return finalList


def format_using_stemmer(listParam):
  #print len(listParam)
  output_list = []
  formatted_list = []
  stemmer_obj = PorterStemmer()
  for subList in listParam:
    formatted_list = [stemmer_obj.stem(token) for token in subList]
    output_list.append(formatted_list)
    formatted_list = []
  return output_list
