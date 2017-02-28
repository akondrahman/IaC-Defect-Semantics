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
    #print "taking a peek (numerals removed):", outputList_NumeralsRemoved[0]
    ## 2
    outputList_UnderscoreHandled = listHandler.splitUnderscores(outputList_NumeralsRemoved)
    ## 3
    outputList_DotHandled = listHandler.splitDots(outputList_UnderscoreHandled)
    #print outputList_DotHandled
    ## 4
    outputList_ColonHandled = listHandler.splitColons(outputList_DotHandled)
    ## 5
    outputList_SlashHandled = listHandler.splitSlashes(outputList_ColonHandled)
    ## 6
    outputList_DashHandled = listHandler.splitDashes(outputList_SlashHandled)
    ## 7
    outputList_CamelNPascalHandled = listHandler.handleCamelNPascalCaseInList(outputList_DashHandled)
    ## 8
    outputList_SplitSpaces = listHandler.splitSpaces(outputList_CamelNPascalHandled)
    ## 9
    outputList_SpecialCharsRemoved = listHandler.removeSpecialCharsFromList(outputList_SplitSpaces)
    ## 10
    outputList_SmallTokensRemoved = listHandler.removeSmallLenghtedTokens(outputList_SpecialCharsRemoved, thresOfTokenLen)
    ## 11
    outputList_StopWordGone = listHandler.removeStopWords(outputList_SmallTokensRemoved)
    ## 12
    outputList_AllKeyWordsRemoved = listHandler.removePuppKeywords(outputList_StopWordGone)
    ## 13
    output_DelimiterRemoved = listHandler.removeDelimitersFromList(outputList_AllKeyWordsRemoved)
    ## 14
    output_utf              = listHandler.convertToUTF(output_DelimiterRemoved)
    ## 15
    output_stemmed          = listHandler.format_using_stemmer(output_utf)
    print "--------------------------- ALMOST THERE! ----------------------------"
    print "I am done [:-)], current length of the list: ", len(output_stemmed)
    return output_stemmed
