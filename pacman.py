import pyxel

class Pacman:
    def __init__(self, x: int, y: int, powered: bool):
        self.x = x
        self.y = y
        self.alive = True
        self.image = 0
        self.powered = powered
        self.velocity = 2
        self.direction = 0
        self.animation_frame = 0
        self.animation_speed = 1

    def update(self):
        self.move()
        self.update_animation()
        self.map_limits()

    def draw(self):
        u = self.animation_frame * 16
        v = self.direction * 16
        pyxel.blt(self.x, self.y, 0, u, v, 16, 16)


    def move(self):
        if pyxel.btn(pyxel.KEY_W):
            self.y -= self.velocity
            self.direction = 2
        elif pyxel.btn(pyxel.KEY_S):
            self.y += self.velocity
            self.direction = 3
        elif pyxel.btn(pyxel.KEY_A):
            self.x -= self.velocity
            self.direction = 1
        elif pyxel.btn(pyxel.KEY_D):
            self.x += self.velocity
            self.direction = 0

    def map_limits(self):
        if self.x < -16:
            self.x = 400
        if self.x > 400:
            self.x = -16
        if self.y < -16:
            self.y = 300
        if self.y > 300:
            self.y = -16


    def update_animation(self):
        if (pyxel.btn(pyxel.KEY_A)) or (pyxel.btn(pyxel.KEY_S)) or (pyxel.btn(
                pyxel.KEY_D)) or (pyxel.btn(
                pyxel.KEY_W)):
            self.animation_frame = (self.animation_frame + 1) % (
                self.animation_speed * 6)
        elif self.animation_frame == 0: # Esto es para que no se quede con
            # la boca cerrada.
            self.animation_frame = self.animation_frame + 1
        else:
            self.animation_frame = self.animation_frame








