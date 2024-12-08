import pyxel
from board import Board,TILE_SIZE
# Importing the Board class and TILE_SIZE constant
from pacman import Pacman
# Importing Pacman class
from ghosts import Blinky, Pinky, Inky, Clyde
# Importing specific ghost classes
from music import PyxelSounds
# Importing PyxelSounds class to handle music and sound effects
from game import Lives, Points
# Importing Lives and Points classes for game progress


class App:
    # Constants for different levels
    LEVELS = [0, 1, 2]  # List of level indices for the different maps
    HEIGHT = 32  # Board height
    WIDTH = 32  # Board width

    def __init__(self):
        # Initializes the game window (256x256) and loads assets from pyxres file
        pyxel.init(256, 256)
        pyxel.load("assets/resources.pyxres")

        self.current_level = 0  # Start with the first level
        self.points = Points()  # Create Points object to track player's points
        self.lives = Lives()  # Create Lives object to track remaining lives
        self.load_level(self.current_level)  # Load the first level
        self.sounds = PyxelSounds()  # Initialize sound system

        # Run the main game loop, calling update() and draw()
        pyxel.run(self.update, self.draw)

    def update(self):
        """
        Update game state. This includes handling user input, checking collisions,
        updating game objects, and progressing through levels.
        """
        # Quit the game when Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            self.sounds.stop_music()  # Stop music
            pyxel.quit()  # Exit the game

        # If Pac-Man is resetting after a collision with a ghost
        if self.pacman.resetting:
            self.pacman.reset_timer -= 1
            # If Pac-Man is in reset state, show reset animation
            if 0 < self.pacman.reset_timer < 70:
                self.pacman.resetting_animation()
            # Once the reset timer is finished, reset positions or end the game if lives are over
            if self.pacman.reset_timer <= 0:
                self.reset_positions()
                if self.lives.lives <= 0:  # Game over if no lives are left
                    pyxel.quit()
                self.pacman.resetting = False  # End resetting state
            return  # Skip other updates while resetting

        # If Pac-Man is eating a ghost
        if self.pacman.eating:
            self.pacman.eating_timer -= 1
            if self.pacman.eating_timer <= 50:
                self.pacman.collided_ghost.eaten_movement()  # Move eaten ghost
            if self.pacman.eating_timer <= 0:
                self.pacman.collided_ghost.eaten = False  # Mark ghost as not eaten
                self.pacman.eating = False  # End the eating state
            return  # Skip other updates while Pac-Man is eating a ghost

        # Update sounds based on whether Pac-Man is powered up
        self.sounds.update(self.pacman.powered)

        # Update ghost behavior based on Pac-Man's state
        for ghost in self.ghosts:
            if isinstance(ghost, Blinky):
                # Blinky chases Pac-Man
                ghost.update(self.pacman.x, self.pacman.y, self.pacman.powered,
                             self.pacman.powered_timer)
            elif isinstance(ghost, Pinky):
                # Pinky predicts Pac-Man's next move
                ghost.update(self.pacman.x, self.pacman.y,
                             self.pacman.direction, self.pacman.powered,
                             self.pacman.powered_timer)
            else:
                # Inky and Clyde move based on other behaviors
                ghost.update(self.pacman.powered, self.pacman.powered_timer)

        # Update Pac-Man's behavior and state
        self.pacman.update(self.ghosts)
        self.points.update()  # Update points display
        self.lives.update()  # Update lives display

        # Proceed to the next level if all dots are collected
        if len(self.board.dots) == 0:
            self.next_level()

    def draw(self):
        """
        Draw game state to the screen.
        """
        pyxel.cls(0)  # Clear screen with background color
        self.board.draw()  # Draw the board
        if self.current_level < len(
                self.LEVELS):  # Draw game objects if the current level is valid
            self.pacman.draw()  # Draw Pac-Man
            if not self.pacman.resetting or self.pacman.reset_timer > 80:
                # Draw ghosts only if Pac-Man is not resetting
                for ghost in self.ghosts:
                    ghost.draw()
        # Draw lives and points on the screen
        self.lives.draw()
        self.points.draw()

    def load_level(self, level_index):
        """
        Load the game board, Pac-Man, and ghosts for the specified level.
        :param level_index: Index of the current level.
        """
        self.board = Board(pyxel.tilemap(
            self.LEVELS[level_index]))  # Load board based on level
        self.pacman = Pacman(self.board, self.points,
                             self.lives)  # Create Pac-Man object
        # Create ghosts (Blinky, Pinky, Inky, Clyde) at the starting position
        self.ghosts = [Blinky(128, 120, self.board),
                       Pinky(128, 120, self.board),
                       Inky(128, 120, self.board),
                       Clyde(128, 120, self.board)]
        self.points.change_points_position(
            level_index)  # Adjust points display position for this level
        self.lives.change_lives_position(
            level_index)  # Adjust lives display position for this level

    def next_level(self):
        """
        Progress to the next level.
        """
        self.current_level += 1
        if self.current_level < len(self.LEVELS):
            self.load_level(self.current_level)  # Load the next level
        else:
            print(
                "¡Game completed!")  # If no more levels, print game completed message
            self.sounds.stop_music()  # Stop music
            self.board = Board(
                pyxel.tilemap(3))  # Load final board (game over or completed)

    def reset_positions(self):
        """
        Reset positions of Pac-Man and all ghosts to their starting points.
        """
        self.pacman.reset(self.board, self.points)
        self.ghosts[0].reset(128, 120, self.board, speed=1,
                             sprite_v=0)  # Reset Blinky
        self.ghosts[1].reset(128, 120, self.board, speed=1,
                             sprite_v=16)  # Reset Pinky
        self.ghosts[2].reset(128, 120, self.board, speed=1,
                             sprite_v=32)  # Reset Inky
        self.ghosts[3].reset(128, 120, self.board, speed=2,
                             sprite_v=48)  # Reset Clyde


App()  # Run the game
