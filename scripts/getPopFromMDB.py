#!/usr/bin/python
# Filename: getSeqFromMDB.py for lociNGS
# shird; 26 may 2011

#this script is to retrieve a subset of loci that contain at least one individual from a given subset of populations

import pymongo
import json
import sys
from Bio import SeqIO
from pymongo import Connection
from Bio.Alphabet import generic_protein, generic_dna, generic_nucleotide
from toNexus import toNexus

connection = Connection()
db = connection.test_database
loci = db.loci
demographic = db.demographic

#create dictionary from populations entered at commandline (pop names are keys)
popsToUse = []
for arg in sys.argv:
	if arg.startswith('POP'):
		print arg
		popsToUse.append(arg)
	
print "popsToUse", popsToUse
pathsToGet = []
cursor = loci.find( {"populationsInFasta" : {'$all': popsToUse } }, {"path" : 1 , "_id" : 0 })
print "Setup cursor: %s" % cursor
for x in cursor:
#	print x["path"]
	pathsToGet.append(x["path"])

print pathsToGet[0]

#toNexus(pathsToGet)


#### MAKE THIS RETURN THE LIST OF PATHS TO PASS TO NEXT FUNCTION - IMA2 OR MIGRATE ####