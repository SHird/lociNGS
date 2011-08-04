#!/usr/bin/env python
# version 1.07
#originally written by Steve Haddock, modified by S. Hird
#original full script seqlite.py available http://www.mbari.org/staff/haddock/scripts/


def SNPnumber(fileFromProgram):
	"""Reads in FASTA or NBRF files, with Mac or unix CRs and
	outputs (or #prints) files with only unique sequences and sites included
	v. 1.07 -- started to add support for sys.arg and skipping duplicate names
	"""
	
	import re
	import sys
	from sets import Set as set # useful for version 2.3?
	
	### Change settings here
	keepall=False # don't chop out conserved sites? just redundant seqs
	printtoscreen=False # false means it will save to the outfile
	printhtml=False
	savetofile=False
	sortthem=True
	appendseqs=False
	skipseq=False 
	skipcount=0
	fractionseqs=2.0 # proportion below which to label (make 4.0 for 25%)
	
	#other definitinos
	firstseq = False
	seqname= ''
	dataset={}
	skipnext=False
	nbrf=False
	backseqs={}
	
	# First, load in the seqs into a dictionary
	if len(sys.argv)>1:
		inputfilename = fileFromProgram
	else: 
		print usage

	try: 
		inFile = open(inputfilename, 'r') 
		alllines = inFile.readlines() # trying a different approach
	# this is easier for the \n detection, but for very large files,
	# it is probably better to use the original formulation
	# plus, does readlines() work in 2.4??
	
	except IOError:
		print"\nCan't find the file %s. Are you in the right directory?" % inputfilename
		print 
		print
		printtoscreen=True # false means it will save to the outfile
		printhtml=False
		savetofile=False
		alllines=[]
		exit(1)
	
	if alllines[0].find('\r')>0:
		print
		print "MacFormat (use unix file when possible)."
		lines=alllines[0].split('\r')
		# print "Found %d lines" % len(lines)	
		
	else:
		lines=alllines
		
	# print len(lines)
	
	for inline in lines:
		line=inline.strip('\r').strip('\n') 
		if skipnext: # needed for NBRF format
			skipnext=False
		else:
			if line and line[0]=='>':
				if firstseq:
					if dataset.get(seqname) in backseqs.keys(): # gets the sequence from the previous record n the loop
						pass #print "Same sequence in",backseqs[dataset[seqname]],"and",seqname
					else:
						backseqs[dataset[seqname]]=seqname
						
				skipseq=False # if we are skipping a repeat, need to reset now
				if line.startswith('>DL;') or line.startswith('>P1;'):
					nbrf=True
					# print 'NBRF format'
					seqname=line.split()[1]  # defaults to space
					skipnext=True
				else:
					seqname=line[1:]
					# print seqname
				if seqname in dataset.keys() and (not appendseqs):
					#print "Duplicate sequence name skipped" , seqname
					skipcount+=1
					skipseq=True # seqname already exists -- skip to next >	
							
				firstseq=True
			elif skipseq:
				continue
			elif firstseq: # we know it's not the first line
				# print  'we have sequence'
				try:
					dataset[seqname] +=  line
				except:
					dataset[seqname]  =  line
				# this should be modified to append
	
	inFile.close()
	
	if nbrf: print "NBRF format" 
	
	dataname=[]
	# removes identical sequences -- make another way
	# to pupulate catacol_list if you want to keep these
	# ->it would just be dataset.items()
	
	# modified to do this above
	# for key, value in dataset.items():
	# 	backseqs[value]=key  
	
	datarows = backseqs.keys()
	dataname = backseqs.values()
	numseqs = len(dataname) # after redundant taxon removal
	
	# print dataname
	# print datarows
	
	
	# now get rid of invariable columns
	datacols=[]
	
	# don't ask me how this works!!
	# transpose the matrix and stuff with - if variable
	datacol_list = map(lambda*datarows: [elem or '-' for elem in datarows], *datarows) 
	
	# remove invariable columns by testing for the length of set()
	# this function leaves unique values
	regsub = re.compile(r'[-?xX]')
	labelindex = {}
	colnum=0
	
	for ri in range(len(datacol_list)):
		tempcol=(''.join(datacol_list[ri]))
		# Ignore dashes in making consensus
		try: 
			testset=set(regsub.sub('',tempcol))
		except NameError:
			#print "failed to find set command"
			#print 'update to python 2.5 or add the line "from sets import Set as set"'
			printtoscreen=False # false means it will save to the outfile
			printhtml=False
			savetofile=False
			break
		if len(testset)>1 or keepall: # keepall will be the column saver
			datacols.append(tempcol)
			starts=[]
			currentindex=[]
			for lett in testset:
			# should define this as a fraction above
				currentcount=tempcol.count(lett) 
				# print str(colnum) +':'+ lett + ':'+ str(currentcount)
				# ** Can change this to MORE THAN **
				if currentcount < (numseqs/fractionseqs):
					starts = [match.start() for match in re.finditer(lett, tempcol)]
					currentindex.extend(starts)
				# print str(colnum) +':' +lett +':' + str(starts)
			for eyes in set(currentindex):
				try:
					labelindex[eyes].extend([colnum])
				except KeyError:
					labelindex[eyes]=[colnum]
			colnum+=1
	
	## DEBUG ##
	# print 'labelindex', labelindex
	
	# return the sequences to their original orientation...
	datarow_sub=[]
	if len(datacols) > 0:
		datarow_list= map(lambda *datacols: [elem or '-' for elem in datacols], *datacols) 
	
		# these are lists, so have to "pack" them back into strings
		for ri in range(len(datarow_list)):
			datarow_sub.append(''.join(datarow_list[ri]))
	
		# print datarow_sub
		# (create a numbered list that we can use to look up in the index order later)
	
		indexholder=range(numseqs)
		# pull names out of original list to add to new list...
	
		indexdict = dict(zip(datarow_sub,indexholder))
		
		# make a dictionary with d['a'][0] = index and d['a'][1] as name
	
		## DEBUG ##
		# print 'indexdict:',indexdict
		
		# remove repeats now that the list has been shortened
		sortkeys = list(set(datarow_sub))  # still unsorted
		
		# sort keys (i.e., sequences) to group by similarity
		if sortthem:
			sortkeys.sort()
		
		# # use this -- a backwards dictionary again
		outdict=dict(zip(datarow_sub,dataname))
		# needed???
		datarow_sub.sort()
		
		########### need to check that we aren't messing things up with all this sorting!
		
		origname=dataset.keys()
		origval=dataset[origname[0]];
		
		# remove 1 from the length if NBRF format because of the asterisk
		introout='Processing file '+inputfilename 
		#print introout
		firstout= "From a list of %d sites in %d sequences," % (len(origval)-1*nbrf, len(origname))
		#print firstout
		secondout= "%d unique sites remain in %d sequences\n" % (len(datarow_sub[0]), len(sortkeys))
		
		number_of_SNPS = (len(datarow_sub[0]))
		
		#print'This is the SNP # ', SNPSnumber
		#print secondout
		return number_of_SNPS
	
	else:
		return 0 ;
	
	
if __name__ == "__main__":
		print info.__doc__
