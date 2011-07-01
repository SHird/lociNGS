#!/usr/bin/python
# Filename: toIMa2.py for lociNGS
# shird; 28 june 2011

#convert a given list of fasta files to IMa2 format
import re
import pymongo
import json
import sys
from Bio import SeqIO
from Bio.Alphabet import generic_protein, generic_dna, generic_nucleotide
import pymongo
from pymongo import Connection

connection = Connection()
db = connection.test_database
loci = db.loci
demographic = db.demographic

###############################################################################
#this code from getPopFromMDB.py - will not be included when scripts are turned into a function
popsToUse = []
popsInds = {}
for arg in sys.argv:
	if arg.startswith('POP'):
		print arg
		popsToUse.append(arg)	
		popsInds[arg] = [-1]

print "popsToUse", popsToUse
pathsToGet = []
cursor = loci.find( {"populationsInFasta" : {'$all': popsToUse } }, {"path" : 1 , "_id" : 0 })
print "Setup cursor: %s" % cursor
for x in cursor:
#	print x["path"]
	pathsToGet.append(x["path"])

#for each population, create an array of all individuals that belong to it
for key in popsInds.keys():
	#set up a cursor to return all paths of documents that contain the individuals in the $all array
	cursor = demographic.find( {"Population" : key } , {"Individual" : 1 , "_id" : 0 })
	print "Setup cursor: %s" % cursor
	for x in cursor:
		print x['Individual']
		popsInds[key].append(x['Individual'])

###############################################################################
#get number of pops and number of loci from the previous data input
numberPops = len(popsToUse)
numberLoci = len(pathsToGet)

#put names of populations in tuple and string
namesPops = ""
print numberPops, numberLoci
print "popsToUse", popsToUse
namesPops = " ".join(sorted(popsToUse))
popsToUseTuple = tuple(sorted(popsToUse))

#get the IMa2 parameters from the IMa2InputFile.txt and put in listInput list
listInput = []
inputFile = open('IMa2InputFile.txt', 'r')
rows = [ line.strip().split(': ') for line in inputFile ]
for row in rows:
	listInput.append(row[1])

#this prints the header for the IMa2 file - write seems inefficient but it works
outputFile = open('IMa2_formatted.txt', 'w')
outputFile.write(listInput[0])
outputFile.write("\n")
outputFile.write(str(numberPops))
outputFile.write("\n")
outputFile.write(namesPops)
outputFile.write("\n")
outputFile.write(listInput[1])
outputFile.write("\n")
outputFile.write(str(numberLoci))
outputFile.write("\n")

for n in pathsToGet:    #from each input file, n, in the list, pathsToGet...
	dataList = []
	#create dictionary of population keys and save -1 as first value in value list
	for pops, inds in popsInds.iteritems():
		popsInds[pops][0] = -1
	currentLocusName = ""  #create and text edit locus name
	currentLocusName = re.sub('/.+/', '', n)
	currentLocusName = currentLocusName.replace(".fasta", "")  #also turn header into string, then print once
	for seq_record in SeqIO.parse(n, "fasta"): #open fasta files, read in indivdiual sequence records
		length = 0
		length = len(seq_record.seq)
		modSeqId = seq_record.id[:-3]
		for pop, inds in popsInds.iteritems():  #for everything in the popsInds dictionary
			if modSeqId in inds:			#if an individual is found in one of the population individual lists
				popsInds[pop][0] = popsInds[pop][0] + 1       #increase counter by 1
				digitLength = 9 - len(pop)     #to ensure seq ID is exactly 10 characters, count prefix, set counter to fill with zeros until 10
				stringID = pop + "_" + str(popsInds[pop][0]).zfill(digitLength) + " " + str(seq_record.seq) + "\n" #concatenate all the parts, including sequence
				dataList.append(stringID) 			
	locusHeader = ""     	#creating locus headers for output
	locusHeader = currentLocusName + " " 
	for each in popsToUseTuple:
		locusHeader = locusHeader + str(popsInds[each][0] + 1) + " "
	locusHeader = locusHeader + str(length) + " " + listInput[3] + " " + listInput[4] + "\n"
	print locusHeader
	dataList = sorted(dataList) #make sure in correct order
	outputFile.write(locusHeader)
	for x in dataList:
		outputFile.write(x)


#IMa2 outputformat should be:
# Description of data
# 2 [npops]
# POP1 POP2 [pop names in order]
# ((0,1):5,(2,3):4):6  (population tree)
# 2 (nloci)
# locus1Name 2 [nIndPop1] 2 [nIndPop2] 10 [length] H [mutModel] 1.0 [inhScalar] 0.0008 [mutRate] 0.0005 - 0.0009 [mutRateRange]
# indPOP1_1     ACGTGACGTA 
# indPOP1_2     ACGTGACGTA 
# indPOP2_1		AGGTGACGTA 
# indPOP1_2	  	AGGTGACGTA 
# locus2Name 2 [nIndPop1] 2 [nIndPop2] 12 [length] H [mutModel] 1.0 [inhScalar] 0.0008 [mutRate] 0.0005 - 0.0009 [mutRateRange]
# indPOP1_1     CCGACGTGCAGG 
# indPOP1_2     CCGACGTGCAGG 
# indPOP2_1		CCGATGTGCAGG 
# indPOP1_2	  	CCGACGTGCAGG 