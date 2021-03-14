import time
import tkinter as tk


class Game(tk.Frame):
	def __init__(self, master=None, board_h=4, board_w=4):
		tk.Frame.__init__(self, master)
		self.grid()

		self.board_h = board_h
		self.board_w = board_w

		self.numbers = [[None for j in range(self.board_w)] for i in range(self.board_h)]
		self.free_pos = [self.board_h - 1, self.board_w - 1]

		for i in range(self.board_h):
			for j in range(self.board_w):
				if not (i == (self.board_h - 1) and j == (self.board_w - 1)):
					self.numbers[i][j] = tk.Button(self, text=f'{i*self.board_w + j}', command=self.button_command(i, j))
					self.numbers[i][j].grid(row=i, column=j)

		self.quit_button = tk.Button(self, text='Quit', command=self.quit)
		self.quit_button.grid(row=self.board_h, column=0)


	def button_command(self, i, j):
		def f():
			cur_pos = [self.numbers[i][j].grid_info()["row"], self.numbers[i][j].grid_info()["column"]]
			if (cur_pos[0] - self.free_pos[0]) ** 2 + (cur_pos[1] - self.free_pos[1]) ** 2 == 1:
				self.numbers[i][j].grid(row=self.free_pos[0], column=self.free_pos[1])
				self.free_pos = cur_pos
		return f


def main():
	app = Game()
	app.master.title('Sample application')
	app.mainloop()
	pass


if __name__ == "__main__":
	main()