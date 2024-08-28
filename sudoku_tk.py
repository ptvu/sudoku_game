import random
import tkinter as tk
from tkinter import messagebox

class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.selected_cell = None
        
        self.create_board()
        self.generate_board()
        self.fixed_cell = [[self.board[i][j] != 0 for j in range(9)] for i in range(9)]
        self.create_buttons()

    def create_board(self):
        for i in range(9):
            for j in range(9):
                cell = tk.Label(self.master, width=2, height=1, font=('Verdana', 20), relief='ridge', bg='white')
                cell.grid(
                    row=i,
                    column=j,
                    padx=(6 if (j > 0 and j % 3 == 0) else 1, 0),
                    pady=(6 if (i > 0 and i % 3 == 0) else 1, 0),
                    sticky='nsew'
                )
                cell.bind('<Button-1>', lambda e, row=i, col=j: self.cell_clicked(row, col))
                self.cells[i][j] = cell

        # Add thick borders
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(self.master, borderwidth=2, relief='raised')
                frame.grid(row=i*3, column=j*3, rowspan=3, columnspan=3, padx=3, pady=3)

        # Create number buttons
        for num in range(1, 10):
            button = tk.Button(self.master, text=str(num), width=2, height=1, 
                               command=lambda n=num: self.number_button_clicked(n))
            button.grid(row=9, column=num-1, padx=1, pady=5)

    def generate_board(self):
        base = 3
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return random.sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        self.board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = squares * 3 // 4
        for p in random.sample(range(squares), empties):
            self.board[p // side][p % side] = 0

        self.update_ui()

    def update_ui(self):
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                value = self.board[i][j]
                if value != 0:
                    cell.config(text=str(value), bg='lightgray')
                else:
                    cell.config(text='', bg='white')

    def cell_clicked(self, row, col):
        if not self.fixed_cell[row][col]:
            if self.selected_cell:
                self.cells[self.selected_cell[0]][self.selected_cell[1]].config(bg='white')
            self.selected_cell = (row, col)
            self.cells[row][col].config(bg='lightblue')

    def number_button_clicked(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            self.board[row][col] = number
            self.cells[row][col].config(text=str(number), bg='#FFC0CB')  # Light baby blue color
            if self.check_win():
                messagebox.showinfo("Congratulations!", "You've solved the Sudoku!")
            self.selected_cell = None

    def check_win(self):
        for row in self.board:
            if 0 in row or len(set(row)) != 9:
                return False
        for col in zip(*self.board):
            if 0 in col or len(set(col)) != 9:
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square = [self.board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if 0 in square or len(set(square)) != 9:
                    return False
        return True

    def create_buttons(self):
        new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        new_game_button.grid(row=10, column=0, columnspan=9, pady=10)

    def new_game(self):
        self.generate_board()
        self.selected_cell = None

if __name__ == '__main__':
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
