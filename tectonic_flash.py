from flask import Flask, render_template, request
import random
import csv

app = Flask(__name__)

# Pre-defined puzzles (for simplicity, using small examples)
# tectonic_list = [
#     ["5x5 - level 5", "t2.board.csv", "t2.layout.csv"],
#     ["5x5 - level 6", "t1.board.csv", "t1.layout.csv"],
#     ["9x5 - level 5", "t3.board.9x5.csv", "t3.layout.9x5.csv"],
#     ["9x11- level 5", "t4.board.9x11.csv", "t4.layout.9x11.csv"],
#     ["9x5 - level 7 moeilijk (100)", "t5.board.9x5.csv", "t5.layout.9x5.csv"]
# ]

puzzles = {
    1: ('tst/t1.board.csv', 'tst/t2.layout.csv'),
    2: ('tst/t2.board.csv', 'tst/t2.layout.csv'),
    # Add more puzzles for levels 1 to 10
}

def load_puzzle(level):
    puzzle_file, layout_file = puzzles[level]
    puzzle = []
    layout = []
    with open(puzzle_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            puzzle.append([int(cell) if cell else None for cell in row])
    with open(layout_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            layout.append([int(cell) for cell in row])
    return puzzle, layout

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    level = int(request.form['level'])
    puzzle, layout = load_puzzle(level)
    return render_template('play.html', puzzle=puzzle, layout=layout)

if __name__ == '__main__':
    app.run(debug=True)