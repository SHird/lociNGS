#!/usr/bin/python

from Tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory
from constructionMDB import fromLociFiles
from constructionMDB import fromBAMFolder
from constructionMDB import fromDemographicData

def callbackBAM():
    BAMfolder = askdirectory() 
    fromBAMFolder(BAMfolder)
    
def callbackFasta():
	FastaFolder = askdirectory() 
	fromLociFiles(FastaFolder)	
	
def callbackDemo():
    Demofile = askopenfilename() 
    fromDemographicData(Demofile)

def donothing():
	root = Tk()
	root.title("now what")
	button = Button(root, text="Do nothing button")
	button.pack()


populations = ['POP1', 'POP2', 'POP3', 'POP4']
programs = ['Nexus', 'IMa2', 'Migrate']
def POPMENU():  #THIS FUNCTION DOES NOT WORK WHEN CALLED FROM THE MENU - RETURNS ALL 0'S EVEN WHEN BOXES ARE CHECKED. IT DOES WORK WHEN CALLED ON ITS OWN. ?????	
	class Checkbar(Frame):
	    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
	        Frame.__init__(self, parent)
	        self.vars = []
	        for pick in picks:
	            var = IntVar()
	            chk = Checkbutton(self, text=pick, variable=var)
	            chk.pack(side=side, anchor=anchor, expand=YES)
	            self.vars.append(var)
	            print var.get(), self.vars 
	    def state(self):
	    	for var in self.vars: print var.get()
	    		#print map(lambda var: var.get(), self.vars)
	
	#if __name__ == '__main__':  #i don't need this because it won't be run as standalone ?
	poproot = Tk()
	lng = Checkbar(poproot, populations)
	tgl = Checkbar(poproot, programs)
	lng.pack()
	tgl.pack(side=LEFT)
	checkbars = [lng, tgl]
	
	def allstates(): 
		for each in checkbars:
			print "this is each.state", each.state()
	
	lng.config(relief=GROOVE, bd=2)
	Button(poproot, text='Peek', command=allstates).pack(side=RIGHT)
	poproot.mainloop()

class TestMenu:
	def __init__(self, master):
	
		self.master = master
		self.menubar = Menu(self.master)
		self.casmenu = Menu(self.menubar)
		self.casmenu.impmenu = Menu(self.casmenu)
		self.casmenu.expmenu = Menu(self.casmenu)
		
		self.casmenu.impmenu.add_command(label='1. Loci/fasta file(s)', command=callbackFasta)
		self.casmenu.impmenu.add_command(label='2. SAM files', command=callbackBAM)
		self.casmenu.impmenu.add_command(label='3. Demographic data', command=callbackDemo)

		self.casmenu.expmenu.add_command(label='Populations', command=POPMENU)
		self.casmenu.expmenu.add_command(label='Individuals', command=donothing)

		self.casmenu.add_cascade(label='Import',menu=self.casmenu.impmenu)
		self.casmenu.add_cascade(label='Export',menu=self.casmenu.expmenu)
 		
		self.menubar.add_cascade(label="File", menu=self.casmenu)
		self.top = Toplevel(menu=self.menubar, width=500, relief=RAISED,borderwidth=2)

def main():
    root = Tk()
    root.withdraw()
    root.title("lociNGS")
    app = TestMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()





#main()

#		self.casmenu.expmenu.choices = Menu(self.casmenu)
#		self.casmenu.expmenu.add_cascade(label='Populations', menu=self.casmenu.expmenu.choices)
 #		self.casmenu.expmenu.add_cascade(label='Individuals', menu=self.casmenu.expmenu.choices)
 
	
#if __name__ == '__main__':
   # main()

	#	self.nexus = BooleanVar()
	#	self.ima2 = BooleanVar()
	#	self.migrate = BooleanVar()
	#	self.casmenu.expmenu.choices.add_checkbutton(label = "NEXUS", onvalue = True, offvalue = False, variable = self.nexus)        
	#	self.casmenu.expmenu.choices.add_checkbutton(label = "IMa2", onvalue = True, offvalue = False, variable = self.ima2)        
	#	self.casmenu.expmenu.choices.add_checkbutton(label = "MIGRATE", onvalue = True, offvalue = False, variable = self.migrate)        

#	self.unused = Menu(self.menubar)

#errmsg = 'Error!'
#Button(text='Quit', command=callback).pack(fill=X)
#Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
#mainloop()
   
#root = Tk()
#menubar = Menu(root)
#filemenu = Menu(menubar, tearoff=0)
##filemenu.add_command(label="Import", command=donothing)
#filemenu.add_command(label="Export Individuals", command=donothing)
#filemenu.add_command(label="Export Populations", command=donothing)
##filemenu.add_command(label="Save as...", command=donothing)
##filemenu.add_command(label="Close", command=donothing)#

#filemenu.add_separator()

#filemenu.add_command(label="Exit", command=root.quit)
#menubar.add_cascade(label="File", menu=filemenu)

#importmenu = Menu(menubar, tearoff=0)
#importmenu.add_command(label="SAM file", command=donothing)
#importmenu.add_separator()
#importmenu.add_command(label="Loci/fasta file(s)", command=donothing)
#importmenu.add_command(label="demographic data", command=donothing)
#editmenu.add_command(label="Paste", command=donothing)
#editmenu.add_command(label="Delete", command=donothing)
#editmenu.add_command(label="Select All", command=donothing)

#menubar.add_cascade(label="Import", menu=importmenu)
#helpmenu = Menu(menubar, tearoff=0)
#helpmenu.add_command(label="Help Index", command=donothing)
#helpmenu.add_command(label="About...", command=donothing)
#menubar.add_cascade(label="Help", menu=helpmenu)

#root.config(menu=menubar)
#root.mainloop()
