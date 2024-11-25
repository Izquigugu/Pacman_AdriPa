import random

from pyxel.pyxel_wrapper import image


class Ghost:
    """this class will have the attributes of different ghosts"""
    def__init__(self, x, y, image):

        self.x = x
        self.y = y
        self.alive = True
        self.image = image
        coin = random.randint(0,1)
        if coin == 0:
            self.blinking = False
        else:
            self.blinking = True

    @property
    def x(self) -> int:
        return self.__x
    @property
    def alive(self) -> bool:
        return self.__alive
    @property
    def image(self) -> str:
        return self.__image:
    @property
    def
