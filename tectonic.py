import csv

class Tectonic:
    def __init__(self):
        self.board = []
        self.layout = []

    def read_from_csv(self, board_file, layout_file):
        self.board = self._read_csv(board_file)
        self.layout = self._read_csv(layout_file)

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
        return f"Board:\n{board_str}\n\nLayout:\n{layout_str}"


if __name__ == '__main__':
    t = Tectonic()
    t.read_from_csv("tst/t1.board.csv", "tst/t1.layout.csv")
    print(t)