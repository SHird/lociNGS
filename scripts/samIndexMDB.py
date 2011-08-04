#!/usr/bin/python
# Filename: samIndexMDB.py for lociNGS
# shird; 27 may 2011
#this script requires a directory of indexed bam files (i.e., a .bam and a .bam.bai file per individual)
#from the directory, a mongoDB database (created with the locusIndexMDB.py script) is updated to include how many reads align to each locus in a reference genome
#takes directory of bam files as argument


import pysam
import argparse
import os
import pymongo
import re
from Bio import SeqIO
from pymongo import Connection
from decimal import *

getcontext().prec = 2

#for getting a connection to MongoDB via pymongo
connection = Connection()
db = connection.test_database
loci = db.loci
demographic = db.demographic

#get path to the bam directory
parser = argparse.ArgumentParser(description='Get path to bam files.')
parser.add_argument('path',help='give the program the path to the folder of locus files')
args = parser.parse_args()
print 'Got this folder:', args.path
bam_library = os.listdir(args.path)
bamPath = {"bamPath" : args.path }
db.loci.insert(bamPath)

#for each .bam file, count how many reads/locus and add to correct document in mongoDB
for bam in bam_library:
	if bam.endswith(".bam"):
		file = os.path.join(args.path, bam)
		print 'Got this file: ', file
###will need to index the bam files if not already done?
		samfile = pysam.Samfile(file, "rb")
		print samfile.nreferences   #prints number of loci
		allLoci = samfile.references
		currentName = re.sub('/.+/', '', file)
		currentName = re.sub('.sorted.bam','', currentName)
		namePath = "individuals."+currentName
		countView = pysam.view("-c",file)  #counts number of reads in bam file
		for line in countView:
			line = line.strip() 
		print "line is now ", line
		db.demographic.update( {"Individual" : currentName }, { '$set' : { "totalReads" : line } } )		

#this counts the matches of reads to a given locus in allLoci, adds 1 for each match then updates MDB
		for n in allLoci:   #foreach locus in the allLoci list
			totalbases = 0
			count = 0
			for alignedread in samfile.fetch(n):
				count = count + 1
				totalbases = totalbases + alignedread.rlen  #problem here: will count all bases even if coverage too low for individual to be called in loci file
			m = re.sub('.+\|.+\|','',n)	
		#	print n, totalbases
			if count>0:
				cursor = db.loci.find( {"locusNumber" : m} , {"length":1, "_id" : 0} )
				for x in cursor:
					currentLength = x["length"]
					averageCov = Decimal(totalbases)/Decimal(currentLength)
					twoDecCov = float(Decimal(averageCov))
					db.loci.update( {"locusNumber" : m }, { '$inc' : { namePath : twoDecCov} } )
					print "updated locusNumber", m, "so that ", namePath, "is now ", twoDecCov, "because totalbases is ", totalbases, "and length is", currentLength
		
		#		print n, count  #can turn this off to quicken script - prints every locus and it's count


samfile.close()