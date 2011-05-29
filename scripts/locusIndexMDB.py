#!/usr/bin/python
# Filename: locusIndex.py for lociNGS
# shird; 24 may 2011
import argparse
import os
import pymongo
import re
from seqlite_mod import SNPnumber
from Bio import SeqIO
from pymongo import Connection

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
	file = os.path.join(args.path, fasta)
	loci_dict = SeqIO.index(file, "fasta")
	#print len(loci_dict), loci_dict.keys()
	SNP = SNPnumber(file)	
	locus = {"locus":fasta, "individuals":loci_dict.keys(), "length": len(loci_dict[loci_dict.keys()[0]]), "path": file, "SNPs" : SNP }   #, "length":len(loci_dict.keys()[0].seq)}
	loci = db.loci
	loci.insert(locus)
	print "locus = ", re.sub(".fasta","",fasta), "; number alleles = ", len(loci_dict), "; length = ", len(loci_dict[loci_dict.keys()[0]])  , "; path = ", file, "; SNPs = ",SNP
	
print "total of ", loci.count() , "loci"

####this creates a dictionary with the names of individuals as keys, so that counts may be associated with individuals
print "\n...reading the names file into a list...\n"
names_file = open("names.txt", "r")
lines = names_file.readlines()
lines = [line.rstrip() for line in lines]
names_file.close()

for name in lines:
	name1 = name+".01"
	print "name: ", name, "found in: ", db.loci.find({"individuals": name1}).count(), "loci"