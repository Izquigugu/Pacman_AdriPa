class Ghost:
    def __init__(self, x, y, color="Red", velocity=1,):
        """
        Initialize the Ghost's attributes.
        :param x: Initial x-coordinate of the Ghost.
        :param y: Initial y-coordinate of the Ghost.
        :param color: Color of the Ghost (default is "Red").
        :param velocity: The speed at which the Ghost moves (default is 1).
        """
        self.x = x
        self.y = y
        self.color = color
        self.state = "normal"  # Can be "normal" or "vulnerable"
        self.velocity = velocity

    # Property for position
    @property
    def position(self):
        return (self.x, self.y)

    # Property for velocity
    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if value > 0:
            self._velocity = value
        else:
            raise ValueError("Velocity must be a positive number.")

    # Method to move the Ghost
    def move(self, direction):
        """
        Move the Ghost based on the given direction and velocity.
        :param direction: Direction to move ("UP", "DOWN", "LEFT", "RIGHT").
        """
        if direction == "UP":
            self.y -= self.velocity
        elif direction == "DOWN":
            self.y += self.velocity
        elif direction == "LEFT":
            self.x -= self.velocity
        elif direction == "RIGHT":
            self.x += self.velocity

    # Method to make the Ghost vulnerable
    def become_vulnerable(self):
        """
        Changes the Ghost's state to "vulnerable".
        """
        self.state = "vulnerable"
        print(f"The {self.color} ghost is now vulnerable!")

    # Method to reset the Ghost to normal
    def reset_state(self):
        """
        Resets the Ghost's state to "normal".
        """
        self.state = "normal"
        print(f"The {self.color} ghost is back to normal!")

    # String representation of the Ghost
    def __str__(self):
        return (f"Ghost: Color={self.color}, Position={self.position}, "
                f"State={self.state}, Velocity={self.velocity}")