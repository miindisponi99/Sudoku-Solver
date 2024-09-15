import tkinter as tk

from tkinter import messagebox


def solve_sudoku(board, rows, cols, boxes, empty_cells, index=0):
    if index == len(empty_cells):
        return True
    row, col = empty_cells[index]
    box_index = (row // 3) * 3 + (col // 3)
    for num in range(1, 10):
        if num not in rows[row] and num not in cols[col] and num not in boxes[box_index]:
            board[row][col] = num
            rows[row].add(num)
            cols[col].add(num)
            boxes[box_index].add(num)
            if solve_sudoku(board, rows, cols, boxes, empty_cells, index + 1):
                return True
            board[row][col] = 0
            rows[row].remove(num)
            cols[col].remove(num)
            boxes[box_index].remove(num)
    return False


def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_buttons()
    
    def create_grid(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry
    
    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=3, columnspan=3, pady=10)
        clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        clear_button.grid(row=10, column=3, columnspan=3, pady=10)
    
    def solve(self):
        try:
            self.board = [[int(self.entries[row][col].get()) if self.entries[row][col].get() else 0
                           for col in range(9)] for row in range(9)]
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter numbers between 1-9 or leave empty.")
            return
        
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empty_cells = []
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                if num == 0:
                    empty_cells.append((row, col))
                else:
                    rows[row].add(num)
                    cols[col].add(num)
                    box_index = (row // 3) * 3 + (col // 3)
                    boxes[box_index].add(num)
        if solve_sudoku(self.board, rows, cols, boxes, empty_cells):
            self.update_entries()
        else:
            messagebox.showerror("No Solution", "This Sudoku puzzle cannot be solved.")
    
    def update_entries(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(self.board[row][col]))
    
    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()