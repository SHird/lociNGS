#!/usr/bin/python
# Filename: getSeqFromMDB.py for lociNGS
# shird; 26 may 2011

import json
import argparse
import os
import pymongo
import re
from seqlite_mod import SNPnumber
from Bio import SeqIO
from pymongo import Connection

connection = Connection()
db = connection.test_database
collection = db.test_collection
loci = db.loci

#set up a cursor to return all paths of documents that contain the individuals in the $all array
cursor = loci.find( {"indInFasta" : { '$all' : ["J01", "J03", "J15", "J14"] } } , {"path" : 1 , "_id" : 0 })
print "Setup cursor: %s" % cursor

#i don't really understand the following, but it makes a dictionary (list?) of query results
def iter():
	for item in cursor:
		yield item
				
dictFromJSON = []				
for x in iter():
	dictFromJSON.append(json.dumps(x))
	print x, "the end"

#text modification to actually be able to access file at end of path	
for y in range(len(dictFromJSON)):
	dictFromJSON[y] = dictFromJSON[y].replace('"','')
	dictFromJSON[y] = dictFromJSON[y].replace('{','')
	dictFromJSON[y] = dictFromJSON[y].replace('}','')
	dictFromJSON[y] = dictFromJSON[y].replace('path: ','')
	file = dictFromJSON[y]
	loci_dict = SeqIO.index(file, "fasta")
	for key in loci_dict.keys():
		print key, loci_dict[key].seq	
		print "\r\r"
#		print "y is ", y, "file is ", file, "locidict ", loci_dict[key].seq

	
	#print dictFromJSON[y]



#print dictFromJSON[1]