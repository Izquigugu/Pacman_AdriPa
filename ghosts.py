import pyxel
import random
from pacman import Pacman
import math

class Ghost:
    def __init__(self, x: int, y: int, color: int, speed: int = 1):
        """
        Initialize the Ghost's attributes.
        :param x: Initial x-coordinate of the Ghost.
        :param y: Initial y-coordinate of the Ghost.
        :param color: Color of the Ghost (used to select its sprite).
        :param speed: Speed at which the Ghost moves (default is 1).
        """
        self.x = x
        self.y = y
        self.color = color
        self._speed = speed  # Use setter to control speed (optional)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.state = "normal"  # Can be "normal" or "frightened"
        self.image = 0  # Placeholder for image reference, could be used later for sprite rendering
        self.animation_speed = 1
        self.animation_frame = 0

    # Property for position (getter and setter)
    @property
    def position(self):
        return (self.x, self.y)

    @position.setter
    def position(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            self.x, self.y = value
        else:
            raise ValueError("Position must be a tuple with x and y coordinates.")

    # Property for speed (setter and getter)
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value > 0:
            self._speed = value
        else:
            raise ValueError("Speed must be positive.")

    def update(self, pacman_x: int, pacman_y: int):
    def update(self, pacman_x, pacman_y):
        self.move(pacman_x, pacman_y)
        self.update_animation_ghost()  # Asegúrate de que esto se llame aquí
        self.map_limits()
    def update_animation_ghost(self):
        """
        Avanza el frame de animación automáticamente.
        """
        if pyxel.frame_count % 10 == 0:  # Cambia de frame cada 10 frames
            self.animation_frame = (self.animation_frame + 1) % 2
        # Calcula `u` según la dirección
        if self.direction == "right":
            self.image = self.animation_frame * 16
        elif self.direction == "left":
            self.image = 32 + self.animation_frame * 16
        elif self.direction == "up":
            self.image = 64 + self.animation_frame * 16
        elif self.direction == "down":
            self.image = 96 + self.animation_frame * 16
    def map_limits(self):
        if self.x < -16:
            self.x = 256
        if self.x > 256:
            self.x = -16
        if self.y < -16:
            self.y = 256
        if self.y > 256:
            self.y = -16
    def updatefrightened(self, pacman_x: int, pacman_y: int):
        """
        Update the ghost's behavior. If frightened, it moves randomly, else it chases Pac-Man.
        :param pacman_x: x-coordinate of Pac-Man.
        :param pacman_y: y-coordinate of Pac-Man.
        """
        if self.state == "frightened":
            self.frightened_move()
        else:
            self.move(pacman_x, pacman_y)

    def draw(self):
        """
        Draw the ghost using Pyxel's blt function.
        """
        pyxel.blt(self.x, self.y, 0, self.color * 16, 0, 16, 16, 0)
        pyxel.blt(self.x, self.y, 1, self.image, 0, 16, 16, 0)

    def move(self, pacman_x: int, pacman_y: int):
        """
        General movement logic for the ghost.
        :param pacman_x: x-coordinate of Pac-Man.
        :param pacman_y: y-coordinate of Pac-Man.
        """
        # Move based on current direction
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

        self.change_direction(pacman_x, pacman_y)

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