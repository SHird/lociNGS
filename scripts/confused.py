#!/usr/bin/python
#Shird for lociNGS
#trying to figure out how to correctly pass variables and return values from within a class to other parts of program



from Tkinter import *

populations = ['POP1', 'POP2', 'POP3', 'POP4']
programs = ['Nexus', 'IMa2', 'Migrate']




class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
           # print var.get(), self.vars 
    def state(self):
    	for var in self.vars: print var.get()
    		#print map(lambda var: var.get(), self.vars)


def POPMENU():  #THIS FUNCTION DOES NOT WORK WHEN CALLED FROM THE MENU - RETURNS ALL 0'S EVEN WHEN BOXES ARE CHECKED. IT DOES WORK WHEN CALLED ON ITS OWN. ?????	
		#if __name__ == '__main__':  #i don't need this because it won't be run as standalone ?
	poproot = Tk()
	lng = Checkbar(poproot, populations)
	tgl = Checkbar(poproot, programs)
	lng.pack()
	tgl.pack(side=LEFT)
	checkbars = [lng, tgl]
	print checkbars[0].vars[0].get()
	
	def allstates(): 
		results = []
		for each in checkbars:
			for eachNow in each.vars:	
				results.append(eachNow.get())
			print "these are results", results
	
	lng.config(relief=GROOVE, bd=2)
	Button(poproot, text='Peek', command=allstates).pack(side=RIGHT)
	poproot.mainloop()

#running these three lines causes allstates to print all zeroes even when boxes are checked
widget = Button(None, text='1. Loci/fasta file(s)', command=POPMENU)
widget.pack()
widget.mainloop()

#running POPMENU() on its own causes allstates to print correctly (1 if box checked, 0 otherwise)	
POPMENU()