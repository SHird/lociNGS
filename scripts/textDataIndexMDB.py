#!/usr/bin/python
# Filename: textDataIndexMDB.py for lociNGS
# shird; 6 june 2011
#this scripts translates a tab-delimited table containing information about individuals in a dataset to a mongoDB database
#takes path to text file as an argument

import argparse
import os
import string
import pymongo
from pymongo import Connection

#get connection to mongodb
connection = Connection()
db = connection.test_database
demographic = db.demographic

#open tab delimited text file
#get path from commandline
parser = argparse.ArgumentParser(description='Get path to demographic text file.')
parser.add_argument('path',help='give the program the path to the tab-delimited demographic data files')
args = parser.parse_args()
print 'Got this file:', args.path
#demoFile = args.path)

f1 = open(args.path, 'r')
rows = [ line.strip().split('\t') for line in f1 ]

#popColumnNum = 0
#indColumnNum = 0

indColumnNum = rows[0].index("Individual")
popColumnNum = rows[0].index("Population")
print "popCol is ", popColumnNum, "indCol is ", indColumnNum


#put data into list of lists and insert to mongodb
listOfDemo = []
popList = []
		
for row in range(1, len(rows)):
	popList.append(rows[row][popColumnNum])

	for column in range(len(rows[0])):
		demoCurrent = []
		demoCurrent = (rows[0][column], rows[row][column])
		listOfDemo.append(demoCurrent)
	dict_listOfDemo = (listOfDemo)
	y = dict(dict_listOfDemo)
	print y
	demographic.insert(y)

dictPopList={}
print popList
setList = set(popList)
for one in setList:
	dictPopList[one] = []
for row in range(1, len(rows)):
	dictPopList[rows[row][popColumnNum]].append(rows[row][indColumnNum])
#	print rows[row][popColumnNum]

loci = db.loci
for each in dictPopList:
	print each
	print dictPopList[each]
	db.loci.update( {"indInFasta" : {'$in': dictPopList[each] } } , {'$addToSet' : {'populationsInFasta': each } }, multi=True )
	
#cursor2 = 	db.loci.find({"populationsInFasta": {'$in' : ['POP1', 'POP2']} } )
#print "Setup cursor: %s" % cursor2
#for x in cursor2:
#	print x

















