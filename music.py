import pyxel
import time
class PyxelSounds:
    # in frames, 60 frames per second
    HIT_DOT_SOUND_TIMEOUT = 5
    def __init__(self):
        self.hit_dot_sound_framestamp = 0
        self.is_powered_music_playing = False
        pyxel.playm(0, loop = False)

    def update(self, powered):
        if powered:
            # Si está en estado powered
            if not self.is_powered_music_playing:  # Si la música 2 no está sonando
                pyxel.stop()  # Detén todas las músicas
                pyxel.playm(2, loop=True)  # Reproduce música 2 en bucle
                self.is_powered_music_playing = True  # Marca que la música 2 está sonando
        else:
            # Si no está en estado powered
            if self.is_powered_music_playing:
                pyxel.stop()  # Detener música 2
                self.is_powered_music_playing = False  # Restablece la bandera
            if pyxel.play_pos(0) is None and pyxel.play_pos(1) is None:
                # Reproduce música 1 si no hay otra música sonando
                pyxel.playm(1, loop=True)

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