import csv


class Cell:
    def __init__(self, row, col, value, block):
        self.row = row
        self.col = col
        self.value = value
        self.block = block

    def __repr__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block})"

    def __str__(self):
        return f"Cell(row={self.row}, col={self.col}, value={self.value}, block={self.block})"


class Tectonic:
    def __init__(self):
        self.board = []
        self.layout = []
        self.cells = []
        self.blocks = []

    def read_from_csv(self, board_file, layout_file):
        self.board = self._read_csv(board_file)
        self.layout = self._read_csv(layout_file)
        self.matrix_to_cells()

    def _read_csv(self, file_path):
        matrix = []
        with open(file_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                matrix.append([int(cell) if cell else 0 for cell in row])
        return matrix

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
                cell = Cell(row_idx, col_idx, value, block_num)
                self.cells.append(cell)
                self.blocks[block_num].append(cell)

    def place_cell(self, row, col, value):
        if self.board[row][col] != 0:
            print(f"This is weird: board already containing value:self.board[row][col]")
        else:
            self.board[row][col] = value


if __name__ == '__main__':
    t = Tectonic()
    t.read_from_csv("tst/t1.board.csv", "tst/t1.layout.csv")
    print(t)
    t.place_cell(0, 1, 1)
    print(t)
