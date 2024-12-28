import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import csv
import tectonic as t


class TectonicApp:
    def __init__(self, root, tec):
        self.root = root
        self.root.title("Tectonic Player")

        self.tec =tec
        self.selected_row = 0
        self.selected_col = 0

        # Initialize the StringVar for the hint label text
        self.hint_label_text = tk.StringVar()
        self.hint_label_text.set("Initial Text")

        self.create_widgets()
        self.update_selection()

    def create_buttons(self, parent, values, row_start, type):
        size_mapping = {
            "normal": {"width": 10, "height": 5},
            "small": {"width": 5, "height": 1}
        }
        for i, value in enumerate(values):
            button = tk.Button(parent, text=str(value), width=size_mapping[type]["width"], height=size_mapping[type]["height"], command=lambda v=value: self.button_pressed(type, v))
            button.grid(row=row_start, column=i, padx=5, pady=5)

    def cell_clicked(self, event, row, col):
        self.selected_col = col
        self.selected_row = row
        self.update_selection()

    def make_cell_click_handler(self, row, col):
        return lambda event: self.cell_clicked(event, row, col)

    def create_widgets(self):
        self.wcells = []
        cell_width = 100
        cell_height = 100

        for i in range(self.tec.rows):
            row_cells = []
            for j in range(self.tec.cols):
                cell_frame = tk.Frame(self.root, width=cell_width, height=cell_height, highlightbackground="black",
                                      highlightthickness=1)
                cell_frame.grid(row=i, column=j, sticky="nsew")
                cell_frame.grid_propagate(False)  # Prevent the frame from resizing to fit its content

                wcell = tk.Label(cell_frame, text=self.tec.board[i][j] if self.tec.board[i][j] != 0 else "", width=10,
                                 height=5, borderwidth=0.5, relief="solid")
                wcell.pack(fill='both', expand=True)
                wcell.config(font=("Helvetica", 12, "bold"))
                wcell.bind("<Button-1>", lambda event, row=i, col=j: self.cell_clicked(event, row, col))

                if self.tec.board[i][j] == 0:
                    small_numbers = tk.Label(wcell, text=self.tec.find_cell(i, j).show_pos(), font=("Arial", 8),
                                             anchor='nw')
                    small_numbers.place(relx=0.02, rely=0.02)

                row_cells.append((cell_frame, wcell))
            self.wcells.append(row_cells)

        for i in range(self.tec.rows):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(self.tec.cols):
            self.root.grid_columnconfigure(j, weight=1)

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Key-h>", self.hint_event)

        for i in range(1, 6):
            self.root.bind(str(i), self.number_pressed)

        # Create a separate frame for the controls and use grid
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=self.tec.rows, column=0, columnspan=self.tec.cols, pady=10, sticky="ew")

        # Create a frame for the buttons
        self.buttons_frame = tk.Frame(self.control_frame)
        self.buttons_frame.pack(side=tk.TOP, padx=10)

        self.create_buttons(self.buttons_frame, range(1, 6), 0, "normal")
        self.create_buttons(self.buttons_frame, range(1, 6), 1, "small")

        # Create the hint button in the buttons frame
        self.hint_button = tk.Button(self.buttons_frame, text="Hint", command=self.hint)
        self.hint_button.grid(row=2, column=2, columnspan=1, pady=10)

        # Create a frame for the hint label below the buttons
        self.hint_label_frame = tk.Frame(self.control_frame)
        self.hint_label_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Create the hint label in the hint label frame
        self.hint_label_text = tk.StringVar()
        self.hint_label_text.set("Initial Text")
        self.hint_label = tk.Label(self.hint_label_frame, textvariable=self.hint_label_text)
        self.hint_label.pack()

    def number_pressed(self, event):
            # print(f"Number {event.char} pressed")
            self.value_entered(int(event.char))

    def hint_event(self,event):
        self.hint()

    def hint(self):
        hint,row, col, value =tec.hint()
        self.hint_label_text.set(f"hint:{hint}, row={row}, col={col}, value={value}")
        self.selected_col = col
        self.selected_row = row
        self.update_selection()

    def button_pressed(self, type, value):
        # messagebox.showinfo("Button Pressed", f"You pressed button {value} in type {type}")
        if type=="normal":
            self.value_entered( value )
        if type=="small":
            if value in self.tec.find_cell(self.selected_row,self.selected_col).possibilities:
                self.tec.remove_domain (self.selected_row, self.selected_col,value)
                self.update_selection()
            else:
                messagebox.showinfo(title="OOPS!", message="Nee, die waarde zit niet in de mogelijkheden")

    def update_selection(self):
        for r in range(self.tec.rows):
            for c in range(self.tec.cols):
                cell_frame, wcell = self.wcells[r][c]
                wcell.config(borderwidth=0, relief="solid")  # Reset all cells to default border
                if c<=self.tec.cols-2 and self.tec.layout[r][c] != self.tec.layout[r][c+1]:
                    # print(f"right: {r},{c} :{self.layout[r][c]}-{self.layout[r][c+1]}")
                    right_border = tk.Frame(cell_frame, bg="black", width=6)
                    right_border.place(relx=1.0, rely=0.0, relheight=1.0, anchor='ne')
                if r<=self.tec.rows-2 and self.tec.layout[r][c] != self.tec.layout[r+1][c]:
                    # print(f"bottom: {r},{c} : {self.layout[r][c]}-{self.layout[r+1][c]}")
                    bottom_border = tk.Frame(cell_frame, bg="black", height=6)
                    bottom_border.place(relx=0.0, rely=1.0, relwidth=1.0, anchor='sw')
                if r == self.selected_row and c == self.selected_col:
                    wcell.config(bg="yellow")
                else:
                    wcell.config(bg="white")
                if self.tec.board[r][c] == 0:
                    small_numbers = tk.Label(wcell, text=self.tec.find_cell(r,c).show_pos(), font=("Arial", 8), anchor='nw')
                    small_numbers.config(bg=wcell.cget("bg"))
                    small_numbers.place(relx=0.02, rely=0.02)


    def move_left(self, event):
        if self.selected_col > 0:
            self.selected_col -= 1
            self.update_selection()

    def move_right(self, event):
        if self.selected_col < self.tec.cols - 1:
            self.selected_col += 1
            self.update_selection()

    def move_up(self, event):
        if self.selected_row > 0:
            self.selected_row -= 1
            self.update_selection()

    def move_down(self, event):
        if self.selected_row < self.tec.rows - 1:
            self.selected_row += 1
            self.update_selection()

    def value_entered(self, v):
        value = v
        if value in self.tec.find_cell(self.selected_row, self.selected_col).possibilities:
            self.tec.place(self.selected_row, self.selected_col, value)
            cell_frame, wcell = self.wcells[self.selected_row][self.selected_col]
            wcell.config(text=value if value != 0 else "")
            # Destroy only the small numbers label if it exists
            for widget in wcell.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("font") == ("Arial", 8):
                    widget.destroy()
            if value == 0:
                small_numbers = tk.Label(wcell,
                                         text=self.tec.find_cell(self.selected_row, self.selected_col).show_pos(),
                                         font=("Arial", 8), anchor='nw')
                small_numbers.place(relx=0.02, rely=0.02)
            self.update_selection()
            if self.tec.board_filled():
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

    pathlocation="tst/"
    tectonic_list = [
        ["5x5 - level 5", "t2.board.csv", "t2.layout.csv"],
        ["5x5 - level 6", "t1.board.csv","t1.layout.csv"],
        ["9x5 - level 5", "t3.board.9x5.csv", "t3.layout.9x5.csv"],
        ["9x11- level 5", "t4.board.9x11.csv", "t4.layout.9x11.csv"],
        ["9x5 - level 7 moeilijk (100)", "t5.board.9x5.csv", "t5.layout.9x5.csv"]

    ]


    # print("Tectonic-Player")
    # print("Which Tectonic you want to play:")
    # for i,val in enumerate(tectonic_list):
    #     print (f"{i}: {val[0]}")
    #
    # index=int(input("your choice:"))

    index = 0

    # file_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t4.board.9x11.csv'
    # layout_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t4.layout.9x11.csv'
    file_path = pathlocation+tectonic_list[index][1]
    layout_path = pathlocation+tectonic_list[index][2]

    print (f"{file_path},{layout_path}")

    tec= t.Tectonic()
    tec.read_from_csv(file_path, layout_path)

    root = tk.Tk()
    app = TectonicApp(root, tec)
    root.mainloop()

    # matrix.append([int(cell) if cell else 0 for cell in row])
    # file_path = '/Users/ZK38UJ/PycharmProjects/tectonic-solver/tst/t1.board.csv'  # Update this path to your CSV file
