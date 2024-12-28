import tkinter as tk

class StartupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Select Level")

        # Create a listbox with 6 items
        self.listbox = tk.Listbox(root, height=6)
        self.listbox.pack(padx=20, pady=20)

        levels = [
            "0: 5x5 - level 5",
            "1: 5x5 - level 6",
            "2: 9x5 - level 5",
            "3: 9x11- level 5",
            "4: 9x5 - level 7 moeilijk",
            "5: 9x11- level 7 heel moeilijk"
        ]

        for level in levels:
            self.listbox.insert(tk.END, level)

        # Bind the Enter key to the selection handler
        self.root.bind("<Return>", self.on_enter)

    def on_enter(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_level = selected_index[0]
            print(f"Selected Level: {selected_level}")
            # Pass the selected level to the TectonicApp
            self.start_tectonic_app(selected_level)

    def start_tectonic_app(self, level):
        self.root.destroy()  # Close the startup window
        main_window = tk.Tk()
        app = TectonicApp(main_window, level)
        main_window.mainloop()
