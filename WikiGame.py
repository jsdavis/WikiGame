# GUI for finding shortest path between 2 Wikipedia articles
from tkinter import *
from PIL import Image, ImageTk
import wikipedia
import webbrowser

class Application(Frame):
	""" A GUI application used to find the shortest path between two Wikipedia articles"""

	def __init__(self, master):
		""" Initialize the Frame """
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		""" Generate instructions, entry boxes and submit buttons. Define actions for events. """

		# Description of program
		self.desc = Label(self, text = "Determine the shortest path between two articles!")
		self.desc.grid(row = 0, column = 0, columnspan = 4, sticky = W, padx = 10, pady = 5)

		# Instructions for inoutting starting article
		self.instructionA = Label(self, text = "Name of starting article")
		self.instructionA.grid(row = 1, column = 0, columnspan = 2, sticky = W, padx = 10, pady = 5)

		# Entry widget for starting article
		self.start = Entry(self)
		self.start.grid(row = 1, column = 3, sticky = W, padx = 10, pady = 5)

		# Instructions for inputting target article
		self.instructionB = Label(self, text = "Name of target article")
		self.instructionB.grid(row = 2, column = 0, columnspan = 2, sticky = W, padx = 10, pady = 5)

		# Entry widget for target article
		self.end = Entry(self)
		self.end.grid(row = 2, column = 3, sticky = W, padx = 10, pady = 5)

		# Search button to compare the two articles
		self.searchB = Button(self, text = "Search")
		# When button is pressed do the search
		self.searchB["command"] = self.search
		self.searchB.grid(row = 3, column = 0, columnspan = 1, sticky = W, padx = 10, pady = 5)

		# Screen to show results
		self.text = Text(self, width = 35, height = 5, wrap = WORD)
		self.text.grid(row = 4, column = 0, columnspan = 4, sticky = W, padx = 10, pady = 5)

	def search(self):
		""" Takes value from text fields and uses the wiki algorithm"""
		self.text.delete(0.0, END)
		# Assigns start to random if empty
		x = self.start.get()
		y = self.end.get()

		if x == '':
			while True:
				try:
					x = wikipedia.random(1)
					self.text.insert(0.0, 'Random start is %s.\n' % x)
					break
				except UnicodeEncodeError:
					pass
		# Assigns end to random if empty
		if y == '':
			while True:
				try:
					y = wikipedia.random(1)
					self.text.insert(0.0, 'Random end is %s.\n' % y)
					break
				except UnicodeEncodeError:
					pass
		self.text.insert(0.0, 'Start is %s.\nTarget is %s.\n' % (x,y))
		#wikiMethod(self.start.get(), self.end.get())

# Creates about page
def about():
	newWin = Toplevel(root, height = 50, width = 50)
	newWin.title('About')
	about = Label(newWin, text="This project was created from October 2nd - October 4th at UCSD's first Hackathon, SD Hacks\n" +
							   "in the year 2015. The authors of this project are Nicholas-Lama Solet, Jacob Sean Davis and Anthony Lu.")
	about.grid()

# Donate command
def donate():
	webbrowser.open('http://bit.ly/1K19Ee4', new=0, autoraise=True)

# Creates window
root = Tk()

# Menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="New", command = donate)
filemenu.add_command(label="Open", command = donate)
filemenu.add_command(label="Save", command = donate)
filemenu.add_command(label="Save as...", command = donate)
filemenu.add_command(label="Close", command = donate)

filemenu.add_separator()

filemenu.add_command(label="Exit", command = root.quit)
menubar.add_cascade(label="File", menu = filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command = donate)

editmenu.add_separator()

editmenu.add_command(label="Cut", command = donate)
editmenu.add_command(label="Copy", command = donate)
editmenu.add_command(label="Paste", command = donate)
editmenu.add_command(label="Delete", command = donate)
editmenu.add_command(label="Select All", command = donate)

menubar.add_cascade(label="Edit", menu = editmenu)
helpmenu = Menu(menubar, tearoff = 0)
helpmenu.add_command(label="Help Index", command = donate)
helpmenu.add_command(label="About...", command = about)
helpmenu.add_command(label="Donate", command = donate)
menubar.add_cascade(label="Help", menu = helpmenu)

root.config(menu=menubar)

# Modifies window
root.title("Wikipedia Game")
root.geometry("305x230")

app = Application(root)

# Starts event loop
root.mainloop()