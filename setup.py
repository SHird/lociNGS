#!/usr/bin/env python
"""Setup file and install script for lociNGS.
"""
from setuptools import setup, find_packages

setup(name = "lociNGS",
	version = "1.0",
	author = "Sarah Hird",
	author_email = "shird1@tigers.lsu.edu",
	description = "lociNGS: a simple database for reformatting and displaying multi-locus datasets",
	url = "https://github.com/SHird/lociNGS",
	namespace_packages = ['locings'], 
 	packages = find_packages(),
	scripts = [	'scripts/run_lociNGS.py'],
	install_requires = [
		"numpy >= 1.6.1",
		"biopython >= 1.57",
		"pysam >= 0.4.1",
		"pymongo >= 1.11",
		"simplejson"]
)