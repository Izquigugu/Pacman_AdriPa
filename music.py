import pyxel
import time
class PyxelSounds:
    # in frames, 60 frames per second
    HIT_DOT_SOUND_TIMEOUT = 5
    def __init__(self):
        self.hit_dot_sound_framestamp = 0
        pyxel.playm(0, loop = False)

    def update(self, powered):
        #if pyxel.play_pos(0) is None:
            #pyxel.playm(1, loop = True)
        """if powered:
            # Si está en estado powered, detener otras músicas y reproducir música 2
            if pyxel.play_pos(2) is None:  # Verifica si la música 2 no está sonando
                pyxel.stop()  # Detén todas las músicas
                pyxel.playm(2, loop = True)  # Reproduce música 2 en bucle"""
        if not powered:
            # Si no está en estado powered
            if (pyxel.play_pos(0) is None and pyxel.play_pos(1) is None and
                    pyxel.play_pos(2) is None):
                # Si la música 0 y la 1 no están sonando y la música 2
                # tampoco,
                # reproducir música 1
                pyxel.playm(1, loop=True)
            if pyxel.play_pos(2) is not None:
                # Detener música 2 si está sonando y no estamos en estado powered
                pyxel.stop(2)

    # Todavía no lo he puesto porque suena muy mal, no sé cómo hacerlo
    def play_eat_dot_sound(self):
        current_frame = pyxel.frame_count
        if (current_frame - self.hit_dot_sound_framestamp <
                self.HIT_DOT_SOUND_TIMEOUT):
            return
        self.hit_dot_sound_framestamp = current_frame
        pyxel.play(3, 1)  # Play a sound effect (channel 0, sound 0)
    def stop_music(self):
        pyxel.stop()  # Stop all playing music and sounds