#!/usr/bin/python
# Filename: samIndexMDB.py for lociNGS
# shird; 27 may 2011

import fnmatch
import pysam
import argparse
import os
import pymongo
import re
import json
import simplejson
from seqlite_mod import SNPnumber
from Bio import SeqIO
from pymongo import Connection

def iter():
	for item in cursor:
		yield item

#for getting a connection to MongoDB via pymongo
connection = Connection()
db = connection.test_database
collection = db.loci

parser = argparse.ArgumentParser(description='Get path to bam files.')
parser.add_argument('path',help='give the program the path to the folder of locus files')
args = parser.parse_args()
print 'Got this folder:', args.path
bam_library = os.listdir(args.path)
#print fasta_library

#print data to post collection in mongoDB
for bam in bam_library:
	if fnmatch.fnmatch(bam, '*.bam'):
		file = os.path.join(args.path, bam)
		print 'Got this file: ', file
###will need to index the bam files if not already done?

		samfile = pysam.Samfile(file, "rb")

		print samfile.nreferences   #prints number of loci
		allLoci = samfile.references

		currentName = re.sub('/.+/', '', file)
		currentName = re.sub('.sorted.bam','', currentName)

		namePath = "individuals."+currentName

		print currentName
		print namePath

		for n in allLoci:
			count = 0
			for alignedread in samfile.fetch(n):
			#	print alignedread.seq
				count = count + 1
			m = re.sub('.+\|.+\|','',n)	
			if count>0:
				db.loci.update( {"locusNumber" : m }, { '$inc' : { namePath : count } } )
				print n, count
		



# re.sub('^+.|.+|','',n)









#cursor = db.loci.find({ namePath : 0 }, {'locusNumber' : 1, "_id" : 0})
#print "cursor", db.loci.find(cursor.next())
				
#dictFromJSON = []				
#for x in iter():
#	dictFromJSON.append(json.dumps(x))
#	print x, "x in iter"
#	cursor2 = db.loci.find(x)
	
	
#print "dictFromJSON ", dictFromJSON

#for key in range(len(dictFromJSON)):
#	print key, "memberOfList dictFromJSON", dictFromJSON[key]



#######PUT LIST MEMBERS INTO A QUERY########


for n in allLoci:
	count = 0
	for alignedread in samfile.fetch(n):
	#	print alignedread.seq
		count = count + 1
	print n, count

#set locus to locusname
#set individual to individual
#search mongo for locus and individual
#update with count

#for name in lines:
#	name1 = "individuals."+name
#	print "name: ", name, "found in: ", db.loci.find({ name1 : 0 } ).count(), "loci"

#db.loci.update({"path": '*.fasta'}, {"$set" : {"numReads2" : 344}})

#SAMindividual = {"locus":fasta, "individuals":loci_dict.keys(), "length": len(loci_dict[loci_dict.keys()[0]]), "path": file, "SNPs" : SNP }   #, "length":len(loci_dict.keys()[0].seq)}
#loci = db.loci
#loci.individuals = { "numReads" : count }

#db.loci.update( {"individuals" : 
#db.loci.insert(locus)
#print "locus = ", re.sub(".fasta","",fasta), "; number alleles = ", len(loci_dict), "; length = ", len(loci_dict[loci_dict.keys()[0]])  , "; path = ", file, "; SNPs = ",SNP
	


samfile.close()




#get path from commandline - right now just doing single file but will upgrade to directory after working out the subsequent code
#parser = argparse.ArgumentParser(description='Get path to a bam file.')
#parser.add_argument('path',help='give the program the path to the folder of locus files')
#args = parser.parse_args()
#print 'Got this file:', args.path
