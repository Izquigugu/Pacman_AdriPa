import pyxel

class Lives:
    def __init__(self):
        self.text = "Lives: 3"  # Static text for now

    def draw(self):
        # Display the text on the screen
        pyxel.text(210, 101, self.text, pyxel.COLOR_WHITE)

class Points:
    def __init__(self):
        self.text = "Points: 0"  # Static text for now

    def draw(self):
        # Display the text on the screen
        pyxel.text(10, 101, self.text, pyxel.COLOR_WHITE)

"""class Level:
class Scoreboards:"""