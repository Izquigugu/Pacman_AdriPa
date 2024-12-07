import pyxel
import time
class PyxelSounds:
    # in frames, 60 frames per second
    HIT_DOT_SOUND_TIMEOUT = 5
    def __init__(self):
        self.hit_dot_sound_framestamp = 0
        pyxel.playm(0, loop=False)  # Loop music by default
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