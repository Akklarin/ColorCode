"""Module defining the ColorButtons class for mode-dependent color actions in the GUI."""

import tkinter as tk


class ColorButtons(tk.Button):
    """Custom Tkinter button that executes different commands depending on the current mode.

    Attributes:
        mode_var (tk.IntVar): Variable indicating the current mode (e.g., 1 for basic, 2 for mixer).
        command_map (dict): Dictionary mapping mode integers to callable command functions.
    """

    def __init__(self, master, mode_var, command_map, **kwargs):
        """
        Initialize the ColorButtons widget.

        Args:
            master (tk.Widget): The parent widget.
            mode_var (tk.IntVar): Tkinter variable used to track the current mode.
            command_map (dict[int, Callable]): A dictionary mapping mode values to commands.
            **kwargs: Additional keyword arguments passed to the tk.Button initializer.
        """
        super().__init__(master, **kwargs)
        self.mode_var = mode_var
        self.command_map = command_map
        self.configure(command=self.execute)

    def execute(self):
        """Execute the command associated with the current mode, if available."""
        key = self.mode_var.get()
        if key in self.command_map:
            return self.command_map[key]()
