import pyxel

from board import Board, TILE_SIZE
from pacman import Pacman
from ghosts import Blinky, Pinky, Inky, Clyde
from music import PyxelSounds
from game import Lives, Points



# We will import all the other files.
"""This would be the main program in which we will execute all the other
ones to make the game run properly."""

""" En esta clase App, se inicializará todo el programa. """
class App:
    LEVELS = [0,1,2,3]
    HEIGHT = 32
    WIDTH = 32
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
        self.sounds.update(self.pacman.powered)
        self.pacman.update()
        for ghost in self.ghosts:
            ghost.update()
        self.points.update()
        if len(self.board.dots) == 0:
            self.next_level()

    def draw(self):
        pyxel.cls(0)
        self.board.draw()
        self.pacman.draw()
        for ghost in self.ghosts:
            ghost.draw()
        self.lives.draw()
        self.points.draw()

    def load_level(self, level_index):
        self.board = Board(pyxel.tilemap(self.LEVELS[level_index]))
        self.pacman = Pacman(self.board, self.points)
        self.ghosts = [Blinky(128, 120, self.board),
                       Pinky(128, 120, self.board),
                       Inky(128, 120, self.board),
                       Clyde(128, 120,self.board)]
        self.points.change_points_position(level_index)
        self.lives.change_lives_position(level_index)

    def next_level(self):
        self.current_level += 1
        if self.current_level < len(self.LEVELS):
            self.load_level(self.current_level)
        else:
            print("¡Game completed!")
            self.sounds.stop_music()
            pyxel.bltm(0, 0, self.tilemap(3), 0,0,self.WIDTH * TILE_SIZE, self.HEIGHT * TILE_SIZE)

App()