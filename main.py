import pyxel

from board import Board
from pacman import Pacman
from ghosts import Ghost
from music import PyxelSounds
from game import Lives
from game import Points


# We will import all the other files.
"""This would be the main program in which we will execute all the other
ones to make the game run properly."""

""" En esta clase App, se inicializará todo el programa. """
class App:
    def __init__(self):
        pyxel.init(256,256)
        pyxel.load("assets/resources.pyxres")

        self.board = Board(pyxel.tilemap(0))
        self.pacman = Pacman(self.board)
        self.ghost = Ghost(200, 150, False)
        self.sounds = PyxelSounds()

        # Lives Remaining
        self.lives = Lives()  # Initialize Lives with 3 lives

        # Points Gained
        self.points = Points()  # Initialize Lives with 3 lives

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.sounds.stop_music()
            pyxel.quit()
        self.pacman.update()
        self.ghost.update(self.pacman.x, self.pacman.y)


    def draw(self):
        pyxel.cls(0)
        self.board.draw()
        self.pacman.draw()
        self.ghost.draw()
        self.lives.draw()
        self.points.draw()

App()