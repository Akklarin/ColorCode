
import tkinter as tk
from color_mixer import ColorMixer
from dictionaries import cod_dict


class MixerWindow(tk.Toplevel):
    def __init__(self, master, shared_entry):
        super().__init__(master)
        self.place_next_to(master)
        self.title("Микшер")
        self.shared_entry = shared_entry
        self.mixer = ColorMixer()

        self.list_frame = tk.LabelFrame(self, text="Замес", font=("Arial", 8), width=150)
        self.list_frame.pack(side="right", fill="y", padx=2, pady=5)
        self.listbox = tk.Listbox(self.list_frame, font=("Arial", 12))
        self.listbox.pack(fill="both", padx=2, expand=True)
        self.reset_button = tk.Button(self.list_frame, text="Сброс", font=("Arial", 8), command=self.reset)
        self.reset_button.pack(fill="x", padx=4, pady=4)
        self.canvas_frame = tk.LabelFrame(self, text="Результат смешения", font=("Arial", 8), width=450)
        self.canvas_frame.pack(side="left", fill="y", padx=2, pady=5)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

    def place_next_to(self, master):
        master.update_idletasks()
        x = master.winfo_x()
        y = master.winfo_y()
        width = master.winfo_width()

        new_x = x + width + 2
        new_y = y

        self.geometry(f"600x340+{new_x}+{new_y}")

    def add_color(self, hex_color: str):
        self.mixer.add_color(hex_color)
        self.listbox.insert(tk.END, ' ' + cod_dict[hex_color])
        self.update_canvas()
        self.update_shared_entry()

    def update_canvas(self):
        result_color = self.mixer.mix_colors()
        self.canvas.delete("all")
        self.canvas.create_rectangle(10, 10, 200, 200, fill=result_color, outline='black')

    def update_shared_entry(self):
        result_color = self.mixer.mix_colors()
        self.shared_entry.delete(0, tk.END)
        self.shared_entry.insert(0, result_color)

    def reset(self):
        self.mixer.colors.clear()
        self.listbox.delete(0, tk.END)
        self.canvas.delete("all")
        self.shared_entry.delete(0, tk.END)
