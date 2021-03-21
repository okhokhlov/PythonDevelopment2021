import tkinter as tk
from tkinter.messagebox import showinfo
import re


class Application(tk.Frame):
	def __init__(self, title):
		super().__init__(None)
		self.grid(sticky="NEWS")
		self.master.title(title)
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.createWidgets()


	def createWidgets(self):
		pass


	def __getattr__(self, name):

		def constructor(widget_class, geometry, **kwargs):
			row_pattern = r"(?P<row>\d+)(\.(?P<row_weight>\d+))?(\+(?P<height>\d+))?:"
			col_pattern = r"(?P<col>\d+)(\.(?P<col_weight>\d+))?(\+(?P<width>\d+))?"
			gravity_pattern = r"(/(?P<gravity>[NSEWnsew]+))?"
			pattern = row_pattern + col_pattern + gravity_pattern
			match_res = re.fullmatch(pattern, geometry).groupdict()

			row = int(match_res["row"])
			col = int(match_res["col"])
			row_weight = int(match_res["row_weight"]) if match_res["row_weight"] is not None else 1
			col_weight = int(match_res["col_weight"]) if match_res["col_weight"] is not None else 1
			height = int(match_res["height"]) if match_res["height"] is not None else 0 
			width = int(match_res["width"]) if match_res["width"] is not None else 0
			gravity = match_res["gravity"] if match_res["gravity"] is not None else "NEWS"

			class ChildWidet(widget_class):
				pass

			ChildWidet.__getattr__ = Application.__getattr__

			widget = ChildWidet(self, **kwargs)

			widget.master.rowconfigure(row, weight=row_weight)
			widget.master.columnconfigure(col, weight=col_weight)
			widget.grid(row=row,
						column=col,
						rowspan=height+1,
						columnspan=width+1,
						sticky=gravity
						)
			
			setattr(self, name, widget)

		return constructor


class App(Application):
	def createWidgets(self):
		self.message = "Congratulations!\nYou've found a sercet level!"
		self.F1(tk.LabelFrame, "1:0", text="Frame 1")
		self.F1.B1(tk.Button, "0:0/NW", text="1")
		self.F1.B2(tk.Button, "0:1/NE", text="2")
		self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
		self.F2(tk.LabelFrame, "1:1", text="Frame 2")
		self.F2.B1(tk.Button, "0:0/N", text="4")
		self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
		self.F2.B3(tk.Button, "1:0/S", text="6")
		self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
		self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()

