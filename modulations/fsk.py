import numpy as np
from typing import Tuple
from .helpers import BitsInput, _check_array, _padding

def m_fsk(bits:BitsInput, M:int, Tb: float, fs: float, h:float=1.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Modulación M-FSK en banda base generando las señales I/Q.

    Convención:
    - Se generan tonos frecuenciales ortogonales (o casi ortogonales según h).
    - Cada símbolo selecciona una de M frecuencias distintas.
    - Se produce la representación compleja I/Q, aunque la modulación en banda base
      es puramente frecuencial.

    :param bits: Secuencia de bits (0/1). Se adapta a múltiplo de log2(M)
    :type bits: BitsInput
    :param M: Orden de la modulación (2,4,8,...). Debe ser potencia de 2.
    :type M: int
    :param Tb: Duración de un bit
    :type Tb: float
    :param fs: Frecuencia de muestreo en banda base
    :type fs: float
    :param h: Índice de modulación (separación espectral). h=1 produce FSK ortogonal
    :type h: float, opcional

    :return: (t, I, Q)
        - t: Vector de tiempo total
        - I: Componente en fase
        - Q: Componente en cuadratura
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
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
    Ts = bitsXsym * Tb
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
    return t, I, Q

def bfsk(bits:BitsInput, Tb:float, fs:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    BFSK (2-FSK) en banda base.

    Envoltoria compleja equivalente a M-FSK con M=2.

    :param bits: Secuencia de bits 0/1
    :type bits: BitsInput
    :param Tb: Tiempo de bit
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    return m_fsk(bits, 2, Tb, fs)

def fsk4(bits:BitsInput, Tb:float, fs:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    4-FSK en banda base.

    Envuelve M-FSK con M=4.

    :param bits: Bits de entrada (se agrupan de a 2 bits por símbolo)
    :type bits: BitsInput
    :param Tb: Tiempo de bit
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: (t, I, Q)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    return m_fsk(bits, 4, Tb, fs)

def gfsk(bits:BitsInput, Tb:float, fs:float, BT:float=0.3, h:float=1.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Modulación GFSK (Gaussian Frequency Shift Keying) en banda base.

    Implementación CPM:
    - Se convierte la secuencia binaria en símbolos NRZ (+1 / -1).
    - Se aplica un filtro Gaussiano con ancho BT para suavizar transiciones.
    - La señal filtrada controla la frecuencia instantánea.
    - La fase se obtiene integrando la frecuencia.
    - Se devuelve la representación compleja I/Q = cos(φ), sin(φ).

    Parámetros:
    - BT controla el compromiso entre ancho de banda y ISI.
    - h es el índice de modulación (MSK corresponde a h = 0.5).

    :param bits: Lista o arreglo de bits (0/1)
    :type bits: BitsInput
    :param Tb: Duración de un bit
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float
    :param BT: Bandwidth-Time del filtro gaussiano
    :type BT: float, opcional
    :param h: Índice de modulación del CPM
    :type h: float, opcional

    :return: (t, I, Q)
        - t: Eje temporal total
        - I: Componente en fase
        - Q: Componente en cuadratura
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    bits = _check_array(bits)
    symbols = 2*bits - 1

    N = int(Tb * fs)
    Tmax = Tb * len(bits)
    t = np.linspace(0, Tmax, len(bits)*N, endpoint=False)

    # Gaussian Filter
    span = 4  # bits
    L = span * N
    ts = np.linspace(-span/2, span/2, L)
    alpha = np.sqrt(np.log(2)) / (BT * Tb)
    g = np.exp(-(alpha * ts)**2)   
    g /= np.sum(g)  # Normalization

    # Apply Filter
    s_expanded = np.repeat(symbols, N)
    filtered = np.convolve(s_expanded, g, mode='same')

    # Phase
    df = h / (2*Tb)
    f_inst = df * filtered
    phase = 2*np.pi * np.cumsum(f_inst) / fs

    I = np.cos(phase)
    Q = np.sin(phase)

    return t, I, Q

