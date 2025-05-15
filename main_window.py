"""
Main window logic for the ColorCode Mixer application.

This module defines the App class, which creates the primary GUI window.
It manages two application modes: a basic mode for viewing color codes and
a mixer mode for combining colors in a secondary window.

Classes:
    App: Main application class handling the UI and user interactions.
"""

import tkinter as tk
from color_buttons import ColorButtons
from second_window import MixerWindow
from dictionaries import name_cod, cod_dict


class App:
    """
    Main application class for the ColorCode Mixer.

    Attributes:
        master (tk.Tk): The root window.
        mode_var (tk.IntVar): Indicates the current mode (1: Basic, 2: Mixer).
        mixer_window (MixerWindow): The secondary mixer window instance.
        lab (tk.Label): Label for displaying color names.
        e (tk.Entry): Entry widget for displaying color codes.
        radio_frame (tk.Frame): Container for mode selection radio buttons.
        button_frame (tk.Frame): Container for color selection buttons.
    """

    def __init__(self, master):
        """Initializes the App with all widgets and bindings."""
        self.master = master
        self.set_window_geometry()
        self.mode_var = tk.IntVar(value=1)
        self.master.bind_all("<Control-KeyPress>", self.on_ctrl_key)
        self.mixer_window = None

        self.lab = tk.Label(master, text='', font='Arial 10')
        self.e = tk.Entry(master, width=16, font='Arial 16', justify='center')
        self.e.bind("<Control-KeyPress>", self.on_ctrl_key)

        self.lab.pack()
        self.e.pack()

        self.radio_frame = tk.Frame(master)
        self.radio_frame.pack()

        tk.Radiobutton(self.radio_frame, text="Базовый", variable=self.mode_var, value=1,
                       command=self.on_mode_change).pack(side='left')
        tk.Radiobutton(self.radio_frame, text="Mикшер", variable=self.mode_var, value=2,
                       command=self.on_mode_change).pack(side='right')

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(fill='both', expand=True)

        # Create a button for each color using ColorButtons
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
        """Sets the initial size and position of the main window."""
        w = self.master.winfo_screenwidth() // 2 - 300
        h = self.master.winfo_screenheight() // 2 - 75
        self.master.geometry('200x340+{}+{}'.format(w, h))

    def on_ctrl_key(self, event):
        """
        Handles global Ctrl key combinations (e.g., Ctrl+C, Ctrl+Z).

        Args:
            event (tk.Event): The keyboard event.
        """
        if event.state & 0x4:
            if event.keycode == 67:
                self.copy_content()
            elif event.keycode == 90:
                self.try_step_back()

    def copy_content(self):
        """Copies the current content of the entry field to the clipboard."""
        content = self.e.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(content)
        self.master.update()

    def try_step_back(self):
        """Triggers a step back in the mixer window if active."""
        if self.mode_var.get() == 2:
            if hasattr(self, "mixer_window") and self.mixer_window.winfo_exists():
                self.mixer_window.step_back()

    def on_mode_change(self):
        """Handles switching between basic mode and mixer mode."""
        mode = self.mode_var.get()
        if mode == 2:
            if self.mixer_window is None or not self.mixer_window.winfo_exists():
                self.mixer_window = MixerWindow(self.master, self.e, self.mode_var)
                self.lab['text'] = ''
                self.e.delete(0, 'end')
        else:
            if self.mixer_window and self.mixer_window.winfo_exists():
                self.e.delete(0, 'end')
                self.mixer_window.destroy()
                self.mixer_window = None

    def push_m1(self, butt_name, bg):
        """
        Handles color selection in basic mode.

        Args:
            butt_name (str): The name of the color button.
            bg (str): The hex code or background color.
        """
        self.lab['text'] = cod_dict[bg]
        self.e.delete(0, 'end')
        self.e.insert(0, name_cod[butt_name])

    def push_m2(self, color):
        """
        Handles color selection in mixer mode.

        Args:
            color (str): The color code to add to the mixer.
        """
        if self.mode_var.get() == 2 and self.mixer_window:
            self.mixer_window.add_color(color)
