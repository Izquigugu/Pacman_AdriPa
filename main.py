import pyxel

from board import Board
from pacman import Pacman
from ghosts import Ghost


# We will import all the other files.
"""This would be the main program in which we will execute all the other
ones to make the game run properly."""

""" En esta clase App, se inicializará todo el programa. """
class App:
    def __init__(self):
        pyxel.init(256,256)
        #Adri, aqui no se si se podría añadir esto scale = 8, caption="Pacman", fps=60 al final del parentesis
        pyxel.load("assets/resources.pyxres")

        self.board = Board(pyxel.tilemap(0))
        self.pacman = Pacman(200, 150, False)
        self.ghost = Ghost(200, 150, False)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.pacman.update()
        self.ghost.update(self.pacman.x, self.pacman.y)

        #Que es esto?

    def draw(self):
        pyxel.cls(0)
        self.board.draw()
        self.pacman.draw()
        self.ghost.draw()

App()