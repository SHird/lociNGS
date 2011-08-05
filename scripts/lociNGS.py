#!/usr/bin/env python

from Tkinter import *
import tkMessageBox
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory
from lociNGS.constructionMDB import fromLociFiles
from lociNGS.constructionMDB import fromBAMFolder
from lociNGS.constructionMDB import fromDemographicData
from lociNGS.constructionMDB import getAllInds
from lociNGS.constructionMDB import getPopDict
from lociNGS.constructionMDB import getDemoColumnsFromMDB
from lociNGS.convertingLociNGS import getRawFastaFromBAM
from Tix import ScrolledWindow
from lociNGS.convertingLociNGS import *
from pymongo import Connection

#MongoDB connection
connection = Connection()
db = connection.test_database
loci = db.loci
demographic = db.demographic
indList=[]

#	return "ok"
	#B1 = Tkinter.Button(top, text = "Say Hello", command = hello)
	#B1.pack()
	
def popup(string):
	master = Toplevel()
	master.withdraw()
	textMessage = "Successful Import of:\n\n"+string
	tkMessageBox.showinfo("Success", textMessage)
	mainloop()


def callbackBAM():
	BAMfolder = askdirectory() 
	fromBAMFolder(BAMfolder)
	popup(BAMfolder)
    
def callbackFasta():
	FastaFolder = askdirectory() 
	fromLociFiles(FastaFolder)	
	popup(FastaFolder)
	
def callbackDemo():
	Demofile = askopenfilename() 
	fromDemographicData(Demofile)
	#tkMessageBox.showinfo("Successful Import", "hooray")	
	popup(Demofile)
	
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
	h = root.winfo_screenheight()
	canvas = Canvas(root,yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set, width = 600, height = h)
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
	label1=Label(frame, text = "Locus Name").grid(row = 0, column = 0, padx = 6)
	label2=Label(frame, text="Length").grid(row=0, column=1, padx = 6)
	label3=Label(frame, text="Coverage_This_Ind").grid(row=0, column=2, padx = 6)
	label4=Label(frame, text="Number_Inds").grid(row=0, column=3, padx = 6)
	label5=Label(frame, text="Coverage_Total").grid(row=0, column=4, padx = 6)
	from pymongo import Connection
	connection = Connection()
	db = connection.test_database
	loci = db.loci
	demographic = db.demographic
	locList = []
	cursorLoc = loci.find( {"indInFasta": string})
	for y in cursorLoc:
		locList.append(y["locusFasta"])
	for locus in locList:
		label9 = Label(frame, text = locus).grid(row=1+locList.index(locus), column = 0, padx = 6)
		cursor = loci.find( {"locusFasta" : locus })
		for x in cursor:
			X = x["locusFasta"]
			locusTotal = 0
			label6=Label(frame, text = x["length"] ).grid(row=1+locList.index(locus),column = 1, padx = 6)
			label7=Label(frame, text=str(len(x["indInFasta"]))).grid(row=1+locList.index(locus), column=3, padx = 6)
			fake = {}
			fake = x["individuals"]
			print "this fake now:", fake
			for each in fake:
				locusTotal = locusTotal + fake[each]
				print "currentLocustotal:", locusTotal
				Y = fake[string]
				print "this is Y:", Y 	
			print "X is", X, "string is:", string, "final locus total:", locusTotal	
			button1=Button(frame, text = fake[string], command = lambda X=X: getRawFastaFromBAM(string,X)).grid(row=1+locList.index(locus), column = 2, padx = 6)
			button2 = Button(frame, text = locusTotal, command = lambda X = X: getAllRawFastaFromBAM(X)).grid(row=1+locList.index(locus), column = 4, padx = 6)					
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
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	canvas = Canvas(root,yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set, width = 800, height = h)
	canvas.grid(row=0, column=0, sticky=N+S+E+W)
	vscrollbar.config(command=canvas.yview)
	hscrollbar.config(command=canvas.xview)
	# make the canvas expandable
	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)
	# create canvas contents
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
	from pymongo import Connection
	connection = Connection()
	db = connection.test_database
	loci = db.loci
	demographic = db.demographic
	indList = getAllInds()
	for ind in indList:
		label9 = Label(frame, text = ind).grid(row=1+indList.index(ind), column = 0, padx = 6)
		cursor = demographic.find( {"Individual" : ind })
		for x in cursor:
			X = ind
			for i in listOfColumns:
				if listOfColumns.index(i) != 2:
					label=Label(frame, text = x[i] ).grid(row=1+indList.index(ind),column = listOfColumns.index(i), padx = 6)
			button=Button(frame, text=x["numLoci"], command=lambda X = X: createLocusWindow(X)).grid(row=1+indList.index(ind), column=2, padx = 6)
	frame.rowconfigure(1, weight=1)
	frame.columnconfigure(1, weight=1)
	canvas.create_window(0, 0,anchor=NW, window=frame)
	frame.update_idletasks()
	canvas.config(scrollregion=canvas.bbox("all"))
	root.title("lociNGS")
	root.mainloop()

def clearMDB():
	from pymongo import Connection
	connection = Connection()
	db = connection.test_database
	loci = db.loci
	demographic = db.demographic
	db.demographic.remove()
	db.loci.remove()

#def labelUpdate(string):
#	v.set("Please enter the data in the order listed in the Import Menu.\nOnce data has been loaded via the Import Menu, press 'Display the data'.")
#	root.update_idletasks()		

class GridDemo(Frame):
	def __init__(self, master=None):
		from pymongo import Connection
		Frame.__init__( self, master )			
		#this creates the menu	
		top = self.winfo_toplevel()
		self.menubar = Menu(top)
		top["menu"] = self.menubar
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
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
		self.casmenu.add_command(label='Clear Database', command=clearMDB)
		self.casmenu.add_command(label='Goodbye', command=sys.exit)
		self.menubar.add_cascade(label="File", menu=self.casmenu)
		#for the actual GUI screen
		self.master.title( "Welcome to lociNGS" )
		self.master.rowconfigure( 0, weight = 1 )
		self.master.columnconfigure( 0, weight = 1 )
		self.grid( sticky = W+E+N+S )
		v = StringVar()
		v.set("Please enter the data in the order listed in the Import Menu.\nOnce data has been loaded via the Import Menu, press 'Display the data'.")
		self.label1=Label(self, textvariable = v)
		self.label1.grid(row = 0, column = 0, padx = 6)	
		
		
		

def main():
	root=Tk()
	GD = GridDemo()
	GD.mainloop()
	#GridDemo().mainloop()
if __name__ == '__main__':
	main()