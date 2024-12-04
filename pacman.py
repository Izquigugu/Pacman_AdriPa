import pyxel
from board import Board, BoardItem, TILE_SIZE

class Pacman:
    def __init__(self, board):
        self.x = board.pacman_grid_x * TILE_SIZE
        self.y = board.pacman_grid_y * TILE_SIZE
        self.board = board
        self.alive = True
        self.image = 0
        self.powered = False
        self.velocity = 2
        self.direction = 0
        self.animation_frame = 0
        self.animation_speed = 1

    def update(self):
        self.move()
        self.update_animation_pacman()
        self.map_limits()
        self.check_dot_collision()

    def draw(self):
        u = self.animation_frame * 16
        v = self.direction * 16
        pyxel.blt(self.x, self.y, 0, u, v, 16, 16, 0)

    def can_move_to(self, new_x, new_y):
        # Dimensiones del sprite de Pac-Man (16x16 píxeles)
        pacman_width = 16
        pacman_height = 16

        # Calcular las esquinas del sprite
        left_tile_x = int(new_x / TILE_SIZE)
        right_tile_x = int((new_x + pacman_width - 1) / TILE_SIZE)
        top_tile_y = int(new_y / TILE_SIZE)
        bottom_tile_y = int((new_y + pacman_height - 1) / TILE_SIZE)

        # Asegurarse de que los índices están dentro de los límites del mapa
        max_x = len(self.board.board_map[0])
        max_y = len(self.board.board_map)

        # Ajustar para teletransporte: tratar índices fuera del rango como válidos
        left_tile_x %= max_x
        right_tile_x %= max_x
        top_tile_y %= max_y
        bottom_tile_y %= max_y

        # Verificar si cualquiera de las esquinas toca un tile de tipo WALL
        if (
                self.board.board_map[top_tile_y][left_tile_x] == BoardItem.WALL
                or self.board.board_map[top_tile_y][
            right_tile_x] == BoardItem.WALL
                or self.board.board_map[bottom_tile_y][
            left_tile_x] == BoardItem.WALL
                or self.board.board_map[bottom_tile_y][
            right_tile_x] == BoardItem.WALL
        ):
            return False
        return True

    def move(self):
        # Movimiento basado en las teclas presionadas
        if pyxel.btn(pyxel.KEY_W):  # Mover hacia arriba
            new_y = self.y - self.velocity
            if self.can_move_to(self.x, new_y):
                self.y = new_y
                self.direction = 2
        if pyxel.btn(pyxel.KEY_S):  # Mover hacia abajo
            new_y = self.y + self.velocity
            if self.can_move_to(self.x, new_y):
                self.y = new_y
                self.direction = 3
        if pyxel.btn(pyxel.KEY_A):  # Mover hacia la izquierda
            new_x = self.x - self.velocity
            if self.can_move_to(new_x, self.y):
                self.x = new_x
                self.direction = 1
        if pyxel.btn(pyxel.KEY_D):  # Mover hacia la derecha
            new_x = self.x + self.velocity
            if self.can_move_to(new_x, self.y):
                self.x = new_x
                self.direction = 0

    def map_limits(self):
        # Dimensiones del mapa en píxeles
        map_width = len(self.board.board_map[0]) * TILE_SIZE
        map_height = len(self.board.board_map) * TILE_SIZE

        # Teletransportar a Pac-Man si cruza los bordes
        if self.x < -16:
            self.x = map_width
        elif self.x >= map_width:
            self.x = -16

        if self.y < -16:
            self.y = map_height
        elif self.y >= map_height:
            self.y = -16

    def update_animation_pacman(self):
        # Animar Pac-Man cuando se está moviendo
        if (
            pyxel.btn(pyxel.KEY_A)
            or pyxel.btn(pyxel.KEY_S)
            or pyxel.btn(pyxel.KEY_D)
            or pyxel.btn(pyxel.KEY_W)
        ):
            self.animation_frame = (self.animation_frame + 1) % (
                self.animation_speed * 6
            )
        elif self.animation_frame == 0:
            self.animation_frame += 1
        else:
            self.animation_frame = self.animation_frame

    def check_dot_collision(self):
        tile_x = int(self.x / TILE_SIZE)
        tile_y = int(self.y / TILE_SIZE)

        if self.board.tilemap.pget(tile_x, tile_y) == BoardItem.DOTS:
            print(f"Comiendo punto en: ({tile_x}, {tile_y})")  # Depuración
            self.board.tilemap.pset(tile_x, tile_y, BoardItem.EMPTY_SPACE)
            for dot in self.board.dots:
                if dot.x == tile_x * TILE_SIZE and dot.y == tile_y * TILE_SIZE:
                    self.board.dots.remove(dot)
            print(len(self.board.dots))

