import pyxel


class Pacman:
    def __init__(self, x: int, y: int, image, powered: bool):
        self.x = x
        self.y = y
        self.alive = True
        self.image = image
        self.powered = powered
        self.velocity = 1

    @property
    def x(self) -> int:
        return self.__x
    @x.setter
    def  x(self, x):
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y
    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def alive(self) -> bool:
        return self.__alive
    @alive.setter
    def alive(self, alive):
        self.__alive = alive
    # Crear property de image
    @property
    def powered(self) -> bool:
        return self.__powered
    @powered.setter
    def powered(self, powered):
        self.__powered = powered

    def move(self):
        if pyxel.btn(pyxel.KEY_W):
            self.y -= self.velocity
        if pyxel.btn(pyxel.KEY_S):
            self.y += self.velocity
        if pyxel.btn(pyxel.KEY_A):
            self.x -= self.velocity
        if pyxel.btn(pyxel.KEY_D):
            self.x += self.velocity






