#!/usr/bin/python

from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory
from constructionMDB import fromLociFiles
from constructionMDB import fromBAMFolder
from constructionMDB import fromDemographicData
from Tix import ScrolledWindow

indList=[]

def callbackBAM():
    BAMfolder = askdirectory() 
    fromBAMFolder(BAMfolder)
    
def callbackFasta():
	FastaFolder = askdirectory() 
	fromLociFiles(FastaFolder)	
	
def callbackDemo():
	Demofile = askopenfilename() 
	indList = fromDemographicData(Demofile)
	return indList

def donothing():
	root = Tk()
	root.title("now what")
	button = Button(root, text="Do nothing button")
	button.pack()

class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
    	self.pack()
    	self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)   
    def state(self):
    	for var in self.vars:
    		return map(lambda var: var.get(), self.vars)

#GET THESE PIECES FROM MONGODB
#populations = ['POP1', 'POP2', 'POP3', 'POP4','POP5','POP6']
#programs = ['Nexus', 'IMa2', 'Migrate']
#individuals = []

def POPMENU(list):
	poproot = Toplevel()
	Label(poproot,text = "Select all that apply:").pack(side=LEFT)
	popmen = Checkbar(poproot, list)
	popmen.pack(side=LEFT)
	def allstates(): 
		print "these are results", popmen.state()
		#add popmen.state to array?
	popmen.config(relief=GROOVE, bd=2)
	Button(poproot, text='Peek', command=allstates).pack(side=RIGHT)

class LocusWindow(Frame):
	def __init__(self, parent=None, string="", side=LEFT, anchor=W):
		from pymongo import Connection
		Frame.__init__(self, parent)
		
		#scrollbar = Scrollbar(self.master)
		#scrollbar.pack(side=RIGHT, fill=Y)
		#frame.grid_rowconfigure(0, weight=1)
		#frame.grid_columnconfigure(0, weight=1)


		#self.pack()
		
		self.master.title( "Loci Data" )
		self.master.rowconfigure( 0, weight = 1 )
		self.master.columnconfigure( 0, weight = 1 )
		self.grid( sticky = W+E+N+S )
		
		self.label1=Label(self, text = "Locus Name")
		self.label1.grid(row = 0, column = 0)
		self.label2=Label(self, text="Length")
		self.label2.grid(row=0, column=1)
		self.label3=Label(self, text="Coverage_This_Ind")
		self.label3.grid(row=0, column=2)
		self.label4=Label(self, text="Number_Inds")
		self.label4.grid(row=0, column=3)
		connection = Connection()
		db = connection.test_database
		loci = db.loci
		demographic = db.demographic
		locList = []
		print "1", string
		cursorLoc = loci.find( {"indInFasta": string})
		for y in cursorLoc:
			locList.append(y["locusFasta"])
		print "2", locList
		for locus in range(10):
			self.label9 = Label(self, text = locList[locus]).grid(row=1+locus, column = 0)
			cursor = loci.find( {"locusFasta" : locList[locus] })
			for x in cursor:
				self.label6=Label(self, text = x["length"] ).grid(row=1+locus,column = 1)
				self.label7=Label(self, text=str(len(x["indInFasta"]))).grid(row=1+locus, column=3)
				self.rowconfigure(1+locus, weight=1)		
				fake = {}
				fake = x["individuals"]
				self.button1=Button(self, text = fake[string]  ).grid(row=1+locus, column = 2)


		self.rowconfigure(0, weight = 1 )
		self.columnconfigure(0, weight = 1 )
		self.columnconfigure(1, weight = 1 )
		self.columnconfigure(2, weight = 1 )
		self.columnconfigure(3, weight = 1 )
		self.columnconfigure(4, weight = 1 )
				


def getLocusInfoForGUI(string):
	print string
	root = Tk()
	#Label(root).pack(side=LEFT)
	locScreen = LocusWindow(root, string)
	swin=tixScrolledWindow(locScreen, width=500, height=500)
	swin.pack()
	locScreen.pack(side=TOP, fill=BOTH, expand=YES)	



		
class GridDemo(Frame):
	def __init__( self ):
		from pymongo import Connection
		Frame.__init__( self )			
		
		def getDemoDataForGUI():
			#to get the MongoDB data
			callbackDemo()
			connection = Connection()
			db = connection.test_database
			loci = db.loci
			demographic = db.demographic
			indList = []
			cursorInd = demographic.find( {}, {'Individual':1, '_id':0})
			for y in cursorInd:
				indList.append(y["Individual"])
			for ind in range(len(indList)):
				self.label9 = Label(self, text = indList[ind]).grid(row=1+ind, column = 0)
				cursor = demographic.find( {"Individual" : indList[ind] })
				for x in cursor:
					X = indList[ind]
					self.label6=Label(self, text = x["Population"] ).grid(row=1+ind,column = 1)
					self.label7=Label(self, text = x["Species"] ).grid(row=1+ind, column = 2)
					self.label8=Label(self, text=x["Location"] ).grid(row=1+ind, column=3)
					self.button1=Button(self, text=x["numLoci"], command=lambda X = X: getLocusInfoForGUI(X)).grid(row=1+ind, column=4)
					self.rowconfigure(1+ind, weight=1)		
			self.rowconfigure(0, weight = 1 )
			self.columnconfigure(0, weight = 1 )
			self.columnconfigure(1, weight = 1 )
			self.columnconfigure(2, weight = 1 )
			self.columnconfigure(3, weight = 1 )
			self.columnconfigure(4, weight = 1 )
	
		#this creates the menu	
		top = self.winfo_toplevel()
		self.menubar = Menu(top)
		top["menu"] = self.menubar
		self.casmenu = Menu(self.menubar)
		self.casmenu.impmenu = Menu(self.casmenu)
		self.casmenu.expmenu = Menu(self.casmenu)		
		
		self.casmenu.impmenu.add_command(label='1. Loci/fasta file(s)', command=callbackFasta)
		self.casmenu.impmenu.add_command(label='2. SAM files', command=callbackBAM)
		self.casmenu.impmenu.add_command(label='3. Demographic data', command=getDemoDataForGUI)
		self.casmenu.expmenu.add_command(label='Populations', command=lambda: POPMENU(programs))
		self.casmenu.expmenu.add_command(label='Individuals', command=lambda: POPMENU(callbackDemo()))
		self.casmenu.add_cascade(label='Import',menu=self.casmenu.impmenu)
		self.casmenu.add_cascade(label='Export',menu=self.casmenu.expmenu)
		self.menubar.add_cascade(label="File", menu=self.casmenu)

			
		#for the actual GUI screen
		self.master.title( "Grid Demo" )
		self.master.rowconfigure( 0, weight = 1 )
		self.master.columnconfigure( 0, weight = 1 )
		self.grid( sticky = W+E+N+S )

		self.label1=Label(self, text = "Individual")
		self.label1.grid(row = 0, column = 0)
		
		self.label2=Label(self, text="Population")
		self.label2.grid(row=0, column=1)
		
		self.label3=Label(self, text="Species")
		self.label3.grid(row=0, column=2)
		
		self.label4=Label(self, text="Location")
		self.label4.grid(row=0, column=3)
		
		self.label5=Label(self, text="# of Loci")
		self.label5.grid(row=0, column=4)
		


def main():
	GridDemo().mainloop()
if __name__ == '__main__':
    main()
