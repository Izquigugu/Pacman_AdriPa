import pyxel

# Class for managing the player's lives in the game
class Lives:
    # Predefined positions on the map for displaying the lives count in different levels
    MAP_POSITIONS_X = [210, 214, 164] # X-coordinates for different levels
    MAP_POSITIONS_Y = [101, 10, 6] # Y-coordinates for different levels
    def __init__(self):
        """
        Initialize the Lives object with the starting values for lives and position.
        """
        self.lives = 3 # Player starts with 3 lives
        self.x = 210 # Initial X position to display lives
        self.y = 101 # Initial Y position to display lives
        self.text = f"Lives: {self.lives}"  # Text showing the number of lives

    def update(self):
        """
        Update the text for lives whenever it changes.
        """
        self.text = f"Lives: {self.lives}" # Update the displayed text with current lives

    def draw(self):
        """
        Draw the lives count on the screen at the specified coordinates.
        """
        pyxel.text(self.x, self.y, self.text, pyxel.COLOR_WHITE)

    def lose_lives(self):
        """
        Decrease the number of lives when the player loses a life.
        """
        self.lives -= 1

    def change_lives_position(self, tilemap_num):
        """
        Change the position of the lives counter based on the level number (tilemap_num).
        """
        self.x = self.MAP_POSITIONS_X[tilemap_num]
        self.y = self.MAP_POSITIONS_Y[tilemap_num]

# Class for managing the player's points in the game
class Points:
    # Predefined positions on the map for displaying the points count in different levels
    MAP_POSITIONS_X = [5, 4, 58] # X-coordinates for different levels
    MAP_POSITIONS_Y = [101, 10, 6] # Y-coordinates for different levels
    def __init__(self):
        """
        Initialize the Points object with the starting value for points and position.
        """
        self.points = 0 # Player starts with 0 points
        self.x = 5 # Initial X position to display points
        self.y = 101 # Initial Y position to display points
        self.text = f"Points: {self.points}"  # Text showing the number of points

    def update(self):
        """
        Update the text for points whenever it changes.
        """
        self.text = f"Points: {self.points}" # Update the displayed text
        # with current points

    def draw(self):
        """
        Draw the points count on the screen at the specified coordinates.
        """
        pyxel.text(self.x, self.y, self.text, pyxel.COLOR_WHITE)

    def sum_points(self, sum_points):
        """
        Add points to the total score.
        :param sum_points: The number of points to add.
        """
        self.points += sum_points

    def change_points_position(self, tilemap_num):
        """
        Change the position of the points counter based on the level number (tilemap_num).
        """
        self.x = self.MAP_POSITIONS_X[tilemap_num]
        self.y = self.MAP_POSITIONS_Y[tilemap_num]

