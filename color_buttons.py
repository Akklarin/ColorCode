import tkinter as tk


class ColorButtons(tk.Button):
    def __init__(self, master, mode_var, command_map, **kwargs):
        super().__init__(master, **kwargs)
        self.mode_var = mode_var
        self.command_map = command_map
        self.configure(command=self.execute)

    def execute(self):
        key = self.mode_var.get()
        if key in self.command_map:
            return self.command_map[key]()