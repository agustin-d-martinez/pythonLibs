import numpy as np
from typing import Tuple, List
from .helpers import BitsInput, _check_array, _alternate_x, _NRZ, _RZ

def unipolar_nrz(bits: BitsInput, Tb: float, Fs: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    Unipolar NRZ encoding.

    :param bits: List of bits.
    :type bits: BitsInput
    :param Tb: Bit duration.
    :type Tb: float
    :param Fs: Sampling frequency.
    :type Fs: float

    :return: Time array and encoded signal (I and Q component). (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    '''
    bits = _check_array(bits)
    t, I = _NRZ(bits, Tb, Fs)
    Q = np.zeros_like(I)
    return t, I, Q

def polar_nrz(bits: BitsInput, Tb: float, Fs: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    Polar NRZ encoding.

    :param bits: Bit list.
    :type bits: BitsInput
    :param Tb: Bit duration.
    :type Tb: float
    :param Fs: Sampling frequency.
    :type Fs: float
    :return: Time array and polar NRZ waveform (I and Q component). (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    '''
    bits = _check_array(bits)
    bits = np.where(np.array(bits) == 1, 1.0, -1.0)
    t, I = _NRZ(bits, Tb, Fs)
    Q = np.zeros_like(I)
    return t, I, Q

def bipolar_nrz(bits: BitsInput, Tb: float, Fs: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    Bipolar NRZ encoding.

    :param bits: Bit list.
    :type bits: BitsInput
    :param Tb: Bit duration.
    :type Tb: float
    :param Fs: Sampling frequency.
    :type Fs: float
    :return: Time array and bipolar NRZ waveform (I and Q component). (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    '''
    bits = _check_array(bits)
    bits = _alternate_x(bits, 1)
    t, I = _NRZ(bits, Tb, Fs)
    Q = np.zeros_like(I)
    return t, I, Q

def unipolar_rz(bits: BitsInput, Tb: float, Fs: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    UNIPOLAR RZ encoding.

    :param bits: Bit list.
    :type bits: BitsInput
    :param Tb: Bit duration.
    :type Tb: float
    :param Fs: Sampling frequency.
    :type Fs: float
    :return: Time array and unipolar RZ waveform (I and Q component). (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    '''
    bits = np.array(bits).astype(float)
    t, I = _RZ(bits, Tb, Fs)
    Q = np.zeros_like(I)
    return t, I, Q

def polar_rz(bits: BitsInput, Tb: float, Fs: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    POLAR RZ encoding.

    :param bits: Bit list.
    :type bits: BitsInput
    :param Tb: Bit duration.
    :type Tb: float
    :param Fs: Sampling frequency.
    :type Fs: float
    :return: Time array and polar RZ waveform (I and Q component). (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    '''
    bits = _check_array(bits)
    bits = np.where(np.array(bits) == 1, 1.0, -1.0)
    t, I = _RZ(bits, Tb, Fs)
    Q = np.zeros_like(I)
    return t, I, Q

def bipolar_rz(bits: BitsInput, Tb: float, Fs: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    Bipolar RZ encoding.

    :param bits: Bit list.
    :type bits: BitsInput
    :param Tb: Bit duration.
    :type Tb: float
    :param Fs: Sampling frequency.
    :type Fs: float
    :return: Time array and bipolar RZ waveform (I and Q component). (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    '''
    bits = _check_array(bits)
    bits = _alternate_x(bits, 1)
    t, I = _RZ(bits, Tb, Fs)
    Q = np.zeros_like(I)
    return t, I, Q

def manchester(bits: BitsInput, Tb: float, Fs: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    Manchester line coding.

    :param bits: Bit list or bit string (e.g. "11001").
    :type bits: BitsInput
    :param Tb: Bit duration.
    :type Tb: float
    :param Fs: Sampling frequency.
    :type Fs: float
    :return: Time array and Manchester waveform (I and Q component). (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    '''
    bits = _check_array(bits)

    N = int(Tb * Fs)  # muestras por bit
    half = N // 2
    I = []
    for b in bits:
        I.extend([b] * half + [-b] * (N - half))

    t = np.arange(len(I)) / Fs
    Q = np.zeros_like(I)
    return t, I, Q

def differential_manchester(bits: List[int], Tb: float, Fs: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Differential Manchester encoding.

    Regla:
    - Siempre hay transición en el medio del bit.
    - Un '1' = hay transición al inicio del intervalo.
    - Un '0' = NO hay transición al inicio.

    :param bits: Lista de bits (0/1).
    :param Tb: Duración del bit.
    :param Fs: Frecuencia de muestreo.
    :return: Time array and Differential Manchester waveform (I and Q component). (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    bits_arr = _check_array(bits)
    N = int(Tb * Fs)
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
    I = np.array(I)
    Q = np.zeros_like(I)
    t = np.arange(len(I)) / Fs
    return t, I, Q

def twoB1Q(bits: BitsInput, Tb: float, Fs: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    2B1Q (2 Binary 1 Quaternary) line coding.

    :param bits: Bit list or bit string.
    :type bits: BitsInput
    :param Tb: Bit duration.
    :type Tb: float
    :param Fs: Sampling frequency.
    :type Fs: float
    :return: Time array and 2B1Q waveform.
    :rtype: Tuple[np.ndarray, np.ndarray]
    '''
    bits = _check_array(bits)
    if len(bits) % 2 != 0:
        bits = np.append(bits, 0)

    levels = []
    mapping = {(0, 0): -3, (0, 1): -1, (1, 0): 1, (1, 1): 3}
    levels = [mapping[(bits[i], bits[i+1])] for i in range(0, len(bits), 2)]

    Ts = 2 * Tb
    N = int(Ts * Fs)

    I = np.repeat(levels, N)
    Q = np.zeros_like(I)
    t = np.arange(len(I)) / Fs
    return t, I, Q

