import numpy as np

import scipy.signal as sig

from typing import Literal, Callable

WindowType = Literal[
    "rectangular",
    "flattop",
    "hann",
    "hamming",
    "blackman",
    "blackman-harris",
]

WindowFunct = Callable[[int], np.ndarray]

WINDOWS_FUNCT_DICT: dict[WindowType, WindowFunct] = {
    "rectangular": lambda nn: np.ones(nn),
    "flattop": lambda nn: sig.windows.flattop(nn),
    "hann": lambda nn: sig.windows.hann(nn),
    "hamming": lambda nn: np.hamming(nn),
    "blackman": lambda nn: sig.windows.blackman(nn),
    "blackman-harris": lambda nn: sig.windows.blackmanharris(nn),
}

