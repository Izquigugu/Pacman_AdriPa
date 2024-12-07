import pyxel
from board import Board


class Lives:
    def __init__(self):
        self.text = "Lives: 3"  # Static text for now

    def draw(self):
        # Display the text on the screen
        pyxel.text(210, 101, self.text, pyxel.COLOR_WHITE)

class Points:
    def __init__(self):
        self.points = 0
        self.text = f"Points: {self.points}"  # Static text for now

    def update(self):
        self.text = f"Points: {self.points}"

    def draw(self):
        # Display the text on the screen
        pyxel.text(5, 101, self.text, pyxel.COLOR_WHITE)

    def sum_dot_points(self):
        self.points += 10

"""class Level:
class Scoreboards:"""