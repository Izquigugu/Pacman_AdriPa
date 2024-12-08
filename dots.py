import pyxel


class Dot:
    """
    This class represents a dot (or pellet) on the game board in Pac-Man.
    It manages its position, state (collected or not), and visual appearance.
    """
    def __init__(self, x: int, y: int):
        """
        Initialize the Dot's attributes.
        :param x: The x-coordinate of the dot on the screen.
        :param y: The y-coordinate of the dot on the screen.
        """
        self.x = x # Horizontal position of the dot
        self.y = y  # Vertical position of the dot
        self.is_big = False  # Default: The dot is small (not a power pellet)
        self.collected = False  # Tracks whether the dot has been collected by Pac-Man

    def collect(self):
        """
        Marks the dot as collected.
        When collected, it will not be drawn on the screen anymore.
        """
        self.collected = True

    def draw(self):
        """
        Draw the dot on the screen, if it has not been collected.
        Uses Pyxel's blt function to render the dot from the sprite bank.
        """
        if not self.collected:
            pyxel.blt(self.x, self.y, 2, 48, 64, 8, 8, 0)


