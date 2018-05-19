import nltk 
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from urlparse import  urljoin
from collections import defaultdict 
import json
import sys
 

index = defaultdict(list)

def loadDict():
	global index
	try:
		with open("dict.txt") as indexFile:
			index = json.loads(indexFile.read())
			print "Index loaded w/ " + str(len(index)) + " entries"
	except:
		print "Dictionary file not found"

def readFile(file, tempDict):
	openedFile = open(file, 'r')
	soup = BeautifulSoup(openedFile, 'html.parser')
	long_string = soup.get_text()
	tokens = nltk.wordpunct_tokenize(str(long_string.encode(encoding='UTF-8')))
	
	totalWordCount = 0

	#tokenize, add wordcount 
	for eachWord in tokens:
		if(eachWord).isalpha():
			tempDict[eachWord.lower()] += 1
			totalWordCount += 1

	openedFile.close()

	return totalWordCount

def createIndex(tempDict,docId):
	#create postings
	for token,frequency in tempDict.items():
		index[token].append((str(docId),frequency))

if __name__ == "__main__":
	# loadDict()
	pass

