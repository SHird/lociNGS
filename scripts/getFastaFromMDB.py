#!/usr/bin/python
# Filename: getFastaFromMDB.py for lociNGS
# shird; 14 june 2011

#script takes a list of individuals at the commandline
#script produces a nexus file for every fasta locus file that contains the individuals in the list

import pymongo
import json
import sys
from Bio import SeqIO
from pymongo import Connection
from Bio.Alphabet import generic_protein, generic_dna, generic_nucleotide

#this function can be called to convert fasta format to nexus
def nexusConverter(list):
	for path in list:
		output_handle = path.replace(".fasta", ".nex")
		print output_handle
		count = SeqIO.convert(path, "fasta", output_handle, "nexus", generic_dna)	

connection = Connection()
db = connection.test_database
loci = db.loci

#make a list of individuals to pass to mongoDB
listOfInds = []
for arg in sys.argv:
	print arg
	listOfInds.append(arg)

del listOfInds[0]  #remove the first element of list to get rid of script name

#set up a cursor to return all paths of documents that contain the individuals in the $all array
cursor = loci.find( {"indInFasta" : { '$all' : listOfInds } } , {"path" : 1 , "_id" : 0 })
print "all : ", listOfInds
print "Setup cursor: %s" % cursor

listOfFasta = []		
fileList = []
for x in cursor:
	listOfFasta.append(json.dumps(x))

for y in range(len(listOfFasta)):
	listOfFasta[y] = listOfFasta[y].replace('"','')
	listOfFasta[y] = listOfFasta[y].replace('{','')
	listOfFasta[y] = listOfFasta[y].replace('}','')
	listOfFasta[y] = listOfFasta[y].replace('path: ','')

nexusConverter(listOfFasta)
