import json 
import sys
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
			
			pathName = r"WEBPAGES/WEBPAGES_RAW/" + fileLocation
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
		fileName = r"WEBPAGES/WEBPAGES_RAW/bookkeeping.json" #sys.argv[1]
		readAllFiles(fileName)

	#init search console
	search.userInput()
	
	#write dictionary to file
	with open("dict.txt","w") as f:
		f.write( json.dumps(test.index) )
		f.close()

