import numpy as np
from .helpers import BitsInput, _check_array, _padding

def m_fsk(bits : BitsInput,
          M : int,
          tb : float,
          fs : float, 
          h : float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """
    M-FSK (Frequency Shift Keying) baseband modulation.

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
    h : float, optional
        Modulation index (default = 1.0). h=1 produces orthogonal FSK.

    Returns
    -------
    t : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal.
    """
    bits = _check_array(bits)

    # Check M
    if M < 1:
        raise ValueError("M debe ser mayor o igual a 1")
    bitsXsym = int(np.log2(M))
    if M != 2**bitsXsym :
        raise ValueError("M debe ser potencia de 2")
    bits = _padding(bits, bitsXsym)

    # Frecuencies
    Ts = bitsXsym * tb
    df = h / Ts
    k = 2 * np.arange(M) + 1 - M
    freqs = k * df 
    symbols = bits.reshape(-1, bitsXsym)
    symbols = np.array([ int("".join(str(x) for x in s), 2) for s in symbols ])     # symbol array

    # Tiempo
    Tmax = Ts * len(symbols)
    t = np.linspace(0, Tmax, int(Tmax * fs), endpoint=False)
   
    samples_per_sym = int(Ts * fs)
    t_sym = np.arange(samples_per_sym) / fs
    I = np.zeros(samples_per_sym * len(symbols))
    Q = np.zeros(len(I))
    for i, sym in enumerate(symbols):
        f = freqs[sym]
        phase = 2*np.pi*f*t_sym

        start = i * samples_per_sym
        end = start + samples_per_sym
        I[start:end] = np.cos(phase) 
        Q[start:end] = np.sin(phase) 
    
    bb = I + 1j*Q
    return t, bb

def bfsk(bits : BitsInput,
         tb : float,
         fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    BFSK (Binary Frequency Shift Keying, M=2).

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
    t : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal.
    """
    return m_fsk(bits, 2, tb, fs)

def fsk4(bits : BitsInput,
         tb : float,
         fs:float) -> tuple[np.ndarray, np.ndarray]:
    """
    4-FSK baseband modulation.

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
    t : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal.
    """
    return m_fsk(bits, 4, tb, fs)

def gfsk(bits : BitsInput,
         tb : float,
         fs : float,
         BT : float = 0.3,
         h : float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """
    GFSK (Gaussian Frequency Shift Keying) baseband modulation.

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
    h : float, optional
        Modulation index (default = 1.0). MSK corresponds to h=0.5.

    Returns
    -------
    t : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal.
    """
    bits = _check_array(bits)
    symbols = 2*bits - 1

    N = int(tb * fs)
    Tmax = tb * len(bits)
    t = np.linspace(0, Tmax, len(bits)*N, endpoint=False)

    # Gaussian Filter
    span = 4  # bits
    L = span * N
    ts = np.linspace(-span/2, span/2, L)
    alpha = np.sqrt(np.log(2)) / (BT * tb)
    g = np.exp(-(alpha * ts)**2)   
    g /= np.sum(g)  # Normalization

    # Apply Filter
    s_expanded = np.repeat(symbols, N)
    filtered = np.convolve(s_expanded, g, mode='same')

    # Phase
    df = h / (2*tb)
    f_inst = df * filtered
    phase = 2*np.pi * np.cumsum(f_inst) / fs

    I = np.cos(phase)
    Q = np.sin(phase)
    bb = I + 1j*Q

    return t, bb

