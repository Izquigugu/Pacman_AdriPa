import pyxel
from dots import Dot

TILE_SIZE = 8
SPRITE_BANK = 3

class BoardItem:
    WALL = (2, 8)
    EMPTY_SPACE = (3, 8)
    GHOSTS_DOOR = (4, 8)
    PACMAN = (5, 8)
    GHOSTS = ()
    DOTS = (6,8)
    POWERUP = (7, 8)
""" He intentado implementar el mapa ya en el juego pero todavía no soy 
capaz, tengo que investigar a ver qué es lo que da error. """
class Board:
    # Medida de tiles en el mapa. (32x32)
    # Cada tile es de 8x8 pixels.-
    HEIGHT = 32
    WIDTH = 32

    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.board_map = []
        self.dots = []
        self.pacman_grid_x = 0
        self.pacman_grid_y = 0
        for y in range(self.HEIGHT):
            self.board_map.append([])
            for x in range(self.WIDTH):
                if self.tilemap.pget(x, y) == BoardItem.WALL:
                    self.board_map[y].append(BoardItem.WALL)
                elif self.tilemap.pget(x, y) == BoardItem.DOTS:
                    self.board_map[y].append(BoardItem.DOTS)
                    self.dots.append(Dot(x * 16, y * 16))
                elif self.tilemap.pget(x, y) == BoardItem.POWERUP:
                    self.board_map[y].append(BoardItem.POWERUP)
                elif self.tilemap.pget(x, y) == BoardItem.GHOSTS_DOOR:
                    self.board_map[y].append(BoardItem.GHOSTS_DOOR)
                elif self.tilemap.pget(x, y) == BoardItem.PACMAN:
                    self.board_map[y].append(BoardItem.EMPTY_SPACE)
                    self.pacman_grid_x = x
                    self.pacman_grid_y = y
                else:
                    self.board_map[y].append(BoardItem.EMPTY_SPACE)

    def draw(self):
        pyxel.bltm(0, 0, self.tilemap, 0, 0, self.WIDTH * TILE_SIZE,
                   self.HEIGHT * TILE_SIZE)


