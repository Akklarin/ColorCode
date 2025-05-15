"""Module providing color mixing logic for RGB hexadecimal color codes."""


class ColorMixer:
    """A class to mix multiple hex color codes into a single average color.

    Attributes:
        colors (list[str]): A list of hexadecimal color codes added to the mixer.
    """

    def __init__(self):
        """Initialize the ColorMixer with an empty color list."""
        self.colors = []

    def add_color(self, hex_color: str):
        """Add a hexadecimal color code to the mixer."""
        self.colors.append(hex_color)

    def step_back(self):
        """
        Remove the most recently added color from the mixer.

        Does nothing if the list is already empty.
        """
        if len(self.colors) > 0:
            self.colors.pop()

    def mix_colors(self) -> str:
        """
        Compute the average color from all added colors.

        Returns:
            str: The resulting color as a hex string. Returns white ('#ffffff') if no colors are present.
        """
        if not self.colors:
            return "#ffffff"

        r_total, g_total, b_total = 0, 0, 0
        for color in self.colors:
            color = color.lstrip("#")
            r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
            r_total += r
            g_total += g
            b_total += b

        n = len(self.colors)
        r_avg = r_total // n
        g_avg = g_total // n
        b_avg = b_total // n

        return "#{:02x}{:02x}{:02x}".format(r_avg, g_avg, b_avg)
