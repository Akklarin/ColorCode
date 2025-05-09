import tkinter as tk
from color_buttons import ColorButtons
from second_window import MixerWindow
from dictionaries import name_cod,cod_dict


class App:
    def __init__(self, master):
        self.master = master
        self.set_window_geometry()
        self.mode_var = tk.IntVar(value=1)
        self.mixer_window = None
        self.current_color = None

        self.lab = tk.Label(master, text='', font='Arial 10')
        self.e = tk.Entry(master, width=16, font='Arial 16', justify='center')
        self.lab.pack()
        self.e.pack()

        self.radioframe = tk.Frame(master)
        self.radioframe.pack()

        tk.Radiobutton(self.radioframe, text="Базовый", variable=self.mode_var, value=1,
                       command=self.on_mode_change).pack(side='left')
        tk.Radiobutton(self.radioframe, text="Микшер", variable=self.mode_var, value=2,
                       command=self.on_mode_change).pack(side='right')

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(fill='both', expand=True)

        for i in name_cod.keys():
            btn = ColorButtons(
                self.button_frame,
                mode_var=self.mode_var,
                command_map={
                    1: lambda i=i: self.push_m1(i, name_cod[i]),
                    2: lambda i=i: self.push_m2(name_cod[i]),
                },
                bg=name_cod[i])
            btn.pack(fill='both', padx=2, pady=1, expand=True)

    def set_window_geometry(self):
        w = self.master.winfo_screenwidth() // 2 - 300
        h = self.master.winfo_screenheight() // 2 - 75
        self.master.geometry('200x340+{}+{}'.format(w, h))

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == 2:
            if self.mixer_window is None or not self.mixer_window.winfo_exists():
                self.mixer_window = MixerWindow(self.master, self.e)
                self.lab['text'] = ''
                self.e.delete(0, 'end')
        else:
            if self.mixer_window and self.mixer_window.winfo_exists():
                self.mixer_window.destroy()
                self.mixer_window = None

    def push_m1(self, butt_name, bg):
        self.lab['text'] = cod_dict[bg]
        self.e.delete(0, 'end')
        self.e.insert(0, name_cod[butt_name])

    def push_m2(self, color):
        if self.mode_var.get() == 2 and self.mixer_window:
            self.mixer_window.add_color(color)