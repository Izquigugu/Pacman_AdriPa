import pyxel
from dots import Dot # Import the Dot class for managing dot objects

# Constants for tile dimensions and sprite bank
TILE_SIZE = 8 # Each tile in the map is 8x8 pixels
SPRITE_BANK = 2 # Sprite bank where board elements are stored

class BoardItem:
    WALL = (2, 8) # Wall tile located at (2, 8) in the sprite bank
    EMPTY_SPACE = (3, 8) # Empty space tile at (3, 8)
    GHOSTS_DOOR = (4, 8) # Door for the ghosts at (4, 8)
    PACMAN = (5, 8) # Starting position for Pac-Man at (5, 8)
    DOTS = (6,8) # Regular dots tile located at (6, 8)
    POWERUP = (7, 8) # Power-up tile located at (7, 8)
"""
This class defines the game board where all the gameplay happens.
It reads from a Pyxel tilemap to create the game layout.
"""

class Board:
    # Board dimensions (in tiles)
    HEIGHT = 32 # Board height: 32 tiles
    WIDTH = 32 # Board width: 32 tiles

    def __init__(self, tilemap):
        self.tilemap = tilemap # The tilemap containing the board structure
        self.board_map = [] # 2D list to store the logical representation of the board
        self.dots = [] # List to store all the dot objects (small points)
        self.pacman_grid_x = 0 # Pac-Man's starting x position in grid coordinates
        self.pacman_grid_y = 0 # Pac-Man's starting y position in grid coordinates

        # Loop through each tile on the board to initialize its content
        for y in range(self.HEIGHT): # Iterate through rows
            self.board_map.append([]) # Create a new row in the board map
            for x in range(self.WIDTH): # Iterate through columns
                # Retrieve the type of tile at the current (x, y) position
                # Check the type of tile and update the board_map accordingly
                if self.tilemap.pget(x, y) == BoardItem.WALL:
                    # If it's a dot, append DOTS to the board map
                    self.board_map[y].append(BoardItem.WALL)
                elif self.tilemap.pget(x, y) == BoardItem.DOTS:
                    self.board_map[y].append(BoardItem.DOTS)
                    # Add a Dot object to the dots list at the correct position
                    self.dots.append(Dot(x * 16, y * 16))
                elif self.tilemap.pget(x, y) == BoardItem.POWERUP:
                    # If it's a power-up, append POWERUP to the board map
                    self.board_map[y].append(BoardItem.POWERUP)
                elif self.tilemap.pget(x, y) == BoardItem.GHOSTS_DOOR:
                    # If it's a ghost door, append GHOSTS_DOOR to the board map
                    self.board_map[y].append(BoardItem.GHOSTS_DOOR)
                elif self.tilemap.pget(x, y) == BoardItem.PACMAN:
                    # If it's Pac-Man's starting position:
                    # Replace it with an EMPTY_SPACE in the board map
                    self.board_map[y].append(BoardItem.EMPTY_SPACE)
                    # Save Pac-Man's starting grid coordinates
                    self.pacman_grid_x = x
                    self.pacman_grid_y = y
                else:
                    # For all other tiles, consider them as EMPTY_SPACE
                    self.board_map[y].append(BoardItem.EMPTY_SPACE)

    def draw(self):
        """
        Draw the game board on the screen.
        This method uses Pyxel's `bltm` function to render the tilemap.
        """
        pyxel.bltm(0, 0, self.tilemap, 0, 0, self.WIDTH * TILE_SIZE,
                   self.HEIGHT * TILE_SIZE)


