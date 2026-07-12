import numpy as np
from .helpers import BitsInput, _check_array, _padding, _constelate


def m_ask(bits : BitsInput,
          M : int,
          tb : float,
          fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    M-ASK (Amplitude Shift Keying) baseband modulation.

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (0/1).
    M : int
        Modulation order (must be a power of 2).
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
    
    # Check M
    if M < 2:
        raise ValueError("M must be grater or equal to 2")
    bitsXsym = int(np.log2(M))
    if M != 2**bitsXsym:
        raise ValueError("M must be power of 2")
    bits = _padding(bits, bitsXsym)
        
    Tmax = tb * len(bits)
    tt = np.arange(0, tb * len(bits), 1/fs)

    # Constelation
    levels = 2*np.arange(M) + 1
    constelation = {}
    for i in range(M):
        b = tuple((i >> k)&1 for k in reversed(range(bitsXsym)))
        constelation[b] = [levels[i], 0]

    I, Q = _constelate(bits, constelation, int(tb*fs*bitsXsym))
    bb = I + 1j*Q
    return tt, bb

def bask(bits : BitsInput,
         tb : float,
         fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Binary ASK (BASK, equivalent to 2-ASK).

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
    return m_ask(bits, 2, tb, fs)

def ask4(bits : BitsInput,
         tb : float,
         fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    4-ASK baseband modulation.

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
    return m_ask(bits, 4, tb, fs)

def ask8(bits : BitsInput,
         tb : float,
         fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    8-ASK baseband modulation.

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
    return m_ask(bits, 8, tb, fs)

def ook(bits : BitsInput,
        tb : float,
        fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    On-Off Keying (OOK) baseband modulation.

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
            
    Tmax = tb * len(bits)
    tt = np.arange(0, tb * len(bits), 1/fs)

    # Constelation
    levels = 2
    constelation = {
        (0,): (0.0, 0.0),
        (1,): (1.0, 0.0),
    }
    I, Q = _constelate(bits, constelation, int(tb*fs))
    bb = I + 1j*Q
    return tt, bb
