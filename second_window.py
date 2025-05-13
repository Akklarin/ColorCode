
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

        self.right_frame = tk.LabelFrame(self, text="Замес", font=("Arial", 8), width=150, height=340)
        self.list_frame = tk.Frame(self.right_frame, width=150, height=300)
        self.button_frame = tk.Frame(self.right_frame, width=150, height=40)

        self.right_frame.pack(fill="both", side="right", padx=2, pady=5)
        self.list_frame.pack(fill="both", side='top', padx=2, pady=2, expand=True)
        self.button_frame.pack(fill="x", side='bottom')

        self.listbox = tk.Listbox(self.list_frame, font=("Arial", 12))
        self.listbox.pack(fill="both", padx=2, expand=True)

        self.reset_button = tk.Button(self.button_frame, text="Сброс", font=("Arial", 8), command=self.reset)
        self.back_button = tk.Button(self.button_frame, text="Шаг назад", font=("Arial", 8), command=self.step_back)

        self.back_button.grid(row=0, column=0, sticky="ew", padx=2, pady=5)
        self.reset_button.grid(row=0, column=1, sticky="ew", padx=2, pady=5)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

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
        self.rect = self.canvas.create_rectangle(10, 10, 200, 200, fill=result_color, outline='black')

    def update_shared_entry(self):
        result_color = self.mixer.mix_colors()
        self.shared_entry.delete(0, tk.END)
        self.shared_entry.insert(0, result_color)

    def reset(self):
        self.mixer.colors.clear()
        self.listbox.delete(0, tk.END)
        self.canvas.delete("all")
        self.shared_entry.delete(0, tk.END)

    def step_back(self):
        self.listbox.delete(tk.END)
        self.mixer.step_back()
        self.update_canvas()
        self.update_shared_entry()