import pyxel
from board import Board


class Lives:
    MAP_POSITIONS_X = [210, 224, 152]
    MAP_POSITIONS_Y = [101, 12, 8]
    def __init__(self):
        self.lives = 3
        self.x = 210
        self.y = 101
        self.text = f"Lives: {self.lives}"  # Static text for now

    def update(self):
        self.text = f"Lives: {self.lives}"

    def draw(self):
        # Display the text on the screen
        pyxel.text(self.x, self.y, self.text, pyxel.COLOR_WHITE)

    def change_lives_position(self, tilemap_num):
        self.x = self.MAP_POSITIONS_X[tilemap_num]
        self.y = self.MAP_POSITIONS_Y[tilemap_num]


class Points:
    MAP_POSITIONS_X = [5, 5, 72]
    MAP_POSITIONS_Y = [101, 12, 8]
    def __init__(self):
        self.points = 0
        self.x = 5
        self.y = 101
        self.text = f"Points: {self.points}"  # Static text for now

    def update(self):
        self.text = f"Points: {self.points}"

    def draw(self):
        # Display the text on the screen
        pyxel.text(self.x, self.y, self.text, pyxel.COLOR_WHITE)

    def sum_points(self, sum_points):
        self.points += sum_points

    def change_points_position(self, tilemap_num):
        self.x = self.MAP_POSITIONS_X[tilemap_num]
        self.y = self.MAP_POSITIONS_Y[tilemap_num]



"""class Level:
class Scoreboards:"""