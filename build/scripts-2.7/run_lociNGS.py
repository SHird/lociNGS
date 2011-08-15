#!/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
#main script for lociNGS
#S.Hird 9 August 2011

from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename, askdirectory
#from tkFileDialog   import askdirectory
from locings.constructionMDB import *
from Tix import ScrolledWindow
from locings.convertingLociNGS import *
from pymongo import Connection

#MongoDB connection
connection = Connection()
db = connection.test_database
loci = db.loci
demographic = db.demographic

class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
    	self.pack()
    	self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(anchor=anchor, expand=YES)
            self.vars.append(var)   
    def state(self):
    	for var in self.vars:
    		return map(lambda var: var.get(), self.vars)

class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only works if you use the grid geometry manager.
    def set(self, lo, hi):
    	if float(lo) <= 0.0 and float(hi) >= 1.0:   # grid_remove is currently missing from Tkinter!
        	self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"
	
class MainScreen(Frame):	
	def callbackFasta(self):
		FastaFolder = askdirectory() 
		fromLociFiles(FastaFolder)	
		success = "Successful Import of:  "+FastaFolder
		self.createWidgets(success, "BLACK")

	def callbackBAM(self):
		BAMfolder = askdirectory() 
		fromBAMFolder(BAMfolder)
		success = "Successful Import of:  "+BAMfolder
		self.createWidgets(success, "BLACK")
    
	def callbackDemo(self):
		Demofile = askopenfilename() 
		fromDemographicData(Demofile)
		success = "Successful Import of:  "+Demofile+"\n"
		self.createWidgets(success, "BLACK")
		
	def clearMDB(self):
		db.demographic.remove()
		db.loci.remove()
		success = "\n*** DATABASE CLEARED ***\n"
		self.createWidgets(success, "RED")

	def someReads(self, string, X):
		dir = getRawFastaFromBAM(string,X)
		locShort = X.split(".")
		success = "Reads for   [INDIVIDUAL: "+string+", LOCUS: " + locShort[0]+ "]   printed to: "+dir
		self.createWidgets(success, "BLUE")
		
	def allReads(self, X):	
		dir = getAllRawFastaFromBAM(X)
		locShort = X.split(".")
		success = "All reads for   [LOCUS: "+ locShort[0] + "]   printed to: "+dir
		self.createWidgets(success,"BLUE")

	def createLocusWindow(self, string):
		root = Tk()
		vscrollbar = AutoScrollbar(root)
		vscrollbar.grid(row=0, column=1, sticky=N+S)
		hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
		hscrollbar.grid(row=1, column=0, sticky=E+W)
		h = root.winfo_screenheight()
		canvas = Canvas(root,yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set, width = 600, height = h)
		canvas.grid(row=0, column=0, sticky=N+S+E+W)
		vscrollbar.config(command=canvas.yview)
		hscrollbar.config(command=canvas.xview)
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		frame = Frame(canvas)
		frame.rowconfigure(1, weight=1)
		frame.columnconfigure(1, weight=1)	
		label1=Label(frame, text = "Locus Name").grid(row = 0, column = 0, padx = 6)
		label2=Label(frame, text="Length").grid(row=0, column=1, padx = 6)
		label9=Label(frame, text="SNPs").grid(row=0, column=2, padx = 6)
		label3=Label(frame, text="Coverage_This_Ind").grid(row=0, column=3, padx = 6)
		label4=Label(frame, text="Number_Inds").grid(row=0, column=4, padx = 6)
		label5=Label(frame, text="Coverage_Total").grid(row=0, column=5, padx = 6)
		locList = []
		cursorLoc = loci.find( {"indInFasta": string})
		for y in cursorLoc:
			locList.append(y["locusName"])
		for locus in locList:
			label9 = Label(frame, text = locus).grid(row=1+locList.index(locus), column = 0, padx = 6)
			cursor = loci.find( {"locusName" : locus })
			for x in cursor:
				X = x["locusFasta"]
				locusTotal = 0
				label6=Label(frame, text = x["length"] ).grid(row=1+locList.index(locus),column = 1, padx = 6)
				label8=Label(frame, text = x["SNPs"] ).grid(row=1+locList.index(locus),column = 2, padx = 6)
				label7=Label(frame, text=str(len(x["indInFasta"]))).grid(row=1+locList.index(locus), column=4, padx = 6)
				fake = {}
				fake = x["individuals"]
				print "this fake now:", fake
				for each in fake:
					locusTotal = locusTotal + fake[each]
					print "currentLocustotal:", locusTotal
					Y = fake[string]
					print "this is Y:", Y 	
			#	print "X is", X, "string is:", string, "final locus total:", locusTotal	
				button1=Button(frame, text = fake[string], command = lambda X=X: self.someReads(string, X)).grid(row=1+locList.index(locus), column = 3, padx = 6)
				button2 = Button(frame, text = locusTotal, command = lambda X=X: self.allReads(X)).grid(row=1+locList.index(locus), column = 5, padx = 6)					
		canvas.create_window(0, 0, anchor=NW, window=frame)
		frame.update_idletasks()
		canvas.config(scrollregion=canvas.bbox("all"))
		root.title(string)
		root.mainloop()
	
	def createSummaryWindow(self):
		indList = getAllInds()
		root = Toplevel()
		vscrollbar = AutoScrollbar(root)
		vscrollbar.grid(row=0, column=1, sticky=N+S)
		hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
		hscrollbar.grid(row=1, column=0, sticky=E+W)
		w, h = root.winfo_screenwidth(), root.winfo_screenheight()
		canvas = Canvas(root,yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set, width = 800, height = h)
		canvas.grid(row=0, column=0, sticky=N+S+E+W)
		vscrollbar.config(command=canvas.yview)
		hscrollbar.config(command=canvas.xview)
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		frame = Frame(canvas, width=768, height=576)
		listOfColumns = ["Individual", "Population", "numLoci"]	
		list1 = getDemoColumnsFromMDB()
		newList1 = []
		for each in list1:
			if each in ("Individual", "Population", "numLoci"):
				pass
			else:
				listOfColumns.append(each)
		for i in listOfColumns:
			frame.label=Label(frame, text = i).grid(row=0, column=listOfColumns.index(i), padx = 6)					
		indList = getAllInds()
		for ind in indList:
			label9 = Label(frame, text = ind).grid(row=1+indList.index(ind), column = 0, padx = 6)
			cursor = demographic.find( {"Individual" : ind })
			for x in cursor:
				X = ind
				for i in listOfColumns:
					if listOfColumns.index(i) != 2:
						label=Label(frame, text = x[i] ).grid(row=1+indList.index(ind),column = listOfColumns.index(i), padx = 6)
				button=Button(frame, text=x["numLoci"], command=lambda X = X: self.createLocusWindow(X)).grid(row=1+indList.index(ind), column=2, padx = 6)
		frame.rowconfigure(1, weight=1)
		frame.columnconfigure(1, weight=1)
		canvas.create_window(0, 0,anchor=NW, window=frame)
		frame.update_idletasks()
		canvas.config(scrollregion=canvas.bbox("all"))
		root.title("lociNGS")
		root.mainloop()

	def POPMENUprograms(self, list):
		programs = ['Nexus', 'IMa2', 'Migrate']
		poproot = Toplevel()
		Label(poproot,text = "Select all that apply:").pack(side=LEFT)
		popmen = Checkbar(poproot, programs)
		popmen.pack(side=LEFT)
		def allstates(): 
		#	print "these are results", popmen.state()
			if popmen.state()[0] == 1:
				dirName = toNexus(list)
				dirFinal = "Nexus file(s) printed to: "+dirName		
				self.createWidgets(dirFinal, "BLUE")
			if popmen.state()[1] == 1:
				dirList = toIMa2(list)
				dirFinal = "IMa2 file printed to: "+dirList[1]		
				self.createWidgets(dirFinal, "BLUE")
			if popmen.state()[2] ==1:
				dirList = toIMa2(list)
				toMigrate(dirList[0])
				dirFinal = "Migrate file printed to: "+dirList[1]		
				self.createWidgets(dirFinal, "BLUE")
			poproot.destroy()
		popmen.config(relief=GROOVE, bd=2)
		Button(poproot, text='Save', command=allstates).pack(side=RIGHT)
	
	def pickInds(self):
		allInds = getAllInds()
		indroot = Toplevel()
		Label(indroot,text = "Select all that apply:").pack(side=LEFT)
		indmen = Checkbar(indroot, allInds)
		indmen.pack(side=LEFT)
		def allstates(): 
			indsToUse = []
			print "these are results", indmen.state()
			for each in range(len(indmen.state())):
				if indmen.state()[each] == 1:
					indsToUse.append(allInds[each])
			cursor = db.loci.find( {"indInFasta": {'$all' : indsToUse} }, {"path" : 1, "_id":0})
			indPathList = []
			for m in cursor:
				indPathList.append(m["path"])
			self.POPMENUprograms(indPathList)
			indroot.destroy()
		indmen.config(relief=GROOVE, bd=2)
		Button(indroot, text='Save', command=allstates).pack(side=RIGHT)
	
	def pickPops(self):
		popsDict = getPopDict()
		popsList = []
		for item in popsDict:
			popsList.append(item)
		popsList = sorted(popsList)
		popsroot = Toplevel()
		Label(popsroot,text = "Select all that apply:").pack(side=LEFT)
		popsmen = Checkbar(popsroot, popsList)
		popsmen.pack(side=LEFT)
		def allstates(): 
			popsToUse = []
			print "these are results", popsmen.state()
			for each in range(len(popsmen.state())):
				if popsmen.state()[each] == 1:
					popsToUse.append(popsList[each])
			cursor = db.loci.find( {"populationsInFasta" : { '$all' : popsToUse } } , {"path" : 1 , "_id" : 0 })
			popPathList = []
			for n in cursor:
				popPathList.append(n["path"])
			print popPathList
			self.POPMENUprograms(popPathList)
			popsroot.destroy()
			#add popmen.state to array?
		popsmen.config(relief=GROOVE, bd=2)
		Button(popsroot, text='Save', command=allstates).pack(side=RIGHT)
	
	def createWidgets(self, string, colorText):
		self.makeMenuBar()
		strVar = StringVar()
		strVar.set(string)
		L = Label(self, textvariable=strVar, fg=colorText).pack(expand=YES, fill=BOTH)
	
	def makeMenuBar(self):
		self.menubar = Menu(self.master)
		self.master.config(menu=self.menubar)
		self.casmenu()
	    
	def openREADME(self):
		f1 = open("README.txt", 'r')
		root = Toplevel()
		vscrollbar = AutoScrollbar(root)
		vscrollbar.grid(row=0, column=1, sticky=N+S)
		hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
		hscrollbar.grid(row=1, column=0, sticky=E+W)
		w, h = root.winfo_screenwidth(), root.winfo_screenheight()
		canvas = Canvas(root,yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set,width = 750, height = h) 
		canvas.grid(row=0, column=0, sticky=N+S+E+W)
		vscrollbar.config(command=canvas.yview)
		hscrollbar.config(command=canvas.xview)
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		frame = Text(canvas, width=100, height=300)
		for line in f1:	
			line.strip()
			frame.insert('end', line)						    
		frame.rowconfigure(1, weight=1)
		frame.columnconfigure(1, weight=1)
		canvas.create_window(0, 0,anchor=NW, window=frame)
		frame.update_idletasks()
		canvas.config(scrollregion=canvas.bbox("all"))
		root.title("README")
		root.mainloop()
	
	def buttons(self):
		root = Toplevel()
		canvas = Canvas(root, height=250, width=490) 
		canvas.grid(row=0, column=0, sticky=N+S+E+W)
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		frame = Text(canvas)
		text1 = """numLoci = number displayed on the button corresponds to the number\nof loci where the individual has written alleles. Pushing this\nbutton will take you to the next screen - the screen that gives\ndetails about each of the loci.\n\nCoverage_This_Ind = number displayed on the button corresponds to\nthe number of raw reads that aligned to that particular locus\nin that particular individual. Pushing this button will output those\nraw reads to a file and the file's location will be output to the\nlociNGS main screen.\n\nCoverage_Total = number displayed on the button corresponds to the\nnumber of raw reads that aligned to that particular locus for all\nindividuals. Pushing this button will output all the raw reads for\nthe locus to a file an the file's location will be output to the\nlociNGS main screen.\n"""
		frame.insert('end', text1)						    
		frame.rowconfigure(1, weight=1)
		frame.columnconfigure(1, weight=1)
		canvas.create_window(0, 0, anchor=NW, window=frame)
		frame.update_idletasks()
		canvas.config(scrollregion=canvas.bbox("all"))
		root.title("lociNGS Buttons")
		root.mainloop()
		
		
	def casmenu(self):
		casmenu = Menu(self.menubar)
		casmenu.impmenu = Menu(casmenu)
		casmenu.expmenu = Menu(casmenu)				
		casmenu.impmenu.add_command(label='1. Loci/fasta file(s)', command=self.callbackFasta)
		casmenu.impmenu.add_command(label='2. SAM files', command=self.callbackBAM)
		casmenu.impmenu.add_command(label='3. Demographic data', command=self.callbackDemo)
		casmenu.expmenu.add_command(label='Populations', command=self.pickPops)
		casmenu.expmenu.add_command(label='Individuals', command=self.pickInds)
		casmenu.add_cascade(label='Import',menu=casmenu.impmenu)
		casmenu.add_cascade(label='Export',menu=casmenu.expmenu)
		casmenu.add_separator()
		casmenu.add_command(label='Display the data', command=self.createSummaryWindow)
		casmenu.add_separator()
		casmenu.add_command(label='Clear Database', command=self.clearMDB)
		casmenu.add_command(label='Goodbye', command=sys.exit)
		self.menubar.add_cascade(label="File", menu=casmenu)
		helpmenu = Menu(self.menubar)
		helpmenu.add_command(label='lociNGS buttons', command=self.buttons)
		helpmenu.add_command(label='README', command=self.openREADME)
		self.menubar.add_cascade(label="Help", menu = helpmenu)

	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		intro = "Please enter the data in the order listed in the Import Menu.\nOnce data has been loaded via the Import Menu, press 'Display the data'."
		self.createWidgets(intro, "BLACK")
		self.master.title("Welcome to lociNGS")
	
if __name__ == '__main__': 
	MainScreen().mainloop()