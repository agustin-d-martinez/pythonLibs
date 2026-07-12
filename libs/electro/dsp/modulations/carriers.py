import numpy as np
from numpy.typing import ArrayLike

def up_carrier(bb : ArrayLike, 
            tt : ArrayLike, 
            fc : float,
            ) -> np.ndarray:
    """
    Upconversion: convert complex baseband to real passband.

    Parameters
    ----------
    bb : ArrayLike
        Complex baseband signal.
    tt : ArrayLike
        Time vector.
    fc : float
        Carrier frequency in Hz.

    Returns
    -------
    rf : ndarray
        Real passband signal.
    """
    tt = np.asarray(tt)
    phase = 2 * np.pi * fc * tt

    return np.real( bb * np.exp(1j * phase) )

def down_carrier(rf : ArrayLike,
                 tt : ArrayLike,
                 fc : float
                 ) -> np.ndarray:
    """
    Downconversion: convert real passband to complex baseband.

    Parameters
    ----------
    rf : ArrayLike
        Real passband signal.
    tt : ArrayLike
        Time vector.
    fc : float
        Carrier frequency in Hz.

    Returns
    -------
    bb : ndarray
        Complex baseband signal.
    """
    tt = np.asarray(tt)
    phase = 2 * np.pi * fc * tt

    return rf * np.exp( -1j * phase )

