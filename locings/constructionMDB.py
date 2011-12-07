#!/usr/bin/env python
# Filename: constructionMDB.py for lociNGS
# shird; 11 july 2011
# this script initiates the db.loci collection in mongoDB and inputs many basic parameters to the database
#a text file with the names of the individuals is required
#takes path to locus directory as argument

#import argparse
import os
import pymongo
import re
import json
import simplejson
from seqlite_mod import SNPnumber
from Bio import SeqIO
from pymongo import Connection
from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename      
import pysam
from decimal import *

#for getting a connection to MongoDB via pymongo
connection = Connection()
db = connection.test_database
loci = db.loci
demographic = db.demographic

def fromLociFiles (folderOfFiles):
	print 'Got this folder:', folderOfFiles
	fasta_library = os.listdir(folderOfFiles)
	#print data to post collection in mongoDB
	for fasta in fasta_library:
		listOflists = []
		if fasta.endswith(".fasta"):
			file = os.path.join(folderOfFiles, fasta)
			print 'Got this file: ', file
			short = fasta.split(".")
			loci_list = list(SeqIO.parse(file, "fasta"))
			for eachLocus in loci_list:
				if eachLocus.id.endswith(".01"):
					current = []
					current = (eachLocus.id.replace(".01", ""), 0)
					listOflists.append(current)
			dict_listOflists = (listOflists)
			x = (dict(dict_listOflists))
			print "X IS: ", x
			SNP = SNPnumber(file)	#calls the SNPnumber function
			locus = {"locusFasta":fasta, "locusName":short[0], "locusNumber": re.sub(".+_(?P<dig>\d+)\D+","\g<dig>", fasta), "individuals": x, "indInFasta" : x.keys(), "length": len(loci_list[0]), "path": file, "SNPs" : SNP }   #, "length":len(loci_dict.keys()[0].seq)}
			loci.insert(locus)
			print "locusFasta = ", fasta, "; locusNumber = ", '\g<dig>' , "; individuals",	x, "; indInFasta" , x.keys(),"; SNPs = ", SNP, "; number alleles = ", len(loci_list), "; length = ", len(loci_list[0])  , "; path = ", file
	print "total of ", loci.count() , "loci"
	
def fromBAMFolder (BAMFolder):
	getcontext().prec = 2	
	print 'Got this folder:', BAMFolder
	bam_library = os.listdir(BAMFolder)
	bamPath = {"bamPath" : BAMFolder }
	db.loci.insert(bamPath)	
	#for each .bam file, count how many reads/locus and add to correct document in mongoDB
	for bam in bam_library:
		if bam.endswith(".bam") or bam.endswith(".sam"):
			print bam
			file = os.path.join(BAMFolder, bam)
			print 'Got this file: ', file
			if bam.endswith(".bam"):
				samfile = pysam.Samfile(file, "rb")
			else:
				samfile = pysam.Samfile(file, "r")
			print samfile.nreferences   #prints number of loci
			allLoci = samfile.references
			currentNameList = bam.split(".")
			currentName = currentNameList[0]
#			currentName = re.sub('.sorted.bam','', bam)
			namePath = "individuals."+currentName
			print "this is namePath", namePath, "this is currentName", currentName
			countBam = 0
			for line in samfile:
				countBam +=1
			totalUsed = 0
			for n in allLoci:   #foreach locus in the allLoci list
			#	print "on locus n in allLoci", n
				shortLocus = []
				shortLocus = n.split("|")
				totalbases = 0
				count = 0
				for alignedread in samfile.fetch(n):
				#	usedReads = len(alignedread)
					count = count + 1
					totalUsed = totalUsed + 1
					totalbases = totalbases + alignedread.rlen  #problem here: will count all bases even if coverage too low for individual to be called in loci file
				if count>0:
					cursor = db.loci.find( {"locusName" : shortLocus[-1]} , {"length":1, "_id" : 0} )
					for x in cursor:
						currentLength = x["length"]
						averageCov = Decimal(totalbases)/Decimal(currentLength)
						twoDecCov = float(Decimal(averageCov))
						db.loci.update( {"locusName" : shortLocus[-1] }, { '$inc' : { namePath : twoDecCov} } )
			demo = {"Individual" : currentName, "totalReads" : countBam, "usedReads": totalUsed, "percentUsed" : totalUsed*100/countBam }
			demographic.insert(demo)	

			samfile.close()	
	
def fromDemographicData (demoFile):
	#open tab delimited text file
	print 'Got this file:', demoFile
	f1 = open(demoFile, 'r')
	rows = [ line.strip().split('\t') for line in f1 ]
	#identify which column corresponds to the individuals and populations
	indColumnNum = rows[0].index("Individual")
	popColumnNum = rows[0].index("Population")
	print "popCol is ", popColumnNum, "indCol is ", indColumnNum
	#put all demographic data into list of lists and insert to mongodb
	listOfDemo = []
	popList = []
	indList=[]
	for row in rows[1:]: # all rows except the first header row
		popList.append(row[popColumnNum])
		for i, column in enumerate(row):
			if i != 0:
				print row[indColumnNum], rows[0][i], column
				db.demographic.update({"Individual":row[indColumnNum]}, { '$set' : {rows[0][i]: column }})
		indList.append(row[indColumnNum])
	for ind in indList:
		print ind, db.loci.find({ "indInFasta" : ind }).count()
		db.demographic.update( {"Individual" : ind }, { '$inc' : { "numLoci" : db.loci.find({ "indInFasta" : ind } ).count() } } )
	dictPopList={}
	print popList
	setList = set(popList)
	for one in setList:
		dictPopList[one] = []
	for row in rows[1:]:
		dictPopList[row[popColumnNum]].append(row[indColumnNum])
	loci = db.loci
	for each, pop_list in dictPopList.iteritems():
		print each, pop_list
		db.loci.update( {"indInFasta" : {'$in': dictPopList[each] } } , {'$addToSet' : {'populationsInFasta': each } }, multi=True )	
		
def getAllInds():
	demographic = db.demographic
	cursor = db.demographic.find({}, {"Individual":1, "_id":0})
	allInds=[]
	for x in cursor:
		allInds.append(x["Individual"])
	allIndsSorted = sorted(allInds)
	return allIndsSorted
	
def getPopDict():
	individuals = getAllInds()
	dictPopList={}
	popList = []
	demographic = db.demographic
	cursor = db.demographic.find({}, {"Population":1, "_id":0})
	for y in cursor:
		popList.append(y["Population"])
	setList = set(popList)
	for one in setList:
		dictPopList[one] = []
		cursor2 = db.demographic.find({"Population" : one}, {"Individual":1, "_id":0})
		for ind in cursor2:
			dictPopList[one].append(ind["Individual"])
	return dictPopList
	
def getDemoColumnsFromMDB():
	cursor = db.demographic.find( { } , {"_id" : 0 })
	columns = []
	for each in cursor[0].keys():
		columns.append(each)
	return columns