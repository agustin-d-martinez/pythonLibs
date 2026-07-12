import numpy as np
from .helpers import BitsInput, _check_array
from .fsk import gfsk

def msk(bits : BitsInput,
        tb : float,
        fs : float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    MSK (Minimum Shift Keying) baseband modulation.

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (0/1).
    tb : float
        Bit duration.
    fs : float
        Sampling frequency in Hz.

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal (I + jQ).
    """
    bits = _check_array(bits)
    symbols = 2*bits - 1

    N = int(tb * fs)
    Tmax = tb * len(bits)
    t = np.linspace(0, Tmax, len(bits)*N, endpoint=False)

    df = 1/(4*tb)

    s_expanded = np.repeat(symbols, N)

    f_inst = df * s_expanded

    # Integral
    phase = 2*np.pi * np.cumsum(f_inst) / fs

    I = np.cos(phase)
    Q = np.sin(phase)
    bb = I + 1j*Q
    return t, bb

def gmsk(bits : BitsInput,
         tb : float,
         fs : float, 
         BT : float = 0.3) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    GMSK (Gaussian Minimum Shift Keying) baseband modulation.

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (0/1).
    tb : float
        Bit duration.
    fs : float
        Sampling frequency in Hz.
    BT : float, optional
        Gaussian filter bandwidth-time product (default = 0.3).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal (I + jQ).
    """
    return gfsk(bits, tb, fs, BT=BT, h=0.5)
