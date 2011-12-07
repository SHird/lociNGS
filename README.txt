lociNGS [v.1] README	

Copyright (C)  2011  Sarah M. Hird 
Permission is granted to copy, distribute and/or modify this document under the terms of the GNU Free Documentation License, Version 1.3 or any later version published by the Free Software Foundation; with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts. A copy of the license is included in the document entitled "GNU Free Documentation License".

LOCINGS: a simple database for reformatting and displaying multi-locus datasets

-----------------------------------------------------------------

1. INSTALLATION
	1.1. MongoDB
		1.1.1. Installation of MongoDB
		1.1.2. Correctly shutting down MongoDB
		1.1.3. How to tell if your computer is 32- or 64- bit
	1.2. lociNGS Easy Install **IMPORTANT**
	1.3. More info
		1.3.1. Python installation
		1.3.2. NumPy
		1.3.3. Biopython
		1.3.4. Pymongo
		1.3.5. Pysam
		1.3.6. seqlite_mod.py, ez_setup.py & distribute_setup.py
2. TO RUN lociNGS
	2.1. Short answer
	2.2. Contents of the folder
	2.3. Starting MongoDB **IMPORTANT**
	2.4. Starting lociNGS
3. INPUT FORMATS
	3.1 Import types
	3.2 Locus Names **IMPORTANT**
4. IMPORTING DATA
	4.1. Loci/fasta file(s)
	4.2. SAM/BAM NGS data
	4.3. Demographic data 
5. THE lociNGS INTERFACE
6. EXPORTING DATA
	6.1 Summary Data	
	6.2. NEXUS format
	6.3. IMa2 format
	6.4. Migrate format
7. TEST DATA
8. WHAT IF...
	8.1. ...lociNGS won't start?
	8.2. ...locus screen coverage buttons all display "0"?
	8.3. ...summary screen shows no data?
	8.4. Problems with IMa2 output
	8.5. Problems with installation
9. CONTACT

----------------------------------------------------------------

1. INSTALLATION
The program is dependent on several other pieces of software. lociNGS was written on MacOSX. lociNGS is available for download at https://github.com/SHird/lociNGS.  You will have to install MongoDB separately from the rest of the package.

1.1 MongoDB
1.1.1 Installation of MDB
Go to www.mongodb.org/downloads; 
Download correct version (if you don't know if your machine is 32 or 64 bit, see section 1.1.3.);
Double click the downloaded file – this should unpack it into a folder called something like "mongodb-osx-x86_64-1.8.2" (I would rename this folder "MongoDB" but you don't have to);
Move the MongoDB folder to Applications (or wherever you want to keep it. ***You will need mongod running every time you use lociNGS, so you should remember where you put the MongoDB folder.);
Make the directory that stores the data by opening a terminal and typing "mkdir –p /data/db" (without the quotations)
Go to the mongoDB folder, then the bin folder. 
Double click mongod. This should open a screen with something like this:

Last login: Wed Aug  3 08:12:53 on ttys001
/Applications/mongodb-osx-x86_64-1.8.1/bin/mongod ; exit;
HappyPappy:~ shird$ /Applications/mongodb-osx-x86_64-1.8.1/bin/mongod ; exit;
/Applications/mongodb-osx-x86_64-1.8.1/bin/mongod --help for help and startup options
Wed Aug  3 09:13:53 [initandlisten] MongoDB starting : pid=11886 port=27017 dbpath=/data/db/ 64-bit 
Wed Aug  3 09:13:53 [initandlisten] db version v1.8.1, pdfile version 4.5
Wed Aug  3 09:13:53 [initandlisten] git version: a429cd4f535b2499cc4130b06ff7c26f41c00f04
Wed Aug  3 09:13:53 [initandlisten] build sys info: Darwin erh2.10gen.cc 9.6.0 Darwin Kernel Version 9.6.0: Mon Nov 24 17:37:00 PST 2008; root:xnu-1228.9.59~1/RELEASE_I386 i386 BOOST_LIB_VERSION=1_40
Wed Aug  3 09:13:53 [initandlisten] waiting for connections on port 27017
Wed Aug  3 09:13:53 [websvr] web admin interface listening on port 28017

Leave this window open as you run lociNGS.

1.1.2. Correctly shutting down MongoDB
When you are finished with lociNGS and MongoDB, you must shut down MongoDB correctly. Click on the terminal window then press Control + C (the control button and the "c" button at once). If you don't do this, you'll have to find a file and delete it before you can get MongoDB running again – spotlight the file "mongod.lock" then drag it to the trash.

1.1.3. How to tell if your computer is 32- or 64-bit (from support.apple.com/kb/ht3696)
1. Choose About This Mac from the Apple () menu in the upper-left menu bar, then click More Info.
2. Open the Hardware section.
3. Locate the Processor Name [under the Hardware Overview].
4. Compare your Processor Name to information below to determine whether your Mac has a 32-bit or 64-bit processor.

Processor Name			32- or 64-bit
Intel Core Solo				32 bit
Intel Core Duo 				32 bit
Intel Core 2 Duo  	  		64 bit
Intel Quad-Core Xeon   		64 bit
Dual-Core Intel Xeon   		64 bit
Quad-Core Intel Xeon   		64 bit
Core i3						64 bit
Core i5						64 bit
Core i7						64 bit

1.2. lociNGS Easy Install
Download the lociNGS package from GitHub. You may either go to the website [ https://github.com/SHird/lociNGS ] and click the "Downloads" button (then choose the .tar.gz option). When the package has downloaded, double click the download, rename it to "lociNGS" and move the folder to the Applications folder (or wherever you'd like it to be).
Alternatively, if you have git on your machine, you can clone the directory by typing "git clone git@github.com:SHird/lociNGS.git /Applications/lociNGS". (This will install lociNGS into the Applications folder on MacOSX. You may move it.)


Open a terminal window, cd into the lociNGS folder
Type "python setup.py install" (each of these steps may take a couple of minutes to complete and will print lots of output to the terminal window)
Type "python distribute_setup.py"
Type "easy_install numpy" (lots of ugly output)
Type "easy_install biopython"

There should be a lot of output to the terminal screen.
Once the last command has finished, type "run_lociNGS.py" - this should open a new window with a short greeting and instructions...

1.3 More information
1.3.1 Python installation
MacOSX should come with a version of Python already installed. If you're not sure Python is on your machine:
In an open terminal, type "python". This should display something like "Python 2.7.1 (r271:86882M, Nov 30 2010, 10:35:34)" plus a couple of other lines of text followed by ">>>". Type "exit()".
If the above did not happen, go to www.python.org/getit/ for Python installation.

1.3.2 NumPy  - http://sourceforge.net/projects/numpy/files/ (they have an automated installer, download the file, double click, follow instructions)
For more information: http://www.scipy.org/Download. NumPy MUST be installed BEFORE Biopython!

1.3.3 Biopython - http://biopython.org/wiki/Download; download, double click, move the folder into the home directory, open terminal window, cd into folder, type three commands: [1] "python setup.py build", [2] "python setup.py test", [3] "sudo python setup.py install"

1.3.4 PyMongo - https://github.com/mongodb/mongo-python-driver; click "Downloads" button (upper-ish right of screen); click "1.11";  once it downloads, rename the folder "pymongo", put the folder in the home directory, cd into it, and type "python setup.py install"
For more information, other installation options: http://api.mongodb.org/python/current/installation.html

1.3.5 pysam - http://code.google.com/p/pysam/downloads/list; download file, double-click, move folder into Applications folder (or where you'd like to keep it), cd into folder and type two commands: [1] "python setup.py build", [2] "python setup.py install"

1.3.6 seqlite_mod.py, ez_setup.py & distribute_setup.py – these module are included with the distribution and you should not have to do much to install them.

2. TO RUN lociNGS:
2.1. Short answer: find and double click "mongod"; type "run_lociNGS.py" in a terminal window
2.2. Contents of the folder
I think it's easiest to keep everything in one place, but you don't necessarily have to. You need the following components in the lociNGS folder in order to run it:
	1.  locings folder
	2.  scripts folder
	3.  setup.py
	4.  README.txt
	5.  locus folder of fasta files*
	6.  BAM and BAI folder*
	7.  Tab-delimited text file of demographic data* 
	8.  IMa2 input file (if formatting for IMa2 or Migrate, format described below)

*These folders/files don't need to be in the lociNGS folder.
After the program is run for the first time, an additional four files will appear with the extension .pyc (for each of the python scripts above). These can be removed but are used to speed up the running of python scripts.

2.3. Starting MongoDB
MongoDB must be running before lociNGS is started. To do this, you can find "mongod" with the Finder and double click it; or go to the MongoDB/bin folder and double click "mongod"; or, from the terminal, you can cd into the MongoDB folder, then cd into "bin" and type "./mongod". Leave the window open and when you are finished with lociNGS YOU MUST EXIT MONGOD BY PRESSING CONTROL+C (TOGETHER). If you forget to do this, the mongod process will be improperly shut down and not start the next time you need it. If that happens, see Section 1.1.2. above.

2.4 Starting lociNGS
To run the program, open a terminal window and type "run_lociNGS.py". This should open a new window with these basic instructions: "Please enter the data in the order listed in the Import Menu. Once data has been loaded via the Import Menu, press ‘Display the data'." Don't close this window – it will close the program.

3. INPUT FORMATS
3.1 Import types
lociNGS uses three imports. 
[1] The first is a folder of files that contain loci in fasta format. These files should have ".fasta" as their final extension. The folder may be located anywhere.
[2] The second import is a folder of indexed bam files from a short read aligner. Each bam (and corresponding .bai) file should correspond to an individual in the dataset. I'm working on getting sam format to work too, but for right now, indexed bam works best.
[3] The third is a tab-delimited text file that contains demographic data for the individuals in the dataset. There must be at least two columns, labeled "Individual" and "Population", which contain information on the name of the individual (as it appears in locus files and BAM file names) and which population the individual came from (these can be numbers or letters). The file may contain as many columns as you'd like, they will appear on the "Summary Screen" of the program.
*lociNGS will run and reformat loci if just [1] loci and [3] demographic data are entered. 

3.2 Locus Names **IMPORTANT**
The names of the files from import [1] that correspond to loci need to match with the locus names in the BAM files, import [2]. Basically, if your loci are called "locus1", "locus2" and "locus3", the fasta files need to be called "locus1.fasta", "locus2.fasta" and "locus3.fasta" and the loci in your BAM file need to be "locus1", "locus2" and "locus3". There are a few exceptions - the locus file name comes from anything before the first "." in the locus file name - so the files could be called "locus1.aln.fasta" or "locus1.080911.fasta" as long as the prefix before the first "." matches the BAM loci. Also, the BAM loci may have prefixes, but this time, due to common GenBank annotation, you may add things to the BAM loci names with a "|" as a separator. So BAM loci may be called something like "gi|323|testdata|locus1" as long as the last piece of the header matches the fasta loci names.
Any combination of the below files will work in lociNGS. Please feel free to contact me if you are unsure if your locus names are causing the program difficulty.

FASTA FILE - must contain the locus name before the first period and have ".fasta" as final extension
locus1.fasta
locus1.aln.fasta
locus1.test.data.fasta

BAM LOCUS NAME - must contain the locus name after the final | or as the only text
locus1
fake|any text you want|locus1
gi|323|fakeData|08august2011|locus1

4. IMPORTING DATA
4.1 Loci/fasta file(s)
Step 1 in the import menu will open a window where you should find and select the locus folder. After successful import, the lociNGS screen will tell you. The terminal window will print data as the files are read. It should be a lot of text that looks something like: 
"Got this file:  /Users/shird/Desktop/juncoLoci/JUNCOmatic_63_aln.fasta
locusFasta =  JUNCOmatic_63_aln.fasta ; individuals {'J12': 0, 'J09': 0, 'J18': 0, 'J19': 0, 'J01': 0, 'J17': 0, 'J03': 0, 'J11': 0, 'J05': 0, 'J04': 0, 'J10': 0, 'J06': 0} ; indInFasta ['J12', 'J09', 'J18', 'J19', 'J01', 'J17', 'J03', 'J11', 'J05', 'J04', 'J10', 'J06'] ; SNPs =  5 ; number alleles =  24 ; length =  284 ; path =  /Users/shird/Desktop/juncoLoci/JUNCOmatic_63_aln.fasta"

4.2 SAM/BAM NGS data
Step 2 will import the net-gen alignments - you should find and select the indexed sam or bam folder. lociNGS will update as the import is finished. The terminal window will print data as the files are read. It will look something like this for each file: 
"Got this folder: /Users/shird/Documents/Dropbox/juncoBam
Got this file:  /Users/shird/Documents/Dropbox/juncoBam/J01.sorted.bam
730
individuals.J01"
Please note that .bam files are binary versions of .sam files and thus .bam files are smaller and will load faster (perhaps much faster) than .sam files. One way to convert .sam files to .bam files is the "view" tool in the samtools package (http://samtools.sourceforge.net/)


4.1.3 Demographic data
The final step imports the demographic data in a tab delimited file - find and select the tab delimited demographic data file. Again, lociNGS will tell you when the import has been successful and the terminal will print data for each individual as the files are read:
"{'Longitude': '-109.876', 'Individual': 'J01', 'Location': 'NoPlace, TX', 'Latitude': '45.678', 'Species': 'Junco hyemalis', 'Population': 'POP1'}
POP1"

5. THE lociNGS INTERFACE
lociNGS has three screens meant to show you how much data is associated with each individual in your dataset. The first screen will display text updates as the program completes functions. The second is a summary screen where each individual is a row and the demographic data are the columns. There is also a "numLoci" column that displays the number of loci called for that particular individual. If you click one of these numLoci buttons, the third screen appears that displays the specific loci. On this screen there are five columns:
Locus Name = the locus file/locus name
Length = length of the locus
Coverage_This_Ind = how many raw reads from this individual aligned to the locus. If this button is pressed, a fasta file is generated that contains these reads. This file will be printed to the directory that contains the lociNGS scripts. 
Number_Inds = how many individuals are present in the locus (fasta) file
Coverage_Total = how many raw reads from any individual aligned to the locus. If this button is pressed, a fasta file that contains the reads is generated and printed to the lociNGS directory.

6. EXPORTING DATA
You may export summary data or the raw data in three formats (NEXUS, IMa2 and MIGRATE); you may select either specific individuals from your dataset you'd like to include in your files OR you may select a set of populations. If you select populations, lociNGS will scan the locus files for any locus that contains at least one individual from each of the selected populations and reformat these loci.

6.1 Summary Data
Selecting the "Export Data -> SummaryData" option will print all the data displayed when you press "Display the data" on the main menu. It will print two files, one for the summary screen and a second that contains all the information for all individuals and loci. This can be a large file but is useful for sorting data in a spreadsheet to report various coverage statistics.

6.2 NEXUS format
NEXUS format requires aligned data. Files will be printed with a ".nex" extension.

6.3 IMa2 format
IMa2 requires an additional input file to describe some of the dataset specific parameters. I've included an example file. Please see IMa2 manual (available at http://lifesci.rutgers.edu/~heylab/ProgramsandData/Programs/IMa2/Using_IMa2_10_13_10.pdf) for more information on the parameters.
The IMa2 extra parameters file must be named "IMa2InputFile.txt" and should follow the format of the included IMa2InputFile format – just type the values you need after the colon.

Header Line: Type whatever you want here that will identify your IMa run
Population Tree: ((0,1):5,(2,3):4):6
Inheritance Scalar: 1
Mutation Model: H
Mutation Rate (optional): 0.000008
Mutation Rate Range Lower (optional): 0.000007
Mutation Rate Range Upper (optional): 0.000009

If you aren't using the Mutation Rate Parameters, delete them from the file. If you are, please note that the mutation rate you enter needs to be the substitutions / site mutation rate; lociNGS will multiply this rate by the length of each locus (# of sites) to give a per base mutation rate (which is what the program requires). Also note that the Population Tree is required and is a very specific format, so please check with the IMa2 documentation for how to write it.

Also note, the same inheritance scalar and mutation model will be printed for every locus. If you have different types of data (autosome, mtDNA, X- or Y-linked data), you might want to put the similar types together in a folder and load them independently into lociNGS, and export with the correct inheritance scalar in the IMa2InputFile. You can then concatenate the files.

6.4 Migrate format
Migrate format requires that an IMa2 additional file be in the folder, but doesn't use the information – so if you just need Migrate output, leave the example IMa2InputFile.txt in the folder as is.
	
7. TEST DATA
I've included a very small test dataset, containing four individuals and five loci. 

8. WHAT IF...? 
I've attempted compiling a list of potential problems - email me (please) if you encounter something not on this list so I can add it for other users.

8.1. ...lociNGS won't start? 
If this ("pymongo.errors.AutoReconnect: could not find master/primary") is the last line of output printed to the terminal window, it means that mongod is not running. In the MongoDB/bin folder, double click on "mongod" then try starting lociNGS again.
 
8.2. ...locus screen coverage buttons all say "0"?
This could be due to the name of the loci in the SAM/BAM files not corresponding correctly to the name of the fasta locus files. Double check by referring to section 3.2 above. Also, if you import the SAM/BAM files before the loci files, you'll get 0s in the coverage columns.

8.3. ...summary screen shows no data?
This could be due to the names of individuals not corresponding correctly between individuals in the fasta files and the demographic data text file. The demographic table needs to have a minimum of two columns, "Individual" and "Population". Make sure the names of the indivdiuals are the same as the fasta files. This could also be due to not importing a demographic data file. You need to import at least a list of the individuals and what population they belong to. 

8.4. ...read data won't print?
Have you moved any folders? When first importing the data, a path is saved to the database, so if you move the sam/bam files, the program won't be able to find the folder. Try reimporting.

8.5. Problems with IMa2.
The IMa2InputFile.txt needs to look almost exactly like the one I've provided. Please let me know if you have specific problems with any of the output formats. 

8.6. Problems with installation
First, check that you are using Python 2.7. Open a terminal and type "python". You should see something like this: 

Python 2.7.1 (r271:86882M, Nov 30 2010, 10:35:34) 
[GCC 4.2.1 (Apple Inc. build 5664)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>

If your Python is version 2.5 or 2.6, try downloading Python 2.7 and reinstalling lociNGS (section 1.2 above). If you have Python 2.7, type the following commands (after the >>>) to make sure all the packages installed correctly - if you get no feedback, it is installed correctly:
"import numpy"
"import Bio"
"import pysam"
"import pymongo"
"import simplejson"
"import cython"
(to exit the python prompt, type "exit()")

If you get an error like: 
"Traceback (most recent call last):
File "<stdin>", line 1, in <module>
ImportError: No module named numpy"
then that package did not install correctly. You can go to the websites listed in section 1.3 above and install the problem package independently and rerun the installation steps in section 1.2 above.

If these suggestions do not work, please contact me with the error messages you're receiving and I'll try to help you get the program running. I understand there's something especially infuriating about buggy software, so please email me!

9. CONTACT
Please feel free to contact me about any issues you're having with lociNGS or the dependent software. I'd be more than happy to do what I can – 

Sarah Hird
shird1@tigers.lsu.edu