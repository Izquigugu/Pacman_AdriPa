import pyxel
class PyxelSounds:
    # in frames, 60 frames per second
    HIT_WALL_SOUND_TIMEOUT = 120
    def __init__(self):
        self.hit_wall_sound_framestamp = 0
        pyxel.playm(0, loop=True)  # Loop music by default
    # Todavía no lo he puesto porque suena muy mal, no sé cómo hacerlo
    def play_eat_dot_sound(self):
        current_frame = pyxel.frame_count
        if current_frame - self.hit_wall_sound_framestamp < self.HIT_WALL_SOUND_TIMEOUT:
            return
        self.__hit_wall_sound_framestamp = current_frame
        pyxel.play(1, 1)  # Play a sound effect (channel 0, sound 0)
    def stop_music(self):
        pyxel.stop()  # Stop all playing music and sounds