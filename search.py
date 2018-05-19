import json

import test

def checkIfValidQuery(query):
	return (query in test.index)

def userInput():
	while True:
		query = raw_input("Search: ") # MAKE SUR TO LOWERCASE QUERY
		if(query != "exit()"):
			if checkIfValidQuery(query) == True:
				docs = retrieveAllDocs(query)
				searchQuery(query,docs)
		else:
			return 

def retrieveAllDocs(query):
	docs =[]
	if (query in test.index):
		for element in test.index[query]:
			if len(docs) >= 10:
				return docs 
			docs.append(element[0])
	return docs

def searchQuery(query, all_documents):
	f = open("reportFile.txt", 'a')
	with open(r"WEBPAGES/WEBPAGES_RAW/bookkeeping.json") as json_file:
		data = json.load(json_file)
		f.write("Token: " + query + "\n")

		for eachDoc in all_documents:
			url = data[eachDoc]
			f.write("	URL: " + url + "\n")
	f.close() 