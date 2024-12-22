import csv
import matplotlib.pyplot as plt


class Cell:
    def __init__(self, row, col, value, block, neighbours, possibilities):
        self.row = row
        self.col = col
        self.value = value
        self.block = block
        self.neighbours = neighbours
        self.possibilities = possibilities

    def __repr__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block}, neighbours={self.neighbours}, possibilities={self.possibilities})"

    def __str__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block}, neighbours={self.neighbours}, possibilities={self.possibilities})"


def _read_csv(file_path):
    matrix = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            matrix.append([int(cell) if cell else 0 for cell in row])
    return matrix


class Tectonic:
    def __init__(self):
        self.board = []
        self.layout = []
        self.cells = []
        self.blocks = []

    def read_from_csv(self, board_file, layout_file):
        self.board = _read_csv(board_file)
        self.layout = _read_csv(layout_file)
        self.matrix_to_cells()
        self.set_cell_possibilities()
        #for cell in self.cells:
            #self.set_cell_neighbours(cell)
        for cell in self.cells:
            self.update_block_and_neighbours_possibilities(cell)

    def __str__(self):
        board_str = '\n'.join([' '.join(map(str, row)) for row in self.board])
        layout_str = '\n'.join([' '.join(map(str, row)) for row in self.layout])
        cells_str = '\n'.join(str(cell) for cell in self.cells)
        blocks_str = '\n'.join(
            f"Block {block_num}:\n" + '\n'.join(f"  {cell}" for cell in block)
            for block_num, block in enumerate(self.blocks)
        )
        return f"Board:\n{board_str}\n\nLayout:\n{layout_str}\n\n{cells_str}\n\n{blocks_str}"

    def matrix_to_cells(self):
        max_block_num = max(max(row) for row in self.layout)  # determines the amount of blocks defined in layout
        self.blocks = [[] for _ in range(max_block_num + 1)]  # creates "empty" blocks
        self.cells = []
        for row_idx, row in enumerate(self.board):
            for col_idx, value in enumerate(row):
                block_num = self.layout[row_idx][col_idx]
                cell = Cell(row_idx, col_idx, value, block_num, neighbours=set(), possibilities=set())
                self.cells.append(cell)
                self.blocks[block_num].append(cell)

    def place_cell(self, row, col, value):
        if self.board[row][col] != 0:
            print(f"This is weird: board already containing value:self.board[row][col]")
        else:
            self.board[row][col] = value

    def show_tectonic(self):
        # Create a plot
        fig, ax = plt.subplots()

        # Hide the axes
        ax.axis('off')

        # Set the limits and aspect ratio
        ax.set_xlim(-0.5, len(self.board[0])-0.5)
        ax.set_ylim( len(self.board) -0.5 , -0.5)
        ax.set_aspect('equal')

        # Display the matrix values in the cells
        for row_idx, row in enumerate(self.board):
            for col_idx, value in enumerate(row):
                if self.board[row_idx][col_idx]>0:
                    ax.text(col_idx, row_idx, self.board[row_idx][col_idx], ha='center', va='center', fontsize=20)
                ax.text(col_idx, row_idx - 0.4, '1 2 3 4 5', ha='center', va='top', fontsize=8)

        # Draw gridlines
        for row_idx, row in enumerate(self.board):
            for col_idx, value in enumerate(row):
                ax.axhline(col_idx - 0.5, xmin=0, xmax= len(self.board)-1, color='black', linewidth=1)
                ax.axvline(row_idx - 0.5, ymin=0, ymax= len(self.board[0]), color='black', linewidth=1)

        #draw the tectonic borders
        # for row_idx, row in enumerate(self.board):
        #     for col_idx, value in enumerate(row):
        #         if col_idx==0 or col_idx==len(self.board[0]-1) or ((col_idx>0) and not (self.layout[row_idx][col_idx] == self.layout[row_idx][col_idx-1])):
        #             print (f"dik : {row_idx},{ col_idx}")

        # Show the plot
        plt.show()

    def set_cell_possibilities(self):
        for cell in self.cells:
            if cell.value == 0:
                block_num = cell.block
                possibilities = cell.possibilities
                block = self.blocks[block_num]
                for i in range(1,len(block)+1):
                    possibilities.add(i)

    def set_cell_neighbours(self,cell):
        for other_cell in self.cells:
            if other_cell != cell:
                if abs(other_cell.row-cell.row) <= 1 and abs(other_cell.col-cell.col) <= 1:
                    cell.neighbours.add(other_cell)

    def update_block_and_neighbours_possibilities(self,cell):
        #print("cell:",cell)
        if cell.value != 0:
            block = self.blocks[cell.block]
            for block_mate in block:
                #print("block_mate:",block_mate)
                if block_mate != cell:
                    block_mate.possibilities.discard(cell.value)
                    #print("updated block_mate:", block_mate)
            for neighbour in cell.neighbours:
                #print("neighbour:",neighbour)
                neighbour.possibilities.discard(cell.value)
                #print("updated neighbour:", neighbour)

if __name__ == '__main__':
    t = Tectonic()
    t.read_from_csv("tst/t1.board.csv", "tst/t1.layout.csv")
    print(t)
    t.place_cell(0, 1, 1)
    print(t)
    t.show_tectonic()
