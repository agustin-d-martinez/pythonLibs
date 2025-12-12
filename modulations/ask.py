import numpy as np
from typing import Tuple
from .helpers import BitsInput, _check_array, _padding, _constelate


def m_ask(bits: BitsInput, M:int, Tb: float, fs: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    M-ASK (Amplitude Shift Keying) en banda base.

    Modulación por desplazamiento de amplitud con M niveles.
    M debe ser potencia de 2.

    Descripción:
    - Se agrupan log2(M) bits por símbolo.
    - Cada símbolo se asigna a un nivel de amplitud dentro del conjunto:
            levels = 2·k + 1 - M_axis,   con k = 0..M_axis-1
      (niveles simétricos, p.ej. para 4-ASK → amplitudes {-3, -1, +1, +3})
    - Frecuencia de muestreo: fs
    - Duración del símbolo: Ts = Tb·log2(M)
    - Señal en banda base:
            I(t) = A_s   (constante dentro del símbolo)
            Q(t) = 0     (ASK es puramente en fase)

    La salida I/Q es apta para usarse luego con una portadora mediante:
            t, s = carrier(I, Q, t, fc)

    :param bits: Secuencia de bits (0/1)
    :type bits: BitsInput
    :param M: Orden de modulación (potencia de 2)
    :type M: int
    :param Tb: Tiempo de bit
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: (t, I, Q)
        - t: Eje temporal total
        - I: Secuencia en fase (amplitud)
        - Q: Secuencia en cuadratura (todo cero)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    bits = _check_array(bits)
    
    # Check M
    if M < 1:
        raise ValueError("M debe ser mayor o igual a 1")
    bitsXsym = int(np.log2(M))
    if M != 2**bitsXsym:
        raise ValueError("M debe ser potencia de 2")
    bits = _padding(bits, bitsXsym)
        
    Tmax = Tb * len(bits)
    t = np.linspace(0, Tmax, int(Tmax*fs), endpoint=False)

    # Constelation
    levels = 2*np.arange(M) + 1
    constelation = {}
    for i in range(M):
        b = tuple((i >> k)&1 for k in reversed(range(bitsXsym)))
        constelation[b] = [levels[i], 0]

    I, Q = _constelate(bits, constelation, int(Tb*fs*bitsXsym))
    return t, I, Q

def bask(bits, Tb, fs):
    """
    BASK / 2-ASK en banda base.

    Forma particular de M-ASK con M = 2.

        bit 0 → amplitud -1
        bit 1 → amplitud +1

    Señal resultante:
        I(t) = ±1 según bit
        Q(t) = 0

    :param bits: Secuencia de bits
    :param Tb: Tiempo de bit
    :param fs: Frecuencia de muestreo
    """
    return m_ask(bits, 2, Tb, fs)

def ask4(bits, Tb, fs):
    """
    4-ASK en banda base.

    Mapea 2 bits por símbolo a 4 niveles de amplitud:
        00 → -3
        01 → -1
        10 → +1
        11 → +3

    Es equivalente a m_ask(bits, M=4, Tb, fs).
    """
    return m_ask(bits, 4, Tb, fs)

def ask8(bits, Tb, fs):
    """
    8-ASK en banda base.

    Mapea 3 bits por símbolo a 8 niveles de amplitud equiespaciados y simétricos.

    Es equivalente a m_ask(bits, M=8, Tb, fs).
    """
    return m_ask(bits, 8, Tb, fs)

