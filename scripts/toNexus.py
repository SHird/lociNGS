#!/usr/bin/python
# Filename: toNexus.py for lociNGS
# shird; 28 june 2011

#convert a given list of fasta files to nexus format

from Bio import SeqIO
from Bio.Alphabet import generic_protein, generic_dna, generic_nucleotide

def toNexus (list):
	for file in list:
		output_handle = file.replace(".fasta", ".nex")
		print output_handle
		SeqIO.convert(file, "fasta", output_handle, "nexus", generic_dna)