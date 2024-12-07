import pyxel
import random
from board import BoardItem, TILE_SIZE

class Ghost:
    def __init__(self, x: int, y: int, color: int, board, speed: int = 1):
        self.x = x
        self.y = y
        self.color = color
        self.board = board
        self._speed = speed
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.image = 0
        self.animation_frame = 0

    def update(self, pacman_x, pacman_y):
        self.move()
        self.update_animation_ghost()
        self.map_limits()

    def can_move_to(self, new_x, new_y):
        """
        Check if the ghost can move to the given position.
        """
        left_tile_x = int(new_x / TILE_SIZE)
        right_tile_x = int((new_x + 15) / TILE_SIZE)
        top_tile_y = int(new_y / TILE_SIZE)
        bottom_tile_y = int((new_y + 15) / TILE_SIZE)

        max_x = len(self.board.board_map[0])
        max_y = len(self.board.board_map)

        # Wrap coordinates for teleportation logic
        left_tile_x %= max_x
        right_tile_x %= max_x
        top_tile_y %= max_y
        bottom_tile_y %= max_y

        # Check for wall collisions
        if (self.board.board_map[top_tile_y][left_tile_x] == BoardItem.WALL or
            self.board.board_map[top_tile_y][right_tile_x] == BoardItem.WALL or
            self.board.board_map[bottom_tile_y][left_tile_x] == BoardItem.WALL or
            self.board.board_map[bottom_tile_y][right_tile_x] == BoardItem.WALL):
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
            self.image = self.animation_frame * 16
        elif self.direction == "left":
            self.image = 32 + self.animation_frame * 16
        elif self.direction == "up":
            self.image = 64 + self.animation_frame * 16
        elif self.direction == "down":
            self.image = 96 + self.animation_frame * 16

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

    def draw(self):
        """
        Draw ghost sprite.
        """
        pyxel.blt(self.x, self.y, 1, self.image, 0, 16, 16, 0)

    def change_direction(self, pacman_x: int, pacman_y: int):
        """
        Change direction at random or based on AI logic (can be refined in subclasses).
        :param pacman_x: x-coordinate of Pac-Man.
        :param pacman_y: y-coordinate of Pac-Man.
        """
        if random.random() < 0.1:  # 10% chance to change direction
            self.direction = random.choice(['up', 'down', 'left', 'right'])

    def frightened_move(self):
        """
        Move randomly when frightened.
        """
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed


class Blinky(Ghost):
    def move(self, pacman_x: int, pacman_y: int):
        """
        Blinky chases Pac-Man directly.
        :param pacman_x: x-coordinate of Pac-Man.
        :param pacman_y: y-coordinate of Pac-Man.
        """
        if abs(self.x - pacman_x) > abs(self.y - pacman_y):
            self.direction = "left" if self.x > pacman_x else "right"
        else:
            self.direction = "up" if self.y > pacman_y else "down"
        super().move(pacman_x, pacman_y)


class Pinky(Ghost):
    def move(self, pacman_x: int, pacman_y: int, pacman_dir: str):
        """
        Pinky predicts Pac-Man's next move based on his direction.
        :param pacman_x: x-coordinate of Pac-Man.
        :param pacman_y: y-coordinate of Pac-Man.
        :param pacman_dir: Pac-Man's current direction.
        """
        if pacman_dir == "up":
            target_x, target_y = pacman_x, pacman_y - 16
        elif pacman_dir == "down":
            target_x, target_y = pacman_x, pacman_y + 16
        elif pacman_dir == "left":
            target_x, target_y = pacman_x - 16, pacman_y
        elif pacman_dir == "right":
            target_x, target_y = pacman_x + 16, pacman_y
        else:
            target_x, target_y = pacman_x, pacman_y

        self.direction = "left" if self.x > target_x else "right"
        super().move(target_x, target_y)


class Inky(Ghost):
    def move(self, pacman_x: int, pacman_y: int, blinky_x: int, blinky_y: int):
        """
        Inky moves based on a combination of Pac-Man's and Blinky's positions.
        :param pacman_x: x-coordinate of Pac-Man.
        :param pacman_y: y-coordinate of Pac-Man.
        :param blinky_x: x-coordinate of Blinky.
        :param blinky_y: y-coordinate of Blinky.
        """
        target_x = 2 * pacman_x - blinky_x
        target_y = 2 * pacman_y - blinky_y
        self.direction = "left" if self.x > target_x else "right"
        super().move(target_x)