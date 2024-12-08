import pyxel


class PyxelSounds:
    # Sound timeout in frames (60 frames per second).
    # This value ensures that the "dot eating" sound effect isn't repeatedly played within 5 frames.
    HIT_DOT_SOUND_TIMEOUT = 5

    def __init__(self):
        """
        Initialize the sound system for the game.
        Sets up music states and starts background music.
        """
        # Stores the last frame when the "dot eating" sound was played
        self.hit_dot_sound_framestamp = 0

        # Flag to indicate whether the "powered" music is currently playing
        self.is_powered_music_playing = False

        # Start the initial background music (music track 0)
        pyxel.playm(0, loop=False)

    def update(self, powered):
        """
        Update the music based on the current game state.
        :param powered: Boolean indicating if the powered-up state is active.
        """
        if powered:
            # If Pac-Man (or the player) is in a "powered" state:
            if not self.is_powered_music_playing:
                # If the "powered-up" music is not already playing:

                pyxel.stop()  # Stop any currently playing music or sounds
                pyxel.playm(2,
                            loop=True)  # Play the "powered-up" music (track 2) in a loop

                # Mark that the "powered-up" music is now playing
                self.is_powered_music_playing = True
        else:
            # If not in the "powered" state:
            if self.is_powered_music_playing:
                # If the "powered-up" music was playing, stop it:
                pyxel.stop()  # Stop the powered-up music
                self.is_powered_music_playing = False  # Reset the flag

            # If no background music is playing on track 0 or 1:
            if pyxel.play_pos(0) is None and pyxel.play_pos(1) is None:
                # Play the normal background music (track 1) in a loop
                pyxel.playm(1, loop=True)

    def play_eat_dot_sound(self):
        """
        Play the sound effect when Pac-Man eats a dot, ensuring it doesn't overlap excessively.
        """
        current_frame = pyxel.frame_count  # Get the current frame count

        # Check if the last sound effect was played within the timeout window
        if (
                current_frame - self.hit_dot_sound_framestamp < self.HIT_DOT_SOUND_TIMEOUT):
            return  # If so, do nothing to prevent overlapping sounds

        # Update the last frame when the sound effect was played
        self.hit_dot_sound_framestamp = current_frame

        # Play the dot eating sound effect (sound 1 on channel 3)
        pyxel.play(3, 1)

    def stop_music(self):
        """
        Stop all currently playing music and sounds.
        """
        pyxel.stop()
