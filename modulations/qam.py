import numpy as np
from typing import Tuple
from .helpers import BitsInput, _check_array, _padding, _constelate, _gray_code

def m_qam(bits:BitsInput, M:int, Tb:float, fs:float, gray_coding:bool=True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    M-QAM rectangular genérico.

    √M niveles por eje. Cada símbolo usa log2(M) bits.
    Los niveles se generan como:
        nivel = 2*k - (√M - 1)
    y luego se normaliza la potencia.

    :param bits: Bits agrupados en log2(M)
    :type bits: array-like
    :param M: Tamaño de constelación (16, 64, 256, 1024...)
    :type M: int
    :param Tb: Tiempo de símbolo
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float
    :param gray_coding: si True Codifica utilizando gray
    :type gray_coding: bool, opcional
    
    :return: t, I(t), Q(t)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
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

    Tmax = Tb * len(bits)
    t = np.linspace(0, Tmax, int(Tmax*fs), endpoint=False)

    I, Q = _constelate(bits, constelation, int(Tb*fs*bitsXsym))
    return t, I, Q

def qam16(bits:BitsInput, Tb:float, fs:float, gray_coding:bool=True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    16-QAM rectangular (Gray).

    4 bits por símbolo:
        2 bits → nivel I  (±1, ±3)
        2 bits → nivel Q  (±1, ±3)

    Se normaliza dividiendo por sqrt(10).

    :param bits: Secuencia de bits (múltiplo de 4)
    :type bits: array-like
    :param Tb: Tiempo de símbolo
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float
    :param gray_coding: si True Codifica utilizando gray
    :type gray_coding: bool, opcional

    :return: t, I(t), Q(t) normalizados
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """

    return m_qam(bits, 16, Tb, fs, gray_coding)

def qam64(bits:BitsInput, Tb:float, fs:float, gray_coding:bool=True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    64-QAM rectangular.

    6 bits por símbolo:
        3 bits → nivel I (±1, ±3, ±5, ±7)
        3 bits → nivel Q

    Normalización automática para potencia unitaria.

    :param bits: Bits (múltiplo de 6)
    :type bits: array-like
    :param Tb: Tiempo de símbolo
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float
    :param gray_coding: si True Codifica utilizando gray
    :type gray_coding: bool, opcional

    :return: t, I(t), Q(t)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    return m_qam(bits, 64, Tb, fs, gray_coding)

def qam1024(bits:BitsInput, Tb:float, fs:float, gray_coding:bool=True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    1024-QAM (32 niveles por eje).

    10 bits por símbolo:
        5 → nivel I  (±1, ±3, ..., ±31)
        5 → nivel Q

    Normalización automática.

    :param bits: Bits (múltiplo de 10)
    :type bits: array-like
    :param Tb: Tiempo de símbolo
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float
    :param gray_coding: si True Codifica utilizando gray
    :type gray_coding: bool, opcional

    :return: t, I(t), Q(t)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    return m_qam(bits, 1024, Tb, fs, gray_coding)
