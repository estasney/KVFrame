import os
import numpy as np
from itertools import cycle
from kivy.core.audio import SoundLoader


class SoundCycler:

    def __init__(self, folder, alpha=1, beta=1):
        self.files = self._find_files(folder)
        self.alpha = alpha
        self.beta = beta
        self.filecycler = cycle(self.files)
        self.current_file = next(self.filecycler)
        self.sound = SoundLoader.load(self.current_file)
        self.sound.loop = True

    def _find_files(self, folder):
        files = []
        for root, _, files in os.walk(folder):
            for file in files:
                files.append(os.path.join(root, file))
        print("\n".join(files))
        return files

    def stop(self, *args, **kwargs):
        self.sound.stop()
        cycle_file = np.random.beta(self.alpha, self.beta) > 0.5
        if cycle_file:
            self.current_file = next(self.filecycler)
            self.sound = SoundLoader.load(self.current_file)
            self.sound.loop = True

    def play(self, *args, **kwargs):
        self.sound.play()
        self.sound.seek(0)



