from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer
from collections import defaultdict

import json

# import nltk
# nltk.download()

"""

Text Processing

"""
def readFileText(fileName):
    with open(fileName, 'r') as file:
        return BeautifulSoup(file.read(), "html.parser").get_text()

# def generateTokens(text):
#     for t in word_tokenize(text):
#         yield t

def buildTokenIndex(fileName):
    results = defaultdict(int)

    fileText = readFileText(fileName)
    stemmer = PorterStemmer()

    for token in wordpunct_tokenize(fileText):
        token = token.lower()
        
        if len(token) > 1 and token.isalpha() and token not in stopwords.words("English"):
            token = stemmer.stem(token)
            results[token] += 1
            # yield token
    return results

def buildInvertedIndex():
    pass

"""

Reading files 

"""

"""

User I/O - searching

"""




if __name__ == "__main__":
    # print(generatePreprocessedTokens(r"WEBPAGES/WEBPAGES_RAW/0/1"))

    #read all files
    with open(r"WEBPAGES/WEBPAGES_RAW/bookkeeping.json") as bookKeepingFile:
        bookKeeping = json.load(bookKeepingFile)

        for docID in bookKeeping.keys():
            filePath = r"WEBPAGES/WEBPAGES_RAW/" + docID
            #process files here
            
    

    

