# GUI for finding shortest path between 2 wiki pages
from tkinter import *
from PIL import Image, ImageTk
import wikipedia
import webbrowser

class Application(Frame):
	""" A GUI application used to find the path between two wiki articles"""

	def __init__(self, master):
		""" Initialize the Frame """
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		""" Generate instructions, entry boxes and submit buttons """

		# Description of program
		self.desc = Label(self, text = "Determine the shortest path between two articles!")
		self.desc.grid(row = 0, column = 0, columnspan = 4, sticky = W, padx = 10, pady = 5)

		# Instructions for starting article
		self.instructionA = Label(self, text = "Name of starting article")
		self.instructionA.grid(row = 1, column = 0, columnspan = 2, sticky = W, padx = 10, pady = 5)

		# Entry widget for starting article
		self.start = Entry(self)
		self.start.grid(row = 1, column = 3, sticky = W, padx = 10, pady = 5)

		# Instructions for target article
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

		# Randomize button
		self.randB = Button(self, text = "Randomize")
		# When button is pressed randomize text fields
		self.randB["command"] =  self.randomize
		self.randB.grid(row = 3, column = 3, columnspan = 2, sticky = W, padx = 10, pady = 5)

		# Screen to show results
		self.text = Text(self, width = 35, height = 5, wrap = WORD)
		self.text.grid(row = 4, column = 0, columnspan = 4, sticky = W, padx = 10, pady = 5)

	def search(self):
		""" Takes value from text fields and uses the wiki algorithm"""
		self.text.delete(0.0, END)
		if self.start.get() != '' and self.end.get() != '':
			self.text.insert(0.0, 'Start is %s. Target is %s' % (self.start.get(), self.end.get()) )
			#wikiMethod(self.start.get(), self.end.get())
		else:
			self.text.insert(0.0, 'A field is blank.')

	def randomize(self):
		""" Randomize the articles """
		# Configure text to be wikipedia.random()
		randA = None
		randB = None
		while True:
			try:
				randA = wikipedia.random(1)
				randB = wikipedia.random(1)
				self.text.delete(0.0, END)
				self.text.insert(0.0, 'Start is %s. Target is %s' % (randA, randB) )
				break
			except UnicodeEncodeError:
				pass
		# wikiMethod(randA, randB)

# Placeholder
def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()		

# Creates about page
def about():
	newWin = Toplevel(root, height = 50, width = 50)
	newWin.title('About')
	about = Label(newWin, text="This project was created from October 2nd - October 4th at UCSD's first Hackathon, SD Hacks\n" +
							   "The authors of this project are Nicholas-Lama Solet, Jacob Sean Davis and Anthony Lu")
	about.grid()

# Donate command
def donate():
	# Takes you to my PayPal
	webbrowser.open('http://bit.ly/1K19Ee4', new=0, autoraise=True)


# Creates window
root = Tk()

# Modifies window
root.title("Wikipedia Game")
root.geometry("305x230")

app = Application(root)

# Starts event loop
root.mainloop()