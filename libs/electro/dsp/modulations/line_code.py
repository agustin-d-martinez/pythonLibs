import numpy as np
from .helpers import BitsInput, _check_array, _alternate_x, _NRZ, _RZ

def unipolar_nrz(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Unipolar NRZ line coding.

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
    signal : ndarray
        Encoded Unipolar NRZ waveform.
    """
    bits = _check_array(bits)
    tt, signal = _NRZ(bits, tb, fs)

    return tt, signal

def polar_nrz(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Polar NRZ line coding.

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
    signal : ndarray
        Encoded Polar NRZ waveform.
    """
    bits = _check_array(bits)
    bits = np.where(np.array(bits) == 1, 1.0, -1.0)
    tt, signal = _NRZ(bits, tb, fs)

    return tt, signal

def bipolar_nrz(bits: BitsInput, tb: float, fs: float)-> tuple[np.ndarray, np.ndarray]:
    """
    Bipolar NRZ line coding.

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
    signal : ndarray
        Encoded Bipolar NRZ waveform.
    """
    bits = _check_array(bits)
    bits = _alternate_x(bits, 1)
    tt, signal = _NRZ(bits, tb, fs)

    return tt, signal

def unipolar_rz(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Unipolar RZ line coding.

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
    signal : ndarray
        Encoded Unipolar RZ waveform.
    """
    bits = np.array(bits).astype(float)
    tt, signal = _RZ(bits, tb, fs)

    return tt, signal

def polar_rz(bits: BitsInput, tb: float, fs: float)-> tuple[np.ndarray, np.ndarray]:
    """
    Polar RZ line coding.

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
    signal : ndarray
        Encoded Polar RZ waveform.
    """
    bits = _check_array(bits)
    bits = np.where(np.array(bits) == 1, 1.0, -1.0)
    tt, signal = _RZ(bits, tb, fs)

    return tt, signal

def bipolar_rz(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Bipolar RZ line coding.

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
    signal : ndarray
        Encoded Bipolar RZ waveform.
    """
    bits = _check_array(bits)
    bits = _alternate_x(bits, 1)
    tt, signal = _RZ(bits, tb, fs)

    return tt, signal

def manchester(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Manchester line coding.

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
    signal : ndarray
        Encoded Manchester waveform.
    """
    bits = _check_array(bits)

    N = int(tb * fs)  # muestras por bit
    half = N // 2
    I = []
    for b in bits:
        I.extend([b] * half + [-b] * (N - half))

    tt = np.arange(len(I)) / fs
    signal = np.array(I)

    return tt, signal

def differential_manchester(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Differential Manchester line coding.

    Rules:
    - Always a transition in the middle of the bit.
    - '1' = transition at the beginning of the interval.
    - '0' = no transition at the beginning.

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
    signal : ndarray
        Encoded Differential Manchester waveform.
    """
    bits_arr = _check_array(bits)
    N = int(tb * fs)
    half = N // 2

    current = 1.0
    I = []
    for b in bits_arr:
        if b == 1:
            current = -current

        first = current
        second = -current
        I.extend([first] * half + [second] * (N - half))
        current = second
    signal = np.array(I)

    tt = np.arange(len(I)) / fs

    return tt, signal

def twoB1Q(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    2B1Q (2 Binary 1 Quaternary) line coding.

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
    signal : ndarray
        Encoded 2B1Q waveform.
    """
    bits = _check_array(bits)
    if len(bits) % 2 != 0:
        bits = np.append(bits, 0)

    levels = []
    mapping = {(0, 0): -3, (0, 1): -1, (1, 0): 1, (1, 1): 3}
    levels = [mapping[(bits[i], bits[i+1])] for i in range(0, len(bits), 2)]

    Ts = 2 * tb
    N = int(Ts * fs)

    signal = np.repeat(levels, N)

    tt = np.arange(len(signal)) / fs
    
    return tt, signal

