'''
analog.py -- Analog modulation utilities.
Provides functions for DSB, DSB-SC, SSB, FM, PM modulation.

All functions use NumPy arrays for maximum compatibility.
'''

import numpy as np
from numpy.typing import ArrayLike
from scipy.signal import hilbert

def DSB(xx : ArrayLike,
        ac : float = 1.0,
        N : int = 1000,  
        fs : float = 1000.0,
        ) -> tuple[np.ndarray, np.ndarray]:
    """
    Double-Sideband modulation with carrier (DSB).

    Parameters
    ----------
    xx : ArrayLike
        Message signal.
    ac : float, optional
        Carrier amplitude (default = 1.0).
    N : int, optional
        Number of samples (default = 1000).
    fs : float, optional
        Sampling frequency in Hz (default = 1000.0).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex envelope of the modulated signal.
    """
    bb = ac + xx       # complex enveloptment
    tt = np.arange(0, N/fs, 1/fs)
    return tt, bb

def DSB_SC(xx : ArrayLike,
           ac : float=1.0,
           N : int = 1000,  
           fs : float = 1000.0,
           ) -> tuple[np.ndarray, np.ndarray]:
    """
    Double-Sideband Suppressed Carrier (DSB-SC).

    Parameters
    ----------
    xx : ArrayLike
        Message signal.
    ac : float, optional
        Amplitude scaling factor (default = 1.0).
    N : int, optional
        Number of samples (default = 1000).
    fs : float, optional
        Sampling frequency in Hz (default = 1000.0).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex envelope of the modulated signal.
    """
    bb = ac * xx      ##In some cases this don't mulpiply by Ac
    tt = np.arange(0, N/fs, 1/fs)
    return tt, bb

def SSB(xx : ArrayLike,
        ac : float = 1.0,
        N : int = 1000,  
        fs : float = 1000.0,
        upper = True) -> tuple[np.ndarray, np.ndarray]:
    """
    Single-Sideband modulation (SSB) using Hilbert transform.

    Parameters
    ----------
    xx : ArrayLike
        Real message signal.
    ac : float, optional
        Amplitude scaling factor (default = 1.0).
    N : int, optional
        Number of samples (default = 1000).
    fs : float, optional
        Sampling frequency in Hz (default = 1000.0).
    upper : bool, optional
        If True, generate upper sideband; if False, lower sideband.

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex envelope of the modulated signal.
    """
    m_hilbert = hilbert(xx)
    if upper:
        bb = xx + 1j * m_hilbert
    else:
        bb = ac* xx - 1j * ac * m_hilbert
    tt = np.arange(0, N/fs, 1/fs)

    return tt, bb

def FM(xx : ArrayLike,
       ac : float = 1.0,
       kf : float = 1,
       N : int = 1000,  
       fs : float = 1000.0,
       ) -> tuple[np.ndarray, np.ndarray]:
    """
    Frequency Modulation (FM).

    Parameters
    ----------
    xx : ArrayLike
        Message signal.
    ac : float, optional
        Carrier amplitude (default = 1.0).
    kf : float, optional
        Frequency deviation constant (default = 1).
    N : int, optional
        Number of samples (default = 1000).
    fs : float, optional
        Sampling frequency in Hz (default = 1000.0).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex envelope of the FM signal.
    """
    integral_mt = np.cumsum(xx) * 1/fs
    tt = np.arange(0, N/fs, 1/fs)

    theta = 2 * np.pi * kf * integral_mt
    bb = ac * np.exp(1j * theta)    # complex enveloptment

    return tt, bb

def PM(xx : ArrayLike,
       ac : float = 1.0,
       kp : float = 1,
       N : int = 1000,  
       fs : float = 1000.0,
       ) -> tuple[np.ndarray, np.ndarray]:
    """
    Phase Modulation (PM).

    Parameters
    ----------
    xx : ArrayLike
        Message signal.
    ac : float, optional
        Carrier amplitude (default = 1.0).
    kp : float, optional
        Phase deviation constant (default = 1).
    N : int, optional
        Number of samples (default = 1000).
    fs : float, optional
        Sampling frequency in Hz (default = 1000.0).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex envelope of the PM signal.
    """
    tt = np.arange(0, N/fs, 1/fs)
    theta = kp * xx
    bb = ac * np.exp(1j * theta)    # complex enveloptment

    return tt, bb
