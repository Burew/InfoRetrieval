import json 
import sys
import os
from collections import defaultdict

import test
import search

docCount = 0
fileTotalWords = defaultdict(int)

def readAllFiles(bookkeeping):
	global docCount

	with open(bookkeeping) as json_file:
		data = json.load(json_file)
		for fileLocation in data:
			docCount += 1
			wordCount = defaultdict(int)  # Creates new dictionary for tokens within a CERTAIN FILE 
			
			pathName = "/Users/suneela/Desktop/school_stuff/Spring2018/CS121/WEBPAGES_RAW/" + fileLocation
			totalWords = test.readFile(pathName, wordCount)
			test.createIndex(wordCount, fileLocation)
			fileTotalWords[fileLocation] += totalWords

			if(docCount % 500 == 0):
				print("doc Count " + str(docCount))

		#calculate Term Frequncy - Inverse Doc Frequency (TF-IDF) for a single word
		# Term frequency: <# specific word in document> DIVIDE BY <# total words in document>
		# inverse doc freq: <# total docs> DIVIDE BY <# docs w/ word in it> 
		for word in test.index:
			for index, (docID, singleWordCount) in enumerate(test.index[word]):
				termFrequency = 1.0 * singleWordCount / fileTotalWords[docID]
				inverseDocFrequency = len(data) / len(test.index[word])
				tf_idf = float("%.3f" % (termFrequency * inverseDocFrequency))
				test.index[word][index] = (docID, tf_idf)


if __name__ == '__main__':
	#clear reportFile.txt
	with open("reportFile.txt", 'w') as f:
		f.write("")
	
	test.loadDict()

	#read files
	if len(test.index) == 0:
		
		readAllFiles(test.bookkeepingFilePath)

	#init search console
	# search.userInput()

	queries = ["INFORMATICS", "MONDEGO", "irvine"]
		
	for query in queries:
		query = query.lower().strip()
		if search.checkIfValidQuery(query) == True:
			docs = search.retrieveAllDocs(query)
			search.searchQuery(query,docs)
	
	#write dictionary to file
	invertedIndexPath = "dict.txt"
	with open(invertedIndexPath,"w") as f:
		f.write( json.dumps(test.index) )
		f.close()


	with open("reportFile.txt", "a") as metadataFile:
		metadataFile.write("\n--------------------------------------------------\n")
		metadataFile.write("Number of documents in corpus: " + str(len(test.bookkeepingDict)) + "\n")
		metadataFile.write("Number of unique tokens in index: " + str(len(test.index)) + "\n")
		metadataFile.write("Size of inverted index on disk: " + str(os.path.getsize(invertedIndexPath)) + " bytes\n")

