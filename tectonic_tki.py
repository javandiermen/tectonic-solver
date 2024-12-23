import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import csv


class Cell:
    def __init__(self, row, col, value, block, neighbours, possibilities):
        self.row = row
        self.col = col
        self.value = value
        self.block = block
        self.neighbours = neighbours
        self.possibilities = possibilities

    def __repr__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block}, neighbours={len(self.neighbours)}, possibilities={self.possibilities})"

    def __str__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block}, neighbours={len(self.neighbours)}, possibilities={self.possibilities})"

    def show_pos(self):
        return str(self.possibilities)+"    "

def _read_csv(file_path):
    matrix = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            matrix.append([int(cell) if cell else 0 for cell in row])
    return matrix


class TectonicApp:
    def __init__(self, root, matrix, layout):
        self.root = root
        self.root.title("Tectonic Player")

        self.matrix = matrix
        self.layout = layout
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.cells = []
        self.blocks = []
        self.selected_row = 0
        self.selected_col = 0

        self.matrix_to_cells()
        self.set_cell_possibilities()
        for cell in self.cells:
            self.set_cell_neighbours(cell)
        for cell in self.cells:
            self.update_block_and_neighbours_possibilities(cell)

        self.create_widgets()
        self.update_selection()


    def __str__(self):
        matrix_str = '\n'.join([' '.join(map(str, row)) for row in self.matrix])
        layout_str = '\n'.join([' '.join(map(str, row)) for row in self.layout])
        cells_str = '\n'.join(str(cell) for cell in self.cells)
        blocks_str = '\n'.join(
            f"Block {block_num}:\n" + '\n'.join(f"  {cell}" for cell in block)
            for block_num, block in enumerate(self.blocks)
        )
        return f"Board:\n{matrix_str}\n\nLayout:\n{layout_str}\n\n{cells_str}\n\n{blocks_str}"

    def matrix_to_cells(self):
        max_block_num = max(max(row) for row in self.layout)  # determines the amount of blocks defined in layout
        self.blocks = [[] for _ in range(max_block_num + 1)]  # creates "empty" blocks
        self.cells = []
        for row_idx, row in enumerate(self.matrix):
            for col_idx, value in enumerate(row):
                block_num = self.layout[row_idx][col_idx]
                cell = Cell(row_idx, col_idx, value, block_num, neighbours=set(), possibilities=set())
                self.cells.append(cell)
                self.blocks[block_num].append(cell)

    def find_cell(self, row, col):
        i = row * self.cols + col
        # self.cells[i] should be the one..
        if (self.cells[i].row != row or self.cells[i].col != col):
            print("strange: should be same row/col")
        return self.cells[i]

    def place(self, row, col, value):
        cell = self.find_cell(row, col)
        self.place_cell(cell, value)

    def place_cell(self, cell, value):
        if self.matrix[cell.row][cell.col] != 0:
            print(f"This is weird: board already containing value:self.board[row][col]")
            exit(1)
        else:
            self.matrix[cell.row][cell.col] = value
            cell.value = value
            self.update_block_and_neighbours_possibilities(cell)

    def set_cell_possibilities(self):
        for cell in self.cells:
            if cell.value == 0:
                block_num = cell.block
                possibilities = cell.possibilities
                block = self.blocks[block_num]
                for i in range(1, len(block) + 1):
                    possibilities.add(i)

    def set_cell_neighbours(self, cell):
        for other_cell in self.cells:
            if other_cell != cell:
                # print(f"checking: [{cell.row},{cell.col}]-[{other_cell.row},{other_cell.col}]")
                if abs(other_cell.row - cell.row) <= 1 and abs(other_cell.col - cell.col) <= 1:
                    # print(f"adding: [{other_cell.row},{other_cell.col}]")
                    cell.neighbours.add(other_cell)

    def update_block_and_neighbours_possibilities(self, cell):
        # print(f"update_block_and_neighbours_possible : cell:{cell} ")
        if cell.value != 0:
            block = self.blocks[cell.block]
            for block_mate in block:
                # print("block_mate:",block_mate)
                if block_mate != cell:
                    block_mate.possibilities.discard(cell.value)
                    # print("updated block_mate:", block_mate)
            for neighbour in cell.neighbours:
                # print("neighbour:",neighbour)
                neighbour.possibilities.discard(cell.value)
                # print("updated neighbour:", neighbour)

    def remove_cell_domain_x(self, cell, arvalue):
        for i in arvalue:
            cell.possibilities.discard(i)

    def remove_domain_x(self, row, col, arvalue):
        cell = self.find_cell(row, col)
        for i in arvalue:
            cell.possibilities.discard(i)

    def remove_cell_domain(self, cell, value):
        cell.possibilities.discard(value)

    def remove_domain(self, row, col, value):
        cell = self.find_cell(row, col)
        cell.possibilities.discard(value)

    def board_filled(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.matrix[r][c]==0:
                    return False
        return True


    def create_widgets(self):
        self.wcells = []
        for i in range(self.rows):
            row_cells = []
            for j in range(self.cols):
                cell_frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
                cell_frame.grid(row=i, column=j, sticky="nsew")  # Use grid without padding and sticky to fill the cell
                wcell = tk.Label(cell_frame, text=self.matrix[i][j] if self.matrix[i][j] != 0 else "", width=8,
                                height=4, borderwidth=0.5, relief="solid")
                wcell.pack(fill='both', expand=True)
                wcell.config(font=("Helvetica", 12, "bold"))
                if self.matrix[i][j] == 0:
                    small_numbers = tk.Label(wcell, text= self.find_cell(i,j).show_pos(), font=("Arial", 8), anchor='nw')
                    small_numbers.place(relx=0.02, rely=0.02)
                row_cells.append((cell_frame, wcell))
            self.wcells.append(row_cells)

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
                cell_frame, wcell = self.wcells[r][c]
                wcell.config(borderwidth=0, relief="solid")  # Reset all cells to default border
                if c<=self.cols-2 and self.layout[r][c] != self.layout[r][c+1]:
                    # print(f"right: {r},{c} :{self.layout[r][c]}-{self.layout[r][c+1]}")
                    right_border = tk.Frame(cell_frame, bg="black", width=6)
                    right_border.place(relx=1.0, rely=0.0, relheight=1.0, anchor='ne')
                if r<=self.rows-2 and self.layout[r][c] != self.layout[r+1][c]:
                    # print(f"bottom: {r},{c} : {self.layout[r][c]}-{self.layout[r+1][c]}")
                    bottom_border = tk.Frame(cell_frame, bg="black", height=6)
                    bottom_border.place(relx=0.0, rely=1.0, relwidth=1.0, anchor='sw')
                if r == self.selected_row and c == self.selected_col:
                    wcell.config(bg="yellow")
                else:
                    wcell.config(bg="white")
                if self.matrix[r][c] == 0:
                    small_numbers = tk.Label(wcell, text=self.find_cell(r,c).show_pos(), font=("Arial", 8), anchor='nw')
                    small_numbers.config(bg=wcell.cget("bg"))
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
        if value in self.find_cell(self.selected_row,self.selected_col).possibilities:
            # self.matrix[self.selected_row][self.selected_col] = value
            self.place(self.selected_row,self.selected_col, value)
            cell_frame, wcell = self.wcells[self.selected_row][self.selected_col]
            wcell.config(text=value if value != 0 else "")
            for widget in wcell.winfo_children():
                widget.destroy()
            if value == 0:
                small_numbers = tk.Label(wcell, text=self.find_cell(self.selected_row,self.selected_col).show_pos(), font=("Arial", 8), anchor='nw')
                small_numbers.place(relx=0.02, rely=0.02)
            self.update_selection()
            if self.board_filled():
                messagebox.showinfo(title="Gefeliciteerd!", message="KLAAR! Geweldig Gespeeld")
        else:
            messagebox.showinfo(title="OOPS!", message="Nee, die waarde kan niet daar... (oen)")



def read_matrix_from_csv(file_path):
    matrix = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            matrix.append([int(cell) if cell else 0 for cell in row])
            # matrix.append([int(cell) for cell in row])
    return matrix


if __name__ == "__main__":

    pathlocation="/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/"
    tectonic_list = [
        ["5x5 - level 5", "t2.board.csv", "t2.layout.csv"],
        ["5x5 - level 6", "t1.board.csv","t1.layout.csv"],
        ["9x5 - level 5", "t3.board.9x5.csv", "t3.layout.9x5.csv"],
        ["9x11- level 5", "t4.board.9x11.csv", "t4.layout.9x11.csv"],
        ["9x5 - level 7 moeilijk (100)", "t5.board.9x5.csv", "t5.layout.9x5.csv"]

    ]


    print("Tectonic-Player")
    print("Which Tectonic you want to play:")
    for i,val in enumerate(tectonic_list):
        print (f"{i}: {val[0]}")

    index=int(input("your choice:"))

    # file_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t4.board.9x11.csv'
    # layout_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t4.layout.9x11.csv'
    file_path = pathlocation+tectonic_list[index][1]
    layout_path = pathlocation+tectonic_list[index][2]

    print (f"{file_path},{layout_path}")
    matrix = read_matrix_from_csv(file_path)
    layout = read_matrix_from_csv(layout_path)
    root = tk.Tk()
    app = TectonicApp(root, matrix, layout)
    root.mainloop()

    # matrix.append([int(cell) if cell else 0 for cell in row])
    # file_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t1.board.csv'  # Update this path to your CSV file
