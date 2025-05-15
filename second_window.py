"""Defines the MixerWindow class providing a GUI for mixing colors."""

import tkinter as tk
from color_mixer import ColorMixer
from dictionaries import cod_dict


class MixerWindow(tk.Toplevel):
    """Mixer window for combining multiple colors and displaying the result.

    Attributes:
        shared_entry (tk.Entry): Entry widget shared with the main window.
        mode_var (tk.IntVar): Variable indicating current mode.
        mixer (ColorMixer): Instance managing color mixing logic.
        right_frame (tk.LabelFrame): Frame containing the listbox and buttons.
        list_frame (tk.Frame): Frame containing the listbox.
        button_frame (tk.Frame): Frame containing control buttons.
        listbox (tk.Listbox): Listbox displaying added colors.
        reset_button (tk.Button): Button to reset the mixer.
        back_button (tk.Button): Button to step back one color.
        canvas_frame (tk.LabelFrame): Frame containing the result canvas.
        canvas (tk.Canvas): Canvas to display the mixed color.
    """

    def __init__(self, master, shared_entry, mode_var):
        """Initialize the mixer window and its widgets.

        Args:
            master (tk.Widget): The parent window.
            shared_entry (tk.Entry): Entry widget shared with the main window.
            mode_var (tk.IntVar): Variable tracking the current mode.
        """
        super().__init__(master)
        self.place_next_to(master)
        self.title("Микшер")
        self.shared_entry = shared_entry
        self.mode_var = mode_var
        self.mixer = ColorMixer()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.right_frame = tk.LabelFrame(self, text="Замес", font=("Arial", 8), width=150, height=340)
        self.list_frame = tk.Frame(self.right_frame, width=150, height=300)
        self.button_frame = tk.Frame(self.right_frame, width=150, height=40)

        self.right_frame.pack(fill="both", side="right", padx=2, pady=5)
        self.list_frame.pack(fill="both", side='top', padx=2, pady=2, expand=True)
        self.button_frame.pack(fill="x", side='bottom')

        self.listbox = tk.Listbox(self.list_frame, font=("Arial", 12))
        self.listbox.pack(fill="both", padx=2, expand=True)

        self.reset_button = tk.Button(self.button_frame, text="Сброс", font=("Arial", 8), command=self.reset)
        self.back_button = tk.Button(self.button_frame, text="Назад", font=("Arial", 8), command=self.step_back)

        self.back_button.grid(row=0, column=0, sticky="ew", padx=2, pady=5)
        self.reset_button.grid(row=0, column=1, sticky="ew", padx=2, pady=5)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.canvas_frame = tk.LabelFrame(self, text="Результат смешения", font=("Arial", 8), width=450)
        self.canvas_frame.pack(side="left", fill="y", padx=2, pady=5)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

    def on_close(self):
        """Handle window close event, reset mode and clear entry."""
        self.mode_var.set(1)
        self.shared_entry.delete(0, tk.END)
        self.destroy()

    def place_next_to(self, master):
        """Position this window to the right of the master window."""
        master.update_idletasks()
        x = master.winfo_x()
        y = master.winfo_y()
        width = master.winfo_width()

        new_x = x + width + 2
        new_y = y

        self.geometry(f"600x340+{new_x}+{new_y}")

    def add_color(self, hex_color: str):
        """Add a color to the mixer and update the UI."""
        self.mixer.add_color(hex_color)
        self.listbox.insert(tk.END, ' ' + cod_dict[hex_color])
        self.update_canvas()
        self.update_shared_entry()

    def update_canvas(self):
        """Redraw the color mixing result rectangle centered on the canvas."""
        result_color = self.mixer.mix_colors()
        self.canvas.delete("all")

        rect_width = 200
        rect_height = 200

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width == 1 and canvas_height == 1:
            self.canvas.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

        x0 = (canvas_width - rect_width) // 2
        y0 = (canvas_height - rect_height) // 2
        x1 = x0 + rect_width
        y1 = y0 + rect_height

        self.canvas.create_rectangle(x0, y0, x1, y1, fill=result_color, outline='black')

    def update_shared_entry(self):
        """Update the shared entry widget with the mixed color value."""
        result_color = self.mixer.mix_colors()
        self.shared_entry.delete(0, tk.END)
        self.shared_entry.insert(0, result_color)

    def reset(self):
        """Reset the mixer, clearing all colors and UI elements."""
        self.mixer.colors.clear()
        self.listbox.delete(0, tk.END)
        self.canvas.delete("all")
        self.shared_entry.delete(0, tk.END)

    def step_back(self):
        """Remove the last added color and update the UI."""
        self.listbox.delete(tk.END)
        self.mixer.step_back()
        self.update_canvas()
        self.update_shared_entry()
