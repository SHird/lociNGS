#!/usr/bin/python

from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory
from constructionMDB import fromLociFiles
from constructionMDB import fromBAMFolder
from constructionMDB import fromDemographicData
from constructionMDB import getAllInds
from constructionMDB import getPopDict
from Tix import ScrolledWindow
from convertingLociNGS import *
from pymongo import Connection

#MongoDB connection
connection = Connection()
db = connection.test_database
loci = db.loci
demographic = db.demographic
indList=[]

def callbackBAM():
    BAMfolder = askdirectory() 
    fromBAMFolder(BAMfolder)
    
def callbackFasta():
	FastaFolder = askdirectory() 
	fromLociFiles(FastaFolder)	
	
def callbackDemo():
	Demofile = askopenfilename() 
	fromDemographicData(Demofile)

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
		
def POPMENUprograms(list):
	programs = ['Nexus', 'IMa2', 'Migrate']
	poproot = Toplevel()
	Label(poproot,text = "Select all that apply:").pack(side=LEFT)
	popmen = Checkbar(poproot, programs)
	popmen.pack(side=LEFT)
	def allstates(): 
		print "these are results", popmen.state()
		if popmen.state()[0] == 1:
			toNexus(list)
		if popmen.state()[1] == 1:
			toIMa2(list)
		if popmen.state()[2] ==1:
			toMigrate(toIMa2(list))
		poproot.destroy()
		#add popmen.state to array?
	popmen.config(relief=GROOVE, bd=2)
	Button(poproot, text='Save', command=allstates).pack(side=RIGHT)
	
def pickInds():
	allInds = getAllInds()
	indroot = Toplevel()
	Label(indroot,text = "Select all that apply:").pack(side=LEFT)
	indmen = Checkbar(indroot, allInds)
	indmen.pack(side=LEFT)
	def allstates(): 
		indsToUse = []
		print "these are results", indmen.state()
	#	POPMENUprograms()
		for each in range(len(indmen.state())):
			if indmen.state()[each] == 1:
				indsToUse.append(allInds[each])
		cursor = db.loci.find( {"indInFasta": {'$all' : indsToUse} }, {"path" : 1, "_id":0})
		indPathList = []
		for m in cursor:
			indPathList.append(m["path"])
		POPMENUprograms(indPathList)
		indroot.destroy()
	indmen.config(relief=GROOVE, bd=2)
	Button(indroot, text='Save', command=allstates).pack(side=RIGHT)

def pickPops():
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
		POPMENUprograms(popPathList)
		popsroot.destroy()
		#add popmen.state to array?
	popsmen.config(relief=GROOVE, bd=2)
	Button(popsroot, text='Save', command=allstates).pack(side=RIGHT)


class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
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

def createLocusWindow(string):
	root = Tk()
	vscrollbar = AutoScrollbar(root)
	vscrollbar.grid(row=0, column=1, sticky=N+S)
	hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
	hscrollbar.grid(row=1, column=0, sticky=E+W)
	canvas = Canvas(root,
	                yscrollcommand=vscrollbar.set,
	                xscrollcommand=hscrollbar.set)
	canvas.grid(row=0, column=0, sticky=N+S+E+W)
	vscrollbar.config(command=canvas.yview)
	hscrollbar.config(command=canvas.xview)
	# make the canvas expandable
	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)
	# create canvas contents
	frame = Frame(canvas)
	frame.rowconfigure(1, weight=1)
	frame.columnconfigure(1, weight=1)
	
	label1=Label(frame, text = "Locus Name")
	label1.grid(row = 0, column = 0)
	label2=Label(frame, text="Length")
	label2.grid(row=0, column=1)
	label3=Label(frame, text="Coverage_This_Ind")
	label3.grid(row=0, column=2)
	label4=Label(frame, text="Number_Inds")
	label4.grid(row=0, column=3)
	from pymongo import Connection
#	string = "J01"
	connection = Connection()
	db = connection.test_database
	loci = db.loci
	demographic = db.demographic
	locList = []
#	print "1", string
	cursorLoc = loci.find( {"indInFasta": string})
	for y in cursorLoc:
		locList.append(y["locusFasta"])
#	print "2", locList
	for locus in range(len(locList)):
		label9 = Label(frame, text = locList[locus]).grid(row=1+locus, column = 0)
		cursor = loci.find( {"locusFasta" : locList[locus] })
		for x in cursor:
			label6=Label(frame, text = x["length"] ).grid(row=1+locus,column = 1)
			label7=Label(frame, text=str(len(x["indInFasta"]))).grid(row=1+locus, column=3)
			#rowconfigure(1+locus, weight=1)		
			fake = {}
			fake = x["individuals"]
			button1=Button(frame, text = fake[string]).grid(row=1+locus, column = 2)
	canvas.create_window(0, 0, anchor=NW, window=frame)
	frame.update_idletasks()
	canvas.config(scrollregion=canvas.bbox("all"))
	root.title(string)
	root.mainloop()

def createSummaryWindow():
	indList = getAllInds()
	root = Toplevel()
	vscrollbar = AutoScrollbar(root)
	vscrollbar.grid(row=0, column=1, sticky=N+S)
	hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
	hscrollbar.grid(row=1, column=0, sticky=E+W)
	canvas = Canvas(root,yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set)
	canvas.grid(row=0, column=0, sticky=N+S+E+W)
	vscrollbar.config(command=canvas.yview)
	hscrollbar.config(command=canvas.xview)
	# make the canvas expandable
	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)
	# create canvas contents
	frame = Frame(canvas)
	frame.label1=Label(frame, text = "Individual")
	frame.label1.grid(row = 0, column = 0)
	frame.label2=Label(frame, text="Population")
	frame.label2.grid(row=0, column=1)
	frame.label3=Label(frame, text="Species")
	frame.label3.grid(row=0, column=2)
	frame.label4=Label(frame, text="Location")
	frame.label4.grid(row=0, column=3)
	frame.label5=Label(frame, text="# of Loci")
	frame.label5.grid(row=0, column=4)
	
	from pymongo import Connection
	connection = Connection()
	db = connection.test_database
	loci = db.loci
	demographic = db.demographic
	indList = []
	cursorInd = demographic.find( {}, {'Individual':1, '_id':0})
	for y in cursorInd:
		indList.append(y["Individual"])
		for ind in range(len(indList)):
			label9 = Label(frame, text = indList[ind]).grid(row=1+ind, column = 0)
			cursor = demographic.find( {"Individual" : indList[ind] })
			for x in cursor:
				X = indList[ind]
				label6=Label(frame, text = x["Population"] ).grid(row=1+ind,column = 1)
				label7=Label(frame, text = x["Species"] ).grid(row=1+ind, column = 2)
				label8=Label(frame, text=x["Location"] ).grid(row=1+ind, column=3)
				button1=Button(frame, text=x["numLoci"], command=lambda X = X: createLocusWindow(X)).grid(row=1+ind, column=4)
	frame.rowconfigure(1, weight=1)
	frame.columnconfigure(1, weight=1)
	canvas.create_window(0, 0, anchor=NW, window=frame)
	frame.update_idletasks()
	canvas.config(scrollregion=canvas.bbox("all"))
	root.title("lociNGS")
	root.mainloop()
		
class GridDemo(Frame):
	def __init__( self ):
		from pymongo import Connection
		Frame.__init__( self )			
		#this creates the menu	
		top = self.winfo_toplevel()
		self.menubar = Menu(top)
		top["menu"] = self.menubar
		self.casmenu = Menu(self.menubar)
		self.casmenu.impmenu = Menu(self.casmenu)
		self.casmenu.expmenu = Menu(self.casmenu)		
		
		self.casmenu.impmenu.add_command(label='1. Loci/fasta file(s)', command=callbackFasta)
		self.casmenu.impmenu.add_command(label='2. SAM files', command=callbackBAM)
		self.casmenu.impmenu.add_command(label='3. Demographic data', command=callbackDemo)
		self.casmenu.expmenu.add_command(label='Populations', command=pickPops)
		self.casmenu.expmenu.add_command(label='Individuals', command=pickInds)
		self.casmenu.add_cascade(label='Import',menu=self.casmenu.impmenu)
		self.casmenu.add_cascade(label='Export',menu=self.casmenu.expmenu)
		self.casmenu.add_command(label='Display the data', command=createSummaryWindow)
		self.casmenu.add_command(label='Goodbye', command=sys.exit)
		self.menubar.add_cascade(label="File", menu=self.casmenu)
#		self.master.withdraw()
		
		#createSummaryWindow()	
		
		#for the actual GUI screen
		self.master.title( "Welcome to lociNGS" )
		self.master.rowconfigure( 0, weight = 1 )
		self.master.columnconfigure( 0, weight = 1 )
		self.grid( sticky = W+E+N+S )

		self.label1=Label(self, text = "Please enter the data in the order listed in the Input Menu.\nOnce data has been loaded via the Input Menu, press 'Display the data'.")
		self.label1.grid(row = 0, column = 0)	
		
def main():
	GridDemo().mainloop()
if __name__ == '__main__':
    main()