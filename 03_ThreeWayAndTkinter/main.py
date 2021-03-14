import random
import tkinter as tk
from tkinter import messagebox as mb

class Game(tk.Frame):
	def __init__(self, master=None, board_h=4, board_w=4):
		tk.Frame.__init__(self, master)
		self.grid(sticky='NSEW')

		self.board_h = board_h
		self.board_w = board_w
		self.win_state = False

		top=self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)

		for i in range(self.board_w):
			self.columnconfigure(i, weight=1)
		for i in range(self.board_h + 1):
			self.rowconfigure(i, weight=1)

		self.numbers = [[None for j in range(self.board_w)] for i in range(self.board_h)]
		self.free_pos = [self.board_h - 1, self.board_w - 1]

		for i in range(self.board_h):
			for j in range(self.board_w):
				if not (i == (self.board_h - 1) and j == (self.board_w - 1)):
					self.numbers[i][j] = tk.Button(self, text=f'{i*self.board_w + j + 1}', command=self.button_command(i, j))
					self.numbers[i][j].grid(row=i, column=j, sticky='NSEW')

		self.quit_button = tk.Button(self, text='Quit', command=self.quit)
		self.quit_button.grid(row=self.board_h, column=0, sticky='NSEW')

		self.new_game_button = tk.Button(self, text='Ne', command=self.new_game)
		self.new_game_button.grid(row=self.board_h, column=self.board_w - 1, sticky='NSEW')

		self.new_game()


	def button_command(self, i, j):
		def f():
			if not self.win_state:
				cur_pos = [self.numbers[i][j].grid_info()["row"], self.numbers[i][j].grid_info()["column"]]
				if (cur_pos[0] - self.free_pos[0]) ** 2 + (cur_pos[1] - self.free_pos[1]) ** 2 == 1:
					self.numbers[i][j].grid(row=self.free_pos[0], column=self.free_pos[1], sticky='NSEW')
					self.free_pos = cur_pos

				self.win_state = True
				for row in range(self.board_h):
					for col in range(self.board_w):
						if self.numbers[row][col] is not None:
							cur_pos = [self.numbers[row][col].grid_info()["row"], self.numbers[row][col].grid_info()["column"]]
							self.win_state = self.win_state and ([row,col] == cur_pos)

				if self.win_state:
					mb.showinfo("", "You win!!!")
					self.new_game()

		return f


	def new_game(self):
		self.win_state = False

		board = [[i * self.board_h + j + 1 for j in range(self.board_w)] for i in range(self.board_h)]
		free_pos = [self.board_h - 1, self.board_w - 1]

		for i in range(10):
			possible_moves = []
			for i in [(0,1), (1,0), (0,-1), (-1,0)]:
				if (self.board_h > i[0] + free_pos[0] >= 0) and (self.board_w > i[1] + free_pos[1] >= 0):
					possible_moves.append([i[0] + free_pos[0], i[1] + free_pos[1]])

			move = random.choice(possible_moves)
			board[free_pos[0]][free_pos[1]], board[move[0]][move[1]] = board[move[0]][move[1]], board[free_pos[0]][free_pos[1]]
			free_pos = move


		for i in range(self.board_h):
			for j in range(self.board_w):
				if board[i][j] != self.board_h * self.board_w:
					y, x = (board[i][j] - 1) // self.board_h, (board[i][j] - 1) % self.board_w
					self.numbers[y][x].grid(row=i, column=j, sticky='NSEW')


		self.free_pos = free_pos


def main():
	app = Game()
	app.master.title('Sample application')
	app.mainloop()
	pass


if __name__ == "__main__":
	main()