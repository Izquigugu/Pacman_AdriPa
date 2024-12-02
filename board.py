import pyxel

TILE_SIZE = 8
SPRITE_BANK = 2

class BoardItem:
    WALL = (2, 8)
    EMPTY_SPACE = (3, 8)
    GHOSTS_DOOR = (4, 8)
    PACMAN = (5, 8)
    GHOSTS = ()
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
        self.pacman_grid_x = 0
        self.pacman_grid_y = 0
        for y in range(self.HEIGHT):
            self.board_map.append([])
            for x in range(self.WIDTH):
                if self.tilemap.pget(x, y) == BoardItem.WALL:
                    self.board_map[y].append(BoardItem.WALL)
                elif self.tilemap.pget(x, y) == BoardItem.GHOSTS_DOOR:
                    self.board_map[y].append(BoardItem.GHOSTS_DOOR)
                elif self.tilemap.pget(x, y) == BoardItem.PACMAN:
                    self.board_map[y].append(BoardItem.EMPTY_SPACE)
                    self.pacman_grid_x = x
                    self.pacman_grid_y = y
                else:
                    self.board_map[y].append(BoardItem.EMPTY_SPACE)

    def draw(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                board_item = self.board_map[y][x]
                board_item_draw(pyxel, x, y, board_item)


def board_item_draw(pyxel, x, y, board_item):
    pyxel.blt(
        x * TILE_SIZE,
        y * TILE_SIZE,
        SPRITE_BANK,
        board_item[0] * TILE_SIZE,
        board_item[1] * TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE
    )

