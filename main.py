from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer
from collections import defaultdict
import os
import json

# constants
webpagesFilePath = r"WEBPAGES/WEBPAGES_RAW/"
bookkeepingFilePath = webpagesFilePath + "bookkeepingTEST.json"
reportFilePath = "reportFile.txt"
invertedIndexPath = "dict.txt"

invertedIndex = defaultdict(list) # token : [posting1, posting2]
docTokenCounts = defaultdict(int) # docID : num of tokens in doc, used for TF-IDF
bookkeeping = {}
stemmer = PorterStemmer()

####################### Loading Necessary Files ########################
def loadBookkeeping():
    if len(bookkeeping) == 0:
        with open(bookkeepingFilePath) as bookKeepingFile:
            bookkeeping.update(json.load(bookKeepingFile))

def loadInvertedIndex():
    try:
        with open(invertedIndexPath) as invertedIndexFile:
            print("Inverted index loaded from \"" + invertedIndexPath + "\"")
            invertedIndex.update(json.load(invertedIndexFile)) 
    except:
        print("Inverted index file \"" + invertedIndexPath + "\" not found, creating new inverted index...")
        buildInvertedIndex()
        writeInvertedIndex()

def writeInvertedIndex():
    with open(invertedIndexPath, "w") as invertedIndexFile:
        json.dump(invertedIndex, invertedIndexFile)

def readFileText(fileName):
    with open(fileName, 'r') as file:
        return BeautifulSoup(file.read(), "html.parser").get_text()

####################### Building the inverted index ########################
"""
    @param fileName: { str } file path name
    @param docID: { str } docID of the file, is also the last part of fileName
    @returns { dict(str:int) } dict of tokens and their number of occurances in the file
    @sideEffect : updates docTokenCounts
    @description: opens file, parses and counts valid tokens
"""
def buildTokensCountFromFile(fileName, docID):
    results = defaultdict(int)
    fileText = readFileText(fileName)
    # stemmer = PorterStemmer()

    numValidTokens = 0
    for token in wordpunct_tokenize(fileText):
        token = token.strip().lower()
        
        if len(token) > 1 and token.isalpha() and token not in stopwords.words("English"):
            token = stemmer.stem(token)
            results[token] += 1
            numValidTokens += 1

    docTokenCounts[docID] = numValidTokens

    return results

"""
    @param tokenCounts: { dict(str, int) } tokens and the number of occurances in the file
    @param docID: { str } 
    @description:  adds an inverted index of <token : [docId, tokenCount]>
        The tokenCount is need for TF-IDF and will be replaced later
"""
def addInvertedIndexFromTokenCounts(tokenCounts, docID):
    for token, tokenCount in tokenCounts.items():
        postings = [docID, tokenCount]   #add more heuristics here later...
        invertedIndex[token].append(postings)

"""
    @description: builds inverted docs specified from bookKeepingFile
        Calculates TF-IDF
        Inverted index will be in this form at the end:
            Token : list( docID_1:TF-IDF_1, docID_2:TF-IDF_2 ... )
"""
def buildInvertedIndex():
    #tokenize and record statistics
    for docNum, docID in enumerate(bookkeeping):
        docFilePath = webpagesFilePath + docID
        tokensCount = buildTokensCountFromFile(docFilePath, docID)
        addInvertedIndexFromTokenCounts(tokensCount, docID)

        if (docNum % 500 == 0):
            print(str(docNum) + " Docs Processed")    
    # At this point, invertedIndex has these entries:
    #   token: [ [docID, num of occurances], [docID, num of occurances] ...]
    # After we calcualte TF-IDF, it will look like this:
    #   token: [ [docID, TF-IDF], [docID, TF-IDF] ... ]

    # calculate TF-IDF, will replace num of occurances
    # TF-IDF = TermFreq * InverseDocFreq
    #   TermFreq = num of token in document DIVIDE_BY num of total tokens in doc
    #   InverseDocFreq = num of total docs DIVIDE_BY num of docs w/ token in it
    for tokens in invertedIndex:
        inverseDocFrequency = float(len(bookkeeping)) / len(invertedIndex[tokens])

        for postingIndex, [docID,count] in enumerate(invertedIndex[tokens]):
            termFrequency = float(count) / docTokenCounts[docID]
            TF_IDF = float("%.3d" % (termFrequency * inverseDocFrequency))
            invertedIndex[tokens][postingIndex] = [docID, TF_IDF]

###################### Handle Queries ########################## 
"""
    @param query { str } normalized query
    @returns links { list[str] }, list of ranked links found
"""
def retrieveLinks(query):
    links = []
    linkLimit = 10

    # print(query, invertedIndex[query])

    for postings in invertedIndex[query]:
        # print(postings)
        docID = postings[0]
        links.append(bookkeeping[docID])
        if len(links) >= linkLimit:
            break

    return links

def addSearchResultToFile(query, links):
    if links:
        with open(reportFilePath, "a") as reportFile:
            reportFile.write("Token: " + query + "\n")
            for link in links:
                reportFile.write("\tURL: " + link + "\n")
                
def userInput():
    query = ""
    while (query != "exit()"):
        query = raw_input("Search: ").strip().lower()
        links = retrieveLinks(stemmer.stem(query))  #stem the query for searching
        addSearchResultToFile(query, links)         # but display the original query
            
if __name__ == "__main__":
    with open(reportFilePath, "w") as reportFile:
        reportFile.write("")
        
    loadBookkeeping()
    loadInvertedIndex()

    #user search
    # userInput()

    queries = ["INFORMATICS", "MONDEGO", "IRVINE"]
    for query in queries:
        query = query.strip().lower()

        # print(query, invertedIndex[query])
        links = retrieveLinks(stemmer.stem(query))
        
        addSearchResultToFile(query, links)
    
    # add statistics
    with open(reportFilePath, "a") as reportFile:
        reportFile.write("\n--------------------------------------------------\n")
        reportFile.write("Number of documents in corpus: " + str(len(bookkeeping)) + "\n")
        reportFile.write("Number of unique tokens in index: " + str(len(invertedIndex)) + "\n")
        reportFile.write("Size of inverted index on disk: " + str(os.path.getsize(invertedIndexPath)) + " bytes\n")
        reportFile.close() #make changes immediate
    
    