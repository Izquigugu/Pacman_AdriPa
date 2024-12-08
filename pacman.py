import pyxel
from board import BoardItem, TILE_SIZE
from music import PyxelSounds
class Pacman:
    def __init__(self, board, points, lives):
        """
        Initialize Pac-Man's attributes.
        :param board: The game board where Pac-Man will move.
        :param points: The points system to track the score.
        :param lives: The lives system to track Pac-Man's remaining lives.
        """
        # Positioning Pac-Man based on the board grid
        self.x = board.pacman_grid_x * TILE_SIZE
        self.y = board.pacman_grid_y * TILE_SIZE
        # Tile position (grid-based coordinates)
        self.tile_x = int(self.x / TILE_SIZE)
        self.tile_y = int(self.y / TILE_SIZE)
        # Game board and state tracking
        self.board = board
        self.points = points
        self.lives = lives
        self.alive = True
        # Sprite-related attributes
        self.image = 0
        self.powered = False
        self.powered_timer = 0
        self.resetting = False
        self.eating = False
        self.reset_timer = 0
        self.eating_timer = 0
        # Movement attributes
        self.velocity = 2
        self.direction = 0
        # Animation attributes
        self.animation_frame = 0
        self.animation_speed = 1
        # Sounds and collision
        self.pyxel_sounds = PyxelSounds()
        self.collided_ghost = None

    def update(self, ghosts):
        """
        Update Pac-Man's behavior each frame:
        - Handle movement, animations, map limits, and collisions.
        :param ghosts: List of ghost objects in the game.
        """
        self.move()
        self.update_animation_pacman()
        self.map_limits()
        self.check_dot_collision()
        self.handle_powered_state()
        # Check for ghost collision
        self.collided_ghost = self.check_ghost_collision(ghosts)
        if (self.collided_ghost is not None and not self.resetting and not
                self.powered):
            # Pac-Man collided with a ghost and is not powered
            self.resetting = True
            self.reset_timer = 100
            self.lives.lose_lives()
            self.animation_frame = 4
            print(f"Colisión con: {type(self.collided_ghost).__name__}")

        if (self.collided_ghost is not None and not self.resetting and
                self.powered):
            # Pac-Man collided with a ghost while in powered-up state
            self.eating = True
            self.eating_timer = 70
            self.points.sum_points(200)
            self.collided_ghost.eaten = True
            self.collided_ghost.scared = False

    def draw(self):
        """
           Draw Pac-Man on the screen using the correct animation frame and direction.
           """
        if self.resetting: # During reset, use frames 7 to 14
            u = self.animation_frame * 16
        else:# Normal animation
            u = self.animation_frame * 16
        v = self.direction * 16 # Select the row of sprites based on direction
        pyxel.blt(self.x, self.y, 0, u, v, 16, 16, 0) # Draw Pac-Man

    def check_ghost_collision(self, ghosts):
        """
               Check for collisions between Pac-Man and any ghosts.
               :param ghosts: List of ghost objects.
               :return: Ghost object if collision is detected, else None.
               """
        pacman_centre_x = self.x + 8
        pacman_centre_y = self.y + 8
        for ghost in ghosts:
            if abs(pacman_centre_x - (ghost.x + 8)) < 8 and abs(
                    pacman_centre_y - (ghost.y + 8)) < 8:
                return ghost # Return the collided ghost
        return None # No collision detected

    def can_move_to(self, new_x, new_y):
        """
           Check if Pac-Man can move to a new position without colliding with walls.
           :param new_x: Target x-coordinate.
           :param new_y: Target y-coordinate.
           :return: True if movement is allowed, False otherwise.
           """
        # Sprite dimensions
        pacman_width = 16
        pacman_height = 16

        # Calculate Pac-Man's collision corners and midpoints
        left_tile_x = int(new_x / TILE_SIZE)
        mid_left_tile_x = int((new_x + 8) / TILE_SIZE)
        right_tile_x = int((new_x + pacman_width - 1) / TILE_SIZE)
        mid_right_tile_x = int((new_x + pacman_width/2 - 1) / TILE_SIZE)
        top_tile_y = int(new_y / TILE_SIZE)
        mid_top_tile_y = int((new_y + 8) / TILE_SIZE)
        bottom_tile_y = int((new_y + pacman_height - 1) / TILE_SIZE)
        mid_bottom_tile_y = int((new_y + pacman_height/2 - 1) / TILE_SIZE)

        # Handle screen teleportation
        max_x = len(self.board.board_map[0])
        max_y = len(self.board.board_map)

        # Handle screen teleportation
        left_tile_x %= max_x
        right_tile_x %= max_x
        top_tile_y %= max_y
        bottom_tile_y %= max_y
        mid_left_tile_x %= max_x
        mid_right_tile_x %= max_x
        mid_top_tile_y %= max_y
        mid_bottom_tile_y %= max_y

        # Check for collisions with walls
        if (
                self.board.board_map[top_tile_y][left_tile_x] == BoardItem.WALL
                or self.board.board_map[top_tile_y][mid_left_tile_x] ==
                BoardItem.WALL or self.board.board_map[mid_top_tile_y][
            left_tile_x] == BoardItem.WALL or self.board.board_map[top_tile_y][
            right_tile_x] == BoardItem.WALL or self.board.board_map[top_tile_y][
            mid_right_tile_x] == BoardItem.WALL or self.board.board_map[
            mid_top_tile_y][
            right_tile_x] == BoardItem.WALL
                or self.board.board_map[bottom_tile_y][
            left_tile_x] == BoardItem.WALL or self.board.board_map[bottom_tile_y][
            mid_left_tile_x] == BoardItem.WALL or self.board.board_map[
            mid_bottom_tile_y][
            left_tile_x] == BoardItem.WALL
                or self.board.board_map[bottom_tile_y][
            right_tile_x] == BoardItem.WALL or self.board.board_map[bottom_tile_y][
            mid_right_tile_x] == BoardItem.WALL or self.board.board_map[
            mid_bottom_tile_y][
            right_tile_x] == BoardItem.WALL
        ):
            return False
        return True

    def move(self):
        """
        Handle Pac-Man's movement based on key inputs.
        """
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
        """
        Handle screen teleportation when Pac-Man crosses map boundaries.
        """
        map_width = len(self.board.board_map[0]) * TILE_SIZE
        map_height = len(self.board.board_map) * TILE_SIZE

        if self.x < -16:
            self.x = map_width
        elif self.x >= map_width:
            self.x = -16

        if self.y < -16:
            self.y = map_height
        elif self.y >= map_height:
            self.y = -16

    def update_animation_pacman(self):
        """
        Recharge the frame animation.
        """
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

    def resetting_animation(self): # 7 al 14
        """
        Recharge the frame animation.
        """
        if pyxel.frame_count % 5 == 0:
            self.animation_frame += 1

        if self.animation_frame > 15:
            self.animation_frame = 15


    def check_dot_collision(self):
        """
        Check for collisions with dots and power-ups on the board.
        """
        self.tile_x = int(self.x / TILE_SIZE)
        self.tile_y = int(self.y / TILE_SIZE)

        if self.board.tilemap.pget(self.tile_x, self.tile_y) == BoardItem.DOTS:
            # Se elimina el dot de la pantalla y se elimina un dot de la
            # lista self.board.dots[].
            self.board.tilemap.pset(self.tile_x, self.tile_y,
                                    BoardItem.EMPTY_SPACE)
            self.board.dots.pop()
            self.points.sum_points(10)
            self.pyxel_sounds.play_eat_dot_sound()

        # Colisión con los powerups
        if (self.board.tilemap.pget(self.tile_x, self.tile_y) ==
                BoardItem.POWERUP):
            self.board.tilemap.pset(self.tile_x, self.tile_y, BoardItem.EMPTY_SPACE)
            self.points.sum_points(50)
            self.pyxel_sounds.play_eat_dot_sound()
            #print(f"Se activó un powerup!")
            self.powered = True
            self.powered_timer += (10 * 30)

    def handle_powered_state(self):
        """
        Manage the powered-up state timer.
        """
        if self.powered:
            self.powered_timer -= 1
            if self.powered_timer <= 0:
                self.powered = False
                self.powered_timer = 0

    def reset(self, board, points):
        """
        Resets Everything
        """
        self.x = board.pacman_grid_x * TILE_SIZE
        self.y = board.pacman_grid_y * TILE_SIZE
        self.tile_x = int(self.x / TILE_SIZE)
        self.tile_y = int(self.y / TILE_SIZE)
        self.board = board
        self.points = points
        self.alive = True
        self.image = 0
        self.powered = False
        self.powered_timer = 0
        self.velocity = 2
        self.direction = 0
        self.animation_frame = 0
        self.animation_speed = 1



