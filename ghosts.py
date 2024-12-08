import pyxel
import random
import math
from board import BoardItem, TILE_SIZE

class Ghost:
    def __init__(self, x: int, y: int, board, speed: int = 1, sprite_v: int = 0):
        """
        Initialize the Ghost's attributes.
        :param x: Initial x-coordinate of the ghost on the screen.
        :param y: Initial y-coordinate of the ghost on the screen.
        :param board: The game board to check collision and movement.
        :param speed: Speed at which the ghost moves.
        :param sprite_v: Sprite version to determine the ghost's color.
        """
        self.x = x # Ghost's position on the x-axis
        self.y = y # Ghost's position on the y-axis
        self.board = board # Reference to the game board
        self._speed = speed # Ghost's speed, default is 1
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.u = 0 # Horizontal sprite coordinate (for animation)
        self.v = sprite_v # Vertical sprite coordinate (for ghost color)
        self.v_scared = 80 # Sprite coordinate for scared ghost
        self.v_eaten = 64 # Sprite coordinate for ghost when eaten
        self.scared = False # Ghost's frightened state
        self.eaten = False # Ghost's eaten state
        self.animation_frame = 0 # Animation frame for the ghost

    def reset(self, x: int, y: int, board, speed: int = 1, sprite_v: int = 0):
        """
        Reset the ghost's attributes after it is eaten or when a new game starts.
        :param x: New x-coordinate.
        :param y: New y-coordinate.
        :param board: The game board to check collision and movement.
        :param speed: New speed for the ghost.
        :param sprite_v: Sprite version for the ghost's color.
        """
        self.x = x
        self.y = y
        self.board = board
        self._speed = speed
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.u = 0
        self.v = sprite_v  # para determinar el color de cada fantasma
        self.animation_frame = 0

    def update(self, powered, powered_timer):
        """
        Update ghost's behavior based on its state.
        :param powered: Boolean indicating if Pac-Man is powered-up.
        :param powered_timer: Timer for how long Pac-Man stays powered-up.
        """
        if powered:
            self.scared = True
        else:
            self.scared = False
        if self.scared:
            self.update_scared_animation(powered_timer)
        elif self.eaten:
            self.eaten_animation()
        else:
            self.update_animation_ghost()

        self.move()
        self.map_limits()
        self.change_direction()

    def eaten_movement(self):
        """
        Handle movement for the ghost when it is eaten.
        """
        if self.x < 128:
            self.x += 3
        if self.y < 120:
            self.y += 3
        if self.x > 128:
            self.x -= 3
        if self.y > 120:
            self.y -= 3

    def eaten_animation(self):
        """
        Set the animation frame for the ghost when it is eaten.
        """
        if self.direction == "right":
            self.u = 0 * 16
        elif self.direction == "left":
            self.u = 1 * 16
        elif self.direction == "up":
            self.u = 2 * 16
        elif self.direction == "down":
            self.u = 3 * 16

    def draw(self):
        """
        Draw the ghost on the screen, accounting for its state (scared, eaten, or normal).
        """
        if self.scared:
            pyxel.blt(self.x, self.y, 1, self.u, self.v_scared, 16, 16, 0)
        elif self.eaten:
            pyxel.blt(self.x, self.y, 1, self.u, self.v_eaten, 16, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 1, self.u, self.v, 16, 16, 0)

    def can_move_to(self, new_x, new_y):
        """
        Check if the ghost can move to the new position (no collision with walls).
        :param new_x: New x-coordinate.
        :param new_y: New y-coordinate.
        :return: True if the move is valid (no wall), False otherwise.
        """
        # Dimensions of the ghost sprite (16x16 pixels)
        ghost_width = 16
        ghost_height = 16

        # Calculate corners and midpoints of the sprite to avoid bugs
        left_tile_x = int(new_x / TILE_SIZE)
        mid_left_tile_x = int((new_x + 8) / TILE_SIZE)
        right_tile_x = int((new_x + ghost_width - 1) / TILE_SIZE)
        mid_right_tile_x = int((new_x + ghost_width / 2 - 1) / TILE_SIZE)
        top_tile_y = int(new_y / TILE_SIZE)
        mid_top_tile_y = int((new_y + 8) / TILE_SIZE)
        bottom_tile_y = int((new_y + ghost_height - 1) / TILE_SIZE)
        mid_bottom_tile_y = int((new_y + ghost_height / 2 - 1) / TILE_SIZE)

        # Ensure the indices are within the bounds of the map
        max_x = len(self.board.board_map[0])
        max_y = len(self.board.board_map)

        # Handle teleportation: wrap around when crossing map boundaries
        left_tile_x %= max_x
        right_tile_x %= max_x
        top_tile_y %= max_y
        bottom_tile_y %= max_y
        mid_left_tile_x %= max_x
        mid_right_tile_x %= max_x
        mid_top_tile_y %= max_y
        mid_bottom_tile_y %= max_y

        # Check if any corner of the ghost's sprite touches a wall
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

    def move_towards(self, target_x, target_y):
        """Move ghost towards a target (e.g., Pac-Man)."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.x += self._speed * (dx / distance)
            self.y += self._speed * (dy / distance)

    def move(self):
        """
        Handle movement based on the current direction.
        """
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
        Update the ghost's animation frames for movement.
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

    def update_scared_animation(self, powered_timer):
        """
        Update the ghost's animation when it is frightened (blinking effect).
        """
        if pyxel.frame_count % 10 == 0:
            self.animation_frame = (self.animation_frame + 1) % 2

        if powered_timer <= (3 * 30):
            if pyxel.frame_count % 20 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                self.u = (self.animation_frame * 16) + 32
            else:
                self.u = self.animation_frame * 16
        else:
            self.u = self.animation_frame * 16

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
    def __init__(self, x, y, board):
        super().__init__(x, y, board, speed=1, sprite_v=0)

    def chase_pacman(self, pacman_x, pacman_y):
        """
        It chases Pacman by choosing the best direction to go, taking into
        account the walls in the map.
        """
        best_direction = None
        min_distance = float("inf")

        possible_moves = {
            "up": (self.x, self.y - self._speed),
            "down": (self.x, self.y + self._speed),
            "left": (self.x - self._speed, self.y),
            "right": (self.x + self._speed, self.y),
        }

        for direction, (new_x, new_y) in possible_moves.items():
            if self.can_move_to(new_x, new_y):
                distance = math.hypot(pacman_x - new_x, pacman_y - new_y)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction

        if best_direction is not None:
            self.direction = best_direction

    def update(self, pacman_x, pacman_y, powered, powered_timer):
        """
        Depending on the state in which the ghost is, it behaves differently.
        """
        if powered:
            self.scared = True
        else:
            self.scared = False

        if self.scared:
            self.update_scared_animation(powered_timer)
        elif self.eaten:
            self.eaten_animation()
        else:
            self.update_animation_ghost()
            self.chase_pacman(pacman_x, pacman_y)  # Sigue a Pac-Man

        self.move()
        self.map_limits()

class Pinky(Ghost):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, speed=1, sprite_v=16)

    def anticipate_pacman(self, pacman_x, pacman_y, pacman_direction):
        """
        This method works similarly as the chasing one, but it goes to a
        tile in front of Pacman.
        """
        anticipation_distance = TILE_SIZE * 6

        if pacman_direction == 2:
            target_x, target_y = pacman_x, pacman_y - anticipation_distance
        elif pacman_direction == 3:
            target_x, target_y = pacman_x, pacman_y + anticipation_distance
        elif pacman_direction == 1:
            target_x, target_y = pacman_x - anticipation_distance, pacman_y
        elif pacman_direction == 0:
            target_x, target_y = pacman_x + anticipation_distance, pacman_y
        else:
            target_x, target_y = pacman_x, pacman_y

        best_direction = None
        min_distance = float("inf")

        possible_moves = {
            "up": (self.x, self.y - self._speed),
            "down": (self.x, self.y + self._speed),
            "left": (self.x - self._speed, self.y),
            "right": (self.x + self._speed, self.y),
        }

        for direction, (new_x, new_y) in possible_moves.items():
            if self.can_move_to(new_x, new_y):
                distance = math.hypot(target_x - new_x, target_y - new_y)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction

        if best_direction is not None:
            self.direction = best_direction

    def update(self, pacman_x, pacman_y, pacman_direction, powered,
               powered_timer):
        """
        This method makes the position update
        """
        if powered:
            self.scared = True
        else:
            self.scared = False

        if self.scared:
            self.update_scared_animation(powered_timer)
        elif self.eaten:
            self.eaten_animation()
        else:
            self.update_animation_ghost()
            self.anticipate_pacman(pacman_x, pacman_y,
                                   pacman_direction)  # Anticipa a Pac-Man

        self.move()
        self.map_limits()

class Inky(Ghost):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, speed=1, sprite_v=32)

class Clyde(Ghost):
    def __init__(self, x, y, board):
        super().__init__(x, y, board, speed=1, sprite_v=48)