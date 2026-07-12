import numpy as np
from .helpers import BitsInput, _check_array, _padding, _constelate

def m_psk(bits: BitsInput, M: int, tb: float, fs: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Generic M-PSK (Phase Shift Keying) baseband modulation.

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (0/1), grouped in log2(M).
    M : int
        Modulation order (must be a power of 2).
    tb : float
        Symbol duration.
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
    if M < 1:
        raise ValueError("M debe ser mayor o igual a 1")
    bitsXsym = int(np.log2(M))
    if M != 2**bitsXsym:
        raise ValueError("M debe ser potencia de 2")
    bits = _padding(bits, bitsXsym)

    Tmax = tb * len(bits)
    tt = np.linspace(0, Tmax, int(Tmax*fs), endpoint=False)

    # Constelation
    constelation = {}
    for i in range(M):
        b = tuple((i >> k)&1 for k in reversed(range(bitsXsym)))

        theta = 2*np.pi*i/M + np.pi/M
        I_b = np.cos(theta)
        Q_b = np.sin(theta)
        constelation[b] = [I_b, Q_b]

    I, Q = _constelate(bits, constelation, int(tb*fs*bitsXsym))
    bb = I + 1j * Q

    return tt, bb

def bpsk(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Binary PSK (BPSK) baseband modulation.

    Mapping:
        0 → +1
        1 → -1

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
    return m_psk(bits, 2, tb, fs)

def qpsk(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Quadrature PSK (QPSK) baseband modulation with Gray mapping.

    Mapping:
        00 → (+1/√2, +1/√2)
        01 → (-1/√2, +1/√2)
        11 → (-1/√2, -1/√2)
        10 → (+1/√2, -1/√2)

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (length must be even).
    tb : float
        Symbol duration (2 bits per symbol).
    fs : float
        Sampling frequency in Hz.

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal (I + jQ).
    """
    return m_psk(bits, 4, tb, fs)

def psk16(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    16-PSK baseband modulation.

    Each 4-bit symbol is mapped to:
        θ_k = 2π * k / 16

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (multiple of 4).
    tb : float
        Symbol duration.
    fs : float
        Sampling frequency in Hz.

    Returns
    -------
    tt : ndarray
        Time vector.
    bb : ndarray
        Complex baseband signal (I + jQ).
    """
    return m_psk(bits, 16, tb, fs)

def oqpsk(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    Offset QPSK (OQPSK).

    Same as QPSK, but the Q branch is delayed by tb.
    This avoids simultaneous transitions in I and Q,
    eliminating zero crossings.

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (grouped in pairs).
    tb : float
        Symbol duration.
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
    bits = bits.reshape(-1, 2)

    Ts = 2 * tb
    samples_per_sym = int(Ts * fs)
    N_half = samples_per_sym // 2

    Tmax = Ts * len(bits)
    tt = np.linspace(0, Tmax, int(Tmax * fs), endpoint=False)

    mapping = {
        (0,0): (1, 1),
        (0,1): (1,-1),
        (1,1): (-1,-1),
        (1,0): (-1, 1),
    }
    I = np.zeros(len(tt))
    Q = np.zeros(len(tt))

    idx = 0
    for pair in bits:
        b = tuple(pair)
        i_sym, q_sym = mapping[b]

        I[idx:idx+samples_per_sym] = i_sym

        q_start = idx + N_half
        q_end   = q_start + samples_per_sym
        Q[q_start:q_end] = q_sym

        idx += samples_per_sym

    bb = I + 1j * Q
    return tt, bb

def pi4_qpsk(bits : BitsInput, tb : float, fs : float) -> tuple[np.ndarray, np.ndarray]:
    """
    π/4-QPSK modulation.

    Alternates between standard QPSK constellation
    and another rotated by π/4 radians. Provides smoother
    phase transitions, used in mobile systems (e.g., IS-54).

    Parameters
    ----------
    bits : BitsInput
        Input bit sequence (grouped in pairs).
    tb : float
        Symbol duration.
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
    bits = bits.reshape(-1, 2)

    Ts = 2 * tb
    samples_per_sym = int(Ts * fs)

    Tmax = Ts * len(bits)
    tt = np.linspace(0, Tmax, int(Tmax * fs), endpoint=False)

    phase_states = [np.pi/4, 0]   
    state_idx = 0

    phase_map = {
        (0,0):  np.pi/4,
        (0,1):  3*np.pi/4,
        (1,1): -3*np.pi/4,
        (1,0): -1*np.pi/4,
    }

    I = np.zeros(len(tt))
    Q = np.zeros(len(tt))
    idx = 0

    for pair in bits:
        base_phase = phase_map[tuple(pair)]
        phase = base_phase + phase_states[state_idx]

        I_sym = np.cos(phase)
        Q_sym = np.sin(phase)

        I[idx:idx+samples_per_sym] = I_sym
        Q[idx:idx+samples_per_sym] = Q_sym

        idx += samples_per_sym
        state_idx ^= 1   

    bb = I + 1j * Q
    return tt, bb

