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

cursor = loci.find( {"individuals" : "R03.01"} , {"path" : 1 , "_id" : 0 })
print "Setup cursor: %s" % cursor

def iter():
	for item in cursor:
		yield item
				
dictFromJSON = []				
for x in iter():
	dictFromJSON.append(json.dumps(x))
	print x, "the end"
	
for y in range(len(dictFromJSON)):
	dictFromJSON[y] = dictFromJSON[y].replace('"','')
	dictFromJSON[y] = dictFromJSON[y].replace('{','')
	dictFromJSON[y] = dictFromJSON[y].replace('}','')
	dictFromJSON[y] = dictFromJSON[y].replace('path: ','')
	file = dictFromJSON[y]
	loci_dict = SeqIO.index(file, "fasta")
	print loci_dict[loci_dict.keys()[0]]

	
	#print dictFromJSON[y]



#print dictFromJSON[1]