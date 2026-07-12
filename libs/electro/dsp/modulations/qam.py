import numpy as np
from .helpers import BitsInput, _check_array, _padding, _constelate, _gray_code

def m_qam(bits : BitsInput,
          M : int,
          tb : float,
          fs : float,
          gray_coding : bool = True
          ) -> tuple[np.ndarray, np.ndarray]:
    """
    Generic rectangular M-QAM baseband modulation.

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (grouped in log2(M)).
    M : int
        Constellation size (16, 64, 256, 1024...).
    tb : float
        Symbol duration.
    fs : float
        Sampling frequency in Hz.
    gray_coding : bool, optional
        If True, apply Gray coding (default = True).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal (I + jQ).
    """
    bits = _check_array(bits)

    # Check M
    if M < 1:
        raise ValueError("M debe ser mayor o igual a 1")
    bitsXsym = int(np.log2(M))
    if M != 2**bitsXsym or bitsXsym % 2 != 0:
        raise ValueError("M debe ser potencia de 4")
    bits = _padding(bits, bitsXsym)

    bits_por_eje = bitsXsym // 2
    M_axis = 2**bits_por_eje

    if gray_coding:
        bin_to_gray = [_gray_code(i) for i in range(M_axis)]

    levels = 2*np.arange(M_axis)+1 - M_axis
    constelation = {}
    for i in range(M):  
        b = tuple((i >> k) & 1 for k in reversed(range(bitsXsym)))

        # Convention: MSB -> I, LSB -> Q
        bI = b[:bits_por_eje]
        bQ = b[bits_por_eje:]

        # Array to number (00->0, 10->2, 11->3)
        idxI = int("".join(str(x) for x in bI),2)
        idxQ = int("".join(str(x) for x in bQ),2)

        # Apply Gray mapping
        if gray_coding:
            idxI = bin_to_gray[idxI]
            idxQ = bin_to_gray[idxQ]

        I_b = levels[idxI]
        Q_b = levels[idxQ]
        constelation[b] = (float(I_b), float(Q_b))

    Tmax = tb * len(bits)
    tt = np.linspace(0, Tmax, int(Tmax*fs), endpoint=False)

    I, Q = _constelate(bits, constelation, int(tb*fs*bitsXsym))
    bb = I + 1j * Q
    return tt, bb

def qam16(bits : BitsInput,
          tb : float,
          fs : float,
          gray_coding : bool = True
          ) -> tuple[np.ndarray, np.ndarray]:
    """
    16-QAM baseband modulation (Gray coded).

    Mapping:
        4 bits per symbol:
        - 2 bits → I levels (±1, ±3)
        - 2 bits → Q levels (±1, ±3)

    Normalized by dividing by sqrt(10).

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (multiple of 4).
    tb : float
        Symbol duration.
    fs : float
        Sampling frequency in Hz.
    gray_coding : bool, optional
        If True, apply Gray coding (default = True).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Normalized complex baseband signal (I + jQ).
    """
    return m_qam(bits, 16, tb, fs, gray_coding)

def qam64(bits : BitsInput,
          tb : float,
          fs : float,
          gray_coding : bool = True
          ) -> tuple[np.ndarray, np.ndarray]:
    """
    64-QAM baseband modulation.

    Mapping:
        6 bits per symbol:
        - 3 bits → I levels (±1, ±3, ±5, ±7)
        - 3 bits → Q levels

    Normalized for unit average power.

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (multiple of 6).
    tb : float
        Symbol duration.
    fs : float
        Sampling frequency in Hz.
    gray_coding : bool, optional
        If True, apply Gray coding (default = True).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Normalized complex baseband signal (I + jQ).
    """
    return m_qam(bits, 64, tb, fs, gray_coding)

def qam1024(bits : BitsInput,
            tb : float,
            fs : float,
            gray_coding : bool = True
            ) -> tuple[np.ndarray, np.ndarray]:
    """
    1024-QAM baseband modulation.

    Mapping:
        10 bits per symbol:
        - 5 bits → I levels (±1, ±3, ..., ±31)
        - 5 bits → Q levels

    Normalized for unit average power.

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (multiple of 10).
    tb : float
        Symbol duration.
    fs : float
        Sampling frequency in Hz.
    gray_coding : bool, optional
        If True, apply Gray coding (default = True).

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Normalized complex baseband signal (I + jQ).
    """
    return m_qam(bits, 1024, tb, fs, gray_coding)
