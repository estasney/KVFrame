import os
import numpy as np
from itertools import cycle
from kivy.core.audio import SoundLoader


class SoundCycler:

    def __init__(self, folder, alpha=1, beta=1):
        self.files = [os.path.join(folder, f) for f in os.listdir(folder)]
        self.alpha = alpha
        self.beta = beta
        self.filecycler = cycle(self.files)
        self.current_file = next(self.filecycler)
        self.sound = SoundLoader.load(self.current_file)

    def stop(self, *args, **kwargs):
        self.sound.stop()
        cycle_file = np.random.beta(self.alpha, self.beta) > 0.5
        if cycle_file:
            self.current_file = next(self.filecycler)
            self.sound = SoundLoader.load(self.current_file)

    def play(self, *args, **kwargs):
        self.sound.play()
        self.sound.seek(0)



