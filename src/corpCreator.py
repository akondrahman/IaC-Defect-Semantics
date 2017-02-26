'''
Akond Rahman
Feb 26, 2017
CorCreator from Simila work
'''

import  listHandler
thresOfTokenLen = 2

def generateCorpus(rawTokenList):
    ###Order of execution is extremely important
    ## 1
    outputList_NumeralsRemoved = listHandler.removeNumeralsFromList(rawTokenList)
    ## 2
    outputList_UnderscoreHandled = listHandler.splitUnderscores(outputList_NumeralsRemoved)
    ## 3
    outputList_CamelNPascalHandled = listHandler.handleCamelNPascalCaseInList(outputList_UnderscoreHandled)
    ## 4
    outputList_SplitSpaces = listHandler.splitSpaces(outputList_CamelNPascalHandled)
    ## 5
    outputList_SpecialCharsRemoved = listHandler.removeSpecialCharsFromList(outputList_SplitSpaces)
    ## 6
    outputList_SmallTokensRemoved = listHandler.removeSmallLenghtedTokens(outputList_SpecialCharsRemoved, thresOfTokenLen)
    ## 7
    outputList_StopWordGone = listHandler.removeStopWords(outputList_SmallTokensRemoved)
    ## 8
    outputList_AllKeyWordsRemoved = listHandler.removePuppKeywords(outputList_StopWordGone)
    ##9
    output_DelimiterRemoved = listHandler.removeDelimitersFromList(outputList_AllKeyWordsRemoved)
    ##10
    output_porter_stemmed = listHandler.format_using_stemmer(output_DelimiterRemoved)
    print "--------------------------- ALMOST THERE! ----------------------------"
    print "I am done [:-)], current length of the list: ", len(output_porter_stemmed)
    return output_porter_stemmed
