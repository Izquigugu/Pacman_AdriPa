import pyxel
import random
import time


class Dot:
    def __init__(self, x: int, y: int):
        """
        Initialize the Dot's attributes.
        :param x: x-coordinate of the dot on the screen.
        :param y: y-coordinate of the dot on the screen.
        :param is_big: If True, this is a big dot (power pellet), otherwise a small dot.
        """
        self.x = x
        self.y = y
        self.is_big = False
        self.collected = False  # To track if the dot is collected by Pac-Man

    def collect(self):
        """
        Marks the dot as collected.
        """
        self.collected = True

    def draw(self):
        if not self.collected:
            pyxel.blt(self.x, self.y, 2, 48, 64, 8, 8, 0)
        """
        Draw the dot on the screen.
        """
        #if not self.collected:
            #if self.is_big:
                #pyxel.blt(self.x, self.y, 0, 16, 0, 8, 8, 0)  # Big dot (
        # power pellet)
           # else:
        #pyxel.blt(self.x, self.y, 2, 6 , 8
                #  , 8, 8,
                 # 0)  # Small
        # dot


"""class GameDots:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.load("assets/resources.pyxres")
        self.board = Board(pyxel.tilemap(0))  # Assuming you already have the Board class
        self.pacman = Pacman(200, 150, False)
        self.dots = self.create_dots()
        self.stage = 1
        self.game_over = False

        pyxel.run(self.update, self.draw)"""

"""def create_dots(self):
        
        Create the dots for each stage (small and big).
        
        dots = []
        for y in range(self.board.HEIGHT):
            for x in range(self.board.WIDTH):
                if self.board.board_map[y][x] == BoardItem.EMPTY_SPACE:
                    if random.random() < 0.1:  # 10% chance to spawn a big dot (power pellet)
                        dots.append(Dot(x * 8, y * 8, is_big=True))
                    else:
                        dots.append(Dot(x * 8, y * 8, is_big=False))
        return dots"""

"""def update(self):
        
        Update the game state: Pac-Man moves, collects dots, and checks for game progression.
        
        if not self.game_over:
            self.pacman.update()
            self.check_dot_collisions()

            # Check if all dots are collected, and progress to the next stage
            if all(dot.collected for dot in self.dots):
                self.progress_to_next_stage()"""

"""def check_dot_collisions(self):
        """
      #  Check if Pac-Man collects any dot.
"""
        for dot in self.dots:
            if not dot.collected:
                if abs(self.pacman.x - dot.x) < 8 and abs(self.pacman.y - dot.y) < 8:
                    dot.collect()

    def progress_to_next_stage(self):
        """
       # Move to the next stage if all dots are collected.
"""
        if self.stage < 3:  # Assuming there are 3 stages
            self.stage += 1
            self.dots = self.create_dots()  # Create new dots for the next stage
            self.pacman.reset_position()  # Reset Pac-Man's position for the new stage
        else:
            self.game_over = True  # Game ends after the 3rd stage

    def draw(self):
        """
       # Draw everything on the screen.
"""
        pyxel.cls(0)
        self.board.draw()  # Draw the board (walls, empty space, etc.)
        self.pacman.draw()
        for dot in self.dots:
            dot.draw()
        self.draw_score()

    def draw_score(self):
        """
       # Display the current score and stage.
"""
        pyxel.text(5, 5, f"Score: {self.pacman.score}", pyxel.COLOR_WHITE)
        pyxel.text(5, 15, f"Stage: {self.stage}", pyxel.COLOR_WHITE)"""