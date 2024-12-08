import pyxel
import random
from board import BoardItem, TILE_SIZE

class Ghost:
    def __init__(self, x: int, y: int, board, speed: int = 1, sprite_v: int = 0):
        self.x = x
        self.y = y
        self.board = board
        self._speed = speed
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.u = 0
        self.v = sprite_v #para determinar el color de cada fantasma
        self.animation_frame = 0

    def update(self):
        self.move()
        self.update_animation_ghost()
        self.map_limits()
        self.change_direction()

    def draw(self):
        """
        Draw ghost sprite.
        """
        pyxel.blt(self.x, self.y, 1, self.u, self.v, 16, 16, 0)

    def can_move_to(self, new_x, new_y):
        # Dimensiones del sprite de Pac-Man (16x16 píxeles)
        ghost_width = 16
        ghost_height = 16

        # Calcular las esquinas del sprite
        # También las mitades para evitar bugs
        left_tile_x = int(new_x / TILE_SIZE)
        mid_left_tile_x = int((new_x + 8) / TILE_SIZE)
        right_tile_x = int((new_x + ghost_width - 1) / TILE_SIZE)
        mid_right_tile_x = int((new_x + ghost_width / 2 - 1) / TILE_SIZE)
        top_tile_y = int(new_y / TILE_SIZE)
        mid_top_tile_y = int((new_y + 8) / TILE_SIZE)
        bottom_tile_y = int((new_y + ghost_height - 1) / TILE_SIZE)
        mid_bottom_tile_y = int((new_y + ghost_height / 2 - 1) / TILE_SIZE)

        # Asegurarse de que los índices están dentro de los límites del mapa
        max_x = len(self.board.board_map[0])
        max_y = len(self.board.board_map)

        # Ajustar para teletransporte: tratar índices fuera del rango como válidos
        left_tile_x %= max_x
        right_tile_x %= max_x
        top_tile_y %= max_y
        bottom_tile_y %= max_y
        mid_left_tile_x %= max_x
        mid_right_tile_x %= max_x
        mid_top_tile_y %= max_y
        mid_bottom_tile_y %= max_y

        # Verificar si cualquiera de las esquinas toca un tile de tipo WALL
        # También verificamos la mitad de los lados para evitar bugs
        if (
                self.board.board_map[top_tile_y][left_tile_x] == BoardItem.WALL
                or self.board.board_map[top_tile_y][mid_left_tile_x] ==
                BoardItem.WALL or self.board.board_map[mid_top_tile_y][
            left_tile_x] == BoardItem.WALL or self.board.board_map[top_tile_y][
            right_tile_x] == BoardItem.WALL or
                self.board.board_map[top_tile_y][
                    mid_right_tile_x] == BoardItem.WALL or
                self.board.board_map[
                    mid_top_tile_y][
                    right_tile_x] == BoardItem.WALL
                or self.board.board_map[bottom_tile_y][
            left_tile_x] == BoardItem.WALL or
                self.board.board_map[bottom_tile_y][
                    mid_left_tile_x] == BoardItem.WALL or self.board.board_map[
            mid_bottom_tile_y][
            left_tile_x] == BoardItem.WALL
                or self.board.board_map[bottom_tile_y][
            right_tile_x] == BoardItem.WALL or
                self.board.board_map[bottom_tile_y][
                    mid_right_tile_x] == BoardItem.WALL or
                self.board.board_map[
                    mid_bottom_tile_y][
                    right_tile_x] == BoardItem.WALL
        ):
            return False
        return True

    def move(self):
        new_x, new_y = self.x, self.y

        if self.direction == "up":
            new_y -= self._speed
        elif self.direction == "down":
            new_y += self._speed
        elif self.direction == "left":
            new_x -= self._speed
        elif self.direction == "right":
            new_x += self._speed

        # Check for collision and update position
        if self.can_move_to(new_x, new_y):
            self.x, self.y = new_x, new_y
        else:
            # If collision, choose a new random direction
            self.direction = random.choice(['up', 'down', 'left', 'right'])

    def update_animation_ghost(self):
        """
        Update ghost animation frames.
        """
        if pyxel.frame_count % 10 == 0:
            self.animation_frame = (self.animation_frame + 1) % 2

        if self.direction == "right":
            self.u = self.animation_frame * 16
        elif self.direction == "left":
            self.u = 32 + self.animation_frame * 16
        elif self.direction == "up":
            self.u = 64 + self.animation_frame * 16
        elif self.direction == "down":
            self.u = 96 + self.animation_frame * 16

    def map_limits(self):
        """
        Teleport ghost to the opposite side if it crosses map boundaries.
        """
        if self.x < -16:
            self.x = 256
        if self.x > 256:
            self.x = -16
        if self.y < -16:
            self.y = 256
        if self.y > 256:
            self.y = -16

    def change_direction(self):
        """
        Change direction at random or based on AI logic (can be refined in subclasses).
        """
        if random.random() < 0.02:  # 10% chance to change direction
            self.direction = random.choice(['up', 'down', 'left', 'right'])

    def frightened_move(self):
        """
        Move randomly when frightened.
        """
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        if self.direction == "up":
            self.y -= self._speed
        elif self.direction == "down":
            self.y += self._speed
        elif self.direction == "left":
            self.x -= self._speed
        elif self.direction == "right":
            self.x += self._speed

class Blinky(Ghost):
    def __init__(self, blinky_x, blinky_y, board):
        super().__init__(blinky_x, blinky_y, board, speed=1, sprite_v=0)

class Pinky(Ghost):
    def __init__(self, pinky_x, pinky_y, board):
        super().__init__(pinky_x, pinky_y, board, speed=1, sprite_v=16)

class Inky(Ghost):
    def __init__(selfself, inky_x, inky_y, board):
        super().__init__(inky_x, inky_y, board, speed=1, sprite_v=32)

class Clyde(Ghost):
    def __init__(self, clyde_x, clyde_y, board):
        super().__init__(clyde_x, clyde_y, board, speed=2, sprite_v=48)