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
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block}, neighbours={len(self.neighbours)}, possibilities={self.possibilities})"

    def __str__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block}, neighbours={len(self.neighbours)}, possibilities={self.possibilities})"


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
        for cell in self.cells:
            self.set_cell_neighbours(cell)
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

    def find_cell(self,row,col):
        i=row*len(self.board[0])+col
        # self.cells[i] should be the one..
        if (self.cells[i].row != row or self.cells[i].col !=col):
            print("strange: should be same row/col")
        return self.cells[i]

    def place(self, row, col, value):
        cell=self.find_cell(row,col)
        self.place_cell(cell,value)

    def place_cell(self, cell, value):
        if self.board[cell.row][cell.col] != 0:
            print(f"This is weird: board already containing value:self.board[row][col]")
            exit(1)
        else:
            self.board[cell.row][cell.col] = value
            cell.value=value
            self.update_block_and_neighbours_possibilities(cell)


    def show_tectonic(self):
        # Create a plot
        fig,ax = plt.subplots()

        # Hide the axes
        ax.axis('off')

        # Set the limits and aspect ratio
        ax.set_xlim(-0.5, len(self.board[0])+0.5)
        ax.set_ylim( len(self.board) +0.5 , -0.5)
        ax.set_aspect('equal')

        xlen=len(self.board[0])+1
        ylen=len(self.board) + 1

        # Display the matrix values in the cells
        for row_idx, row in enumerate(self.board):
            for col_idx, value in enumerate(row):
                cell=self.cells[row_idx*len(self.board[0])+col_idx]
                if self.board[row_idx][col_idx]>0:
                    ax.text(col_idx+0.5, row_idx+0.5, self.board[row_idx][col_idx], ha='center', va='center', fontsize=20)
                else:
                    ax.text(col_idx+0.5, row_idx +0.5 - 0.4, cell.possibilities, ha='center', va='top', fontsize=8)
                # Draw vertical gridline (thick border)
                ax.axvline(col_idx, ymin=(0.5 / ylen), ymax=((ylen - 0.5) / ylen), color='black', linewidth= 1 if col_idx != 0 else 4)
            #draw horizontal gridline (thick border)
            ax.axhline(row_idx, xmin=(0.5 / xlen), xmax=((xlen - 0.5) / xlen), color='black', linewidth=1 if row_idx != 0 else 4)
        ax.axvline(len(self.board[0]), ymin=(0.5 / ylen), ymax=((ylen - 0.5) / ylen), color='black', linewidth=4)
        ax.axhline(len(self.board) , xmin=(0.5 / xlen), xmax=((xlen - 0.5) / xlen), color='black', linewidth=4)



        #draw the tectonic borders vertical
        for row_idx in range (0,len(self.board)):
            for col_idx in range(1, len (self.board[0])):
                if self.layout[row_idx][col_idx-1] != self.layout[row_idx][col_idx]:
                #     print(f"debug: {row_idx},{col_idx}: ymin={(ylen-(0.5+row_idx))}, ymax={(ylen-(0.5+row_idx+1))}")
                    ax.axvline(col_idx, ymin=( (ylen-(0.5+row_idx)) / ylen), ymax=( (ylen-(0.5+row_idx+1)) / ylen), color='black',
                               linewidth=4)

        #draw the tectonic borders horizontal
        for row_idx in range (1,len(self.board)):
            for col_idx in range(0, len (self.board[0])):
                if self.layout[row_idx-1][col_idx] != self.layout[row_idx][col_idx]:
                    # print(f"debug: {row_idx},{col_idx}: xmin={(0.5+col_idx)}, ymax={(0.5+col_idx+1)}")
                    ax.axhline(row_idx, xmin=( (0.5+col_idx) / xlen), xmax=( (0.5+col_idx+1) / xlen), color='black',
                               linewidth=4)


        # Show the plot
        width=9
        height=9
        fig.set_figwidth(width)
        fig.set_figheight(height)
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
                print(f"checking: [{cell.row},{cell.col}]-[{other_cell.row},{other_cell.col}]")
                if abs(other_cell.row-cell.row) <= 1 and abs(other_cell.col-cell.col) <= 1:
                    print(f"adding: [{other_cell.row},{other_cell.col}]")
                    cell.neighbours.add(other_cell)

    def update_block_and_neighbours_possibilities(self,cell):
        # print(f"update_block_and_neighbours_possible : cell:{cell} ")
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

    def remove_cell_domain_x(self,cell, arvalue):
        for i in arvalue:
            cell.possibilities.discard(i)

    def remove_domain_x(self,row,col, arvalue):
        cell=self.find_cell(row,col)
        for i in arvalue:
            cell.possibilities.discard(i)

    def remove_cell_domain(self,cell, value):
        cell.possibilities.discard(value)

    def remove_domain(self,row,col, value):
        cell=self.find_cell(row,col)
        cell.possibilities.discard(value)


if __name__ == '__main__':
    t = Tectonic()
    t.read_from_csv("tst/t1.board.csv", "tst/t1.layout.csv")
    # print(t)
    t.place(0, 1, 1)   #naked single
    cell=t.find_cell(4,2)
    t.remove_cell_domain_x(cell,[1,2,4])   #neighbor trio
    t.place_cell(cell,5) #naked single
    t.remove_domain(3,0,1)    #neighbor hidden singles 1
    t.remove_domain(3,1,1)
    t.remove_domain_x(4,1,[2,4])   #neighbor duo
    t.place(4,1,1)
    t.place(3,3,1) #hidden single
    t.remove_domain_x(2,1,[4,5])   #neighbor duo
    t.remove_domain_x(2,1,[2,4])   #neighbor duo
    t.place(2, 1, 1) #naked single
    t.remove_domain_x(1,3,[4,5])   #neighbor duo
    t.place(1, 3, 1) #naked single
    t.remove_domain_x(0,3,[4,5])   #block duo
    t.place(0, 3, 3) #naked single
    t.remove_domain_x(2,0,[2,4])   #block duo
    t.place(2,0, 5) #naked single
    t.place(1,1, 4) #naked single
    t.place(1,0, 2) #naked single
    t.place(1,2, 5) #naked single
    t.place(2,3, 4) #naked single
    t.place(3,2, 2) #naked single
    t.place(3,1, 4) #naked single
    t.place(4,3, 4) #naked single
    t.place(3,0, 2) #naked single
    t.show_tectonic()
