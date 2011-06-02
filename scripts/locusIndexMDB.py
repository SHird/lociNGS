#!/usr/bin/python
# Filename: locusIndex.py for lociNGS
# shird; 24 may 2011
import argparse
import os
import fnmatch
import pymongo
import re
import json
import simplejson
from seqlite_mod import SNPnumber
from Bio import SeqIO
from pymongo import Connection
#from pymongo.bson import BSON


#for getting a connection to MongoDB via pymongo
connection = Connection()
db = connection.test_database
collection = db.test_collection

#get path from commandline
parser = argparse.ArgumentParser(description='Get path to fasta files.')
parser.add_argument('path',help='give the program the path to the folder of locus files')
args = parser.parse_args()
print 'Got this folder:', args.path
fasta_library = os.listdir(args.path)
#print fasta_library

#print data to post collection in mongoDB
for fasta in fasta_library:
	listOflists = []
	if fnmatch.fnmatch(fasta, '*.fasta'):
		file = os.path.join(args.path, fasta)
		print 'Got this file: ', file
		loci_list = list(SeqIO.parse(file, "fasta"))
		for eachLocus in loci_list:
			if fnmatch.fnmatch(eachLocus.id, '*.01'):
		#		print eachLocus.id
				current = []
				current = ( re.sub("\.01", "", eachLocus.id) , 0 )
				print current
				listOflists.append(current)
		dict_listOflists = (listOflists)
		print "dict_listOflists is ", dict_listOflists
		x = (dict(dict_listOflists))
#		print "x is ", x
#		print len(loci_dict), loci_dict.keys()
	#	if len(listOflists) > 1:
		SNP = SNPnumber(file)	
	#	else:
	#		SNP = 0
		locus = {"locusFasta":fasta, "locusNumber": re.sub(".+_(?P<dig>\d+)_\D+","\g<dig>",fasta), "individuals": x, "indInFasta" : x.keys(), "length": len(loci_list[0]), "path": file, "SNPs" : SNP }   #, "length":len(loci_dict.keys()[0].seq)}
		loci = db.loci
		loci.insert(locus)
		#print "locus = ", re.sub(".fasta","",fasta), "; locusNumber = ", \g<dig>, "; individuals", x, "; number alleles = ", len(loci_list), "; length = ", len(loci_list[0])  , "; path = ", file, "; SNPs = ",SNP
	
print "total of ", loci.count() , "loci"

####this creates a dictionary with the names of individuals as keys, so that counts may be associated with individuals
print "\n...reading the names file into a list...\n"
names_file = open("names.txt", "r")
lines = names_file.readlines()
lines = [line.rstrip() for line in lines]
names_file.close()

for name in lines:
	name1 = "individuals."+name
	print "name: ", name, "found in: ", db.loci.find({ name1 : 0 } ).count(), "loci"