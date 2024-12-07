import pyxel

from board import Board
from pacman import Pacman
from ghosts import Ghost
from music import PyxelSounds
from game import Lives, Points



# We will import all the other files.
"""This would be the main program in which we will execute all the other
ones to make the game run properly."""

""" En esta clase App, se inicializará todo el programa. """
class App:
    LEVELS = [0, 1, 2]
    def __init__(self):
        pyxel.init(256,256)
        pyxel.load("assets/resources.pyxres")
        self.current_level = 0
        self.points = Points()
        self.lives = Lives()
        self.load_level(self.current_level)
        self.sounds = PyxelSounds()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.sounds.stop_music()
            pyxel.quit()
        self.pacman.update()
        self.ghost.update(self.pacman.x, self.pacman.y)
        self.points.update()
        # Todavía no funciona los niveles, tengo que mirarlo
        """if len(self.board.dots) == 0:
            self.next_level()"""

    def draw(self):
        pyxel.cls(0)
        self.board.draw()
        self.pacman.draw()
        self.ghost.draw()
        self.lives.draw()
        self.points.draw()

    def load_level(self, level_index):
        self.board = Board(pyxel.tilemap(self.LEVELS[level_index]))
        self.pacman = Pacman(self.board, self.points)
        self.ghost = Ghost(200, 150, False)

    def next_level(self):
        self.current_level += 1
        if self.current_level < len(self.LEVELS):
            self.load_level(self.current_level)
        else:
            print("¡Game completed!")
            # Habría que hacer una pantalla final

App()