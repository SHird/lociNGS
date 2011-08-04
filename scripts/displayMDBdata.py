#!/usr/bin/python
# Filename: displayMDBdata.py for lociNGS
# shird; 9 june 2011

import json
import argparse
import os
import pymongo
import re
from seqlite_mod import SNPnumber
from Bio import SeqIO
from pymongo import Connection
from Bio.Alphabet import generic_protein, generic_dna, generic_nucleotide

connection = Connection()
db = connection.test_database
loci = db.loci
demographic = db.demographic

#set up a cursor to return all paths of documents that contain the individuals in the $all array
cursor = demographic.find()
print "Setup cursor: %s" % cursor
#i don't really understand the following, but it makes a dictionary (list?) of query results
def iter():
	for item in cursor:
		yield item				
#print some demographic info to screen from cursor
for x in iter():
	print "Individual:", x["Individual"], ", Location:", x["Location"], ", Total Number of Reads:", x["totalReads"], ", Number of Loci:", x["numLoci"]


#print locus information to screen from new cursor
cursor = loci.find( {"locusFasta" : { '$exists' : 'true' } } )
print "Setup cursor: %s" % cursor
for y in iter():
	print "Locus:", y["locusFasta"], ", Individuals Present:", y["indInFasta"], ", Individuals with Read Counts:", y["individuals"]
