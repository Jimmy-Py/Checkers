from pathlib import Path

import pygame


SOUNDS = {
    "capture": "capture.wav",
    "unselection": "unselect.wav",
    "selection": "select.wav",
    "normal_move": "normal_move.wav",
    "illegal_move": "illegal_move.wav",
}


def sound_path(sound_name):
    return str(Path(__file__).parent.parent / "sounds" / sound_name)


class SoundMachine:
    def __init__(self, initialize_mixer=True, mute=False):
        self.mute = mute
        if initialize_mixer:
            pygame.mixer.init()

        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        for sound_name, sound_file in SOUNDS.items():
            self.sounds[sound_name] = pygame.mixer.Sound(sound_path(sound_file))

    def play(self, sound_name):
        if not self.mute and sound_name in self.sounds:
            pygame.mixer.Sound.play(self.sounds[sound_name])

    def toggle_mute(self):
        self.mute = not self.mute
        return self.mute
