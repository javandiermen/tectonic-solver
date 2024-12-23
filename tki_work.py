import tkinter as tk
from tkinter import simpledialog
import csv


class MatrixApp:
    def __init__(self, root, matrix, layout):
        self.root = root
        self.root.title("Dynamic Matrix")

        self.matrix = matrix
        self.layout = layout
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.selected_row = 0
        self.selected_col = 0

        self.create_widgets()
        self.update_selection()

    def create_widgets(self):
        self.cells = []
        for i in range(self.rows):
            row_cells = []
            for j in range(self.cols):
                cell_frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
                cell_frame.grid(row=i, column=j, sticky="nsew")  # Use grid without padding and sticky to fill the cell
                cell = tk.Label(cell_frame, text=self.matrix[i][j] if self.matrix[i][j] != 0 else "", width=10,
                                height=5, borderwidth=1, relief="solid")
                cell.pack(fill='both', expand=True)
                if self.matrix[i][j] == 0:
                    small_numbers = tk.Label(cell, text="1 2 3 4 5", font=("Arial", 8), anchor='nw')
                    small_numbers.place(relx=0.02, rely=0.02)
                row_cells.append((cell_frame, cell))
            self.cells.append(row_cells)

        for i in range(self.rows):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(self.cols):
            self.root.grid_columnconfigure(j, weight=1)

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Return>", self.enter_value)

    def update_selection(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell_frame, cell = self.cells[r][c]
                cell.config(borderwidth=1, relief="solid")  # Reset all cells to default border
                if c<=self.cols-2 and self.layout[r][c] != self.layout[r][c+1]:
                    print(f"right: {r},{c} :{self.layout[r][c]}-{self.layout[r][c+1]}")
                    right_border = tk.Frame(cell_frame, bg="black", width=6)
                    right_border.place(relx=1.0, rely=0.0, relheight=1.0, anchor='ne')
                if r<=self.rows-2 and self.layout[r][c] != self.layout[r+1][c]:
                    print(f"bottom: {r},{c} : {self.layout[r][c]}-{self.layout[r+1][c]}")
                    bottom_border = tk.Frame(cell_frame, bg="black", height=6)
                    bottom_border.place(relx=0.0, rely=1.0, relwidth=1.0, anchor='sw')
                if r == self.selected_row and c == self.selected_col:
                    cell.config(bg="yellow")
                else:
                    cell.config(bg="white")
                if self.matrix[r][c] == 0:
                    small_numbers = tk.Label(cell, text="1 2 3 4 5", font=("Arial", 8), anchor='nw')
                    small_numbers.place(relx=0.02, rely=0.02)

    def move_left(self, event):
        if self.selected_col > 0:
            self.selected_col -= 1
            self.update_selection()

    def move_right(self, event):
        if self.selected_col < self.cols - 1:
            self.selected_col += 1
            self.update_selection()

    def move_up(self, event):
        if self.selected_row > 0:
            self.selected_row -= 1
            self.update_selection()

    def move_down(self, event):
        if self.selected_row < self.rows - 1:
            self.selected_row += 1
            self.update_selection()

    def enter_value(self, event):
        value = simpledialog.askinteger("Input", "Enter value:")
        if value is not None:
            self.matrix[self.selected_row][self.selected_col] = value
            cell_frame, cell = self.cells[self.selected_row][self.selected_col]
            cell.config(text=value if value != 0 else "")
            for widget in cell.winfo_children():
                widget.destroy()
            if value == 0:
                small_numbers = tk.Label(cell, text="1 2 3 4 5", font=("Arial", 8), anchor='nw')
                small_numbers.place(relx=0.02, rely=0.02)


def read_matrix_from_csv(file_path):
    matrix = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            matrix.append([int(cell) if cell else 0 for cell in row])
            # matrix.append([int(cell) for cell in row])
    return matrix


if __name__ == "__main__":
    file_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t1.board.csv'
    matrix = read_matrix_from_csv(file_path)
    layout_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t1.layout.csv'
    layout = read_matrix_from_csv(layout_path)
    root = tk.Tk()
    app = MatrixApp(root, matrix, layout)
    root.mainloop()

    # matrix.append([int(cell) if cell else 0 for cell in row])
    # file_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t1.board.csv'  # Update this path to your CSV file
