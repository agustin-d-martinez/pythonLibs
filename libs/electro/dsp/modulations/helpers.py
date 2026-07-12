import numpy as np
from numpy.typing import ArrayLike
from typing import Union

BitsInput = Union[str, list[int], tuple[int, ...], ArrayLike]

def _check_array(bits : BitsInput, min_len : int = 1) -> np.ndarray:
    """
    Validate and normalize input bit sequence.

    Parameters
    ----------
    bits : str | list | tuple | np.ndarray
        Input bit sequence.
    min_len : int, optional
        Minimum required length (default = 1).

    Returns
    -------
    arr : ndarray
        Normalized bit array (dtype=int8).
    """
    if isinstance(bits, str):                       # String
        if not all(c in "01" for c in bits):
            raise ValueError(f"The array must have only 1 or 0.")
        arr = np.fromiter(bits, dtype=np.int8)

    else:
        try:
            arr = np.asarray(bits, dtype=np.int8)
        except Exception:
            raise ValueError(f"The array must be a bit sequence (1 or 0).")

    if arr.ndim != 1:
        raise ValueError(f"The array must be unidimensional.")
    if not np.all((arr == 0) | (arr == 1)):
        raise ValueError(f"The array must have only 1 or 0.")
    if len(arr) < min_len:
        raise ValueError(f"The array must have at least {min_len} bits.")

    return arr

def _alternate_x(arr : ArrayLike, value : int) -> np.ndarray:
    """
    Alternate polarity for a given value in an array.

    Parameters
    ----------
    arr : ArrayLike
        Input array.
    value : int
        Value to alternate.

    Returns
    -------
    out : ndarray
        Array with alternating polarity applied.
    """
    out = arr.copy().astype(float)
    polarity = 1
    for i, val in enumerate(arr):
        if val == value:
            out[i] = value * polarity
            polarity = -polarity
    return out

def _NRZ(bits : ArrayLike, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate NRZ (Non-Return-to-Zero) waveform.

    Parameters
    ----------
    bits : ArrayLike
        Input bit sequence.
    tb : float
        Bit duration.
    fs : float
        Sampling frequency.

    Returns
    -------
    t : ndarray
        Time vector.
    signal : ndarray
        NRZ waveform.
    """
    N = int(tb * fs)                            # muestras por bit
    signal = np.repeat([b for b in bits], N)
    t = np.arange(len(signal)) / fs
    return t, signal

def _RZ(bits: ArrayLike, tb: float, fs: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate RZ (Return-to-Zero) waveform.

    Parameters
    ----------
    bits : ArrayLike
        Input bit sequence.
    tb : float
        Bit duration.
    fs : float
        Sampling frequency.

    Returns
    -------
    t : ndarray
        Time vector.
    signal : ndarray
        RZ waveform.
    """
    N = int(tb * fs)                            # muestras por bit
    half = N // 2
    signal = []
    for b in bits:
        signal.extend([b] * half + [0] * (N - half))
    t = np.arange(len(signal)) / fs
    return t, signal

def _constelate(bits : ArrayLike, 
                constelation : dict[tuple[int, ...], tuple[float, float]], 
                samples_per_symbol : int
                ) -> tuple[np.ndarray, np.ndarray]:
    """
    Map bit sequence to I/Q constellation.

    Parameters
    ----------
    bits : ArrayLike
        Input bit sequence.
    constelation : dict
        Mapping from bit tuples to (I, Q) coordinates.
    samples_per_symbol : int
        Number of samples per symbol.

    Returns
    -------
    I : ndarray
        In-phase component.
    Q : ndarray
        Quadrature component.
    """
    bitsXsym = len(next(iter(constelation.keys())))
    cant_sym = len(bits)//bitsXsym

    I = np.empty(cant_sym, dtype=float)
    Q = np.empty(cant_sym, dtype=float)
    for i in range(cant_sym):
        symbol = tuple(bits[i*bitsXsym:i*bitsXsym+bitsXsym])
        if symbol not in constelation:
            raise ValueError(f'simbolo {symbol} no esta en la constelacion.')
        I[i], Q[i] = constelation[symbol]
    
    I = np.kron(I, np.ones(samples_per_symbol))
    Q = np.kron(Q, np.ones(samples_per_symbol))

    return I, Q

def _padding(bits : ArrayLike, multiple : int, add : int = 0 ) -> np.ndarray:
    """
    Pad bit sequence to a required multiple.

    Parameters
    ----------
    bits : ArrayLike
        Input bit sequence.
    multiple : int
        Required multiple length.
    add : int, optional
        Value used for padding (default = 0).

    Returns
    -------
    arr : ndarray
        Bit sequence padded to the required multiple.
    """
    extra = (-len(bits))%multiple
    if extra == 0:
        return bits
    pad = np.full(extra,add,dtype=int)
    return np.concatenate([bits, pad])

def _gray_code(n : int) -> int:
    """
    Compute Gray code of an integer.

    Parameters
    ----------
    n : int
        Input integer.

    Returns
    -------
    g : int
        Gray code of the input integer.
    """
    return n ^ (n >> 1)
