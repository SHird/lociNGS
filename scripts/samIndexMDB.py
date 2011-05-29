#!/usr/bin/python
# Filename: samIndexMDB.py for lociNGS
# shird; 27 may 2011

import pysam
import argparse


#get path from commandline
parser = argparse.ArgumentParser(description='Get path to a bam file.')
parser.add_argument('path',help='give the program the path to the folder of locus files')
args = parser.parse_args()
print 'Got this file:', args.path


samfile = pysam.Samfile(args.path, "rb")

print samfile.nreferences

for alignedread in samfile.fetch('gi|336|RAIL|182'):
	print alignedread
	
samfile.close()