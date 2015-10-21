# GUI for finding shortest path between 2 Wikipedia articles
from tkinter import *
from PIL import Image, ImageTk
import webbrowser
import SearcherAlgorithm

class Application(Frame):
	# A GUI application used to find the shortest path between two Wikipedia articles

	def __init__(self, master):
		# Initialize the Frame """
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		# Generate instructions, entry boxes and submit buttons. Define actions for events.

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
		# Takes value from text fields and uses the wiki algorithm
		self.text.delete(0.0, END)
		# Uses x and y to start algorithm
		x = self.start.get()
		y = self.end.get()
		#print(SearcherAlgorithm.main(x, y))
		list1 = SearcherAlgorithm.main(x, y)
		print(list1)
		self.text.insert(END, list1);

# Creates about page
def about():
	newWin = Toplevel(root, height = 50, width = 50)
	newWin.resizable(height = False, width = False)
	newWin.title('About')

	about = Label(newWin, text="This project was created from October 2nd - October 4th at UCSD's first Hackathon, SD Hacks\n" +
							   "in the year 2015. The authors of this project are Nicholas-Lama Solet, Jacob Sean Davis and Anthony Lu.")
	about.grid()

# Creates window
root = Tk()

# Menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
# filemenu.add_command(label="New")
# filemenu.add_command(label="Open")
# filemenu.add_command(label="Save")
# filemenu.add_command(label="Save as...")
# filemenu.add_command(label="Close")

# filemenu.add_separator()

filemenu.add_command(label="Exit", command = root.quit)
menubar.add_cascade(label="File", menu = filemenu)
# editmenu = Menu(menubar, tearoff=0)
# editmenu.add_command(label="Undo")

# editmenu.add_separator()

# editmenu.add_command(label="Cut")
# editmenu.add_command(label="Copy")
# editmenu.add_command(label="Paste")
# editmenu.add_command(label="Delete")
# editmenu.add_command(label="Select All")

# menubar.add_cascade(label="Edit", menu = editmenu)
helpmenu = Menu(menubar, tearoff = 0)
# helpmenu.add_command(label="Help Index")
helpmenu.add_command(label="About...", command = about)
# helpmenu.add_command(label="Donate")
menubar.add_cascade(label="Help", menu = helpmenu)

root.config(menu=menubar)

# Modifies window
root.title("Wikipedia Game")
root.geometry("305x230")

app = Application(root)

# Starts event loop
root.mainloop()
