import numpy as np
from typing import Tuple
from .helpers import BitsInput, _check_array
from .fsk import gfsk

def msk(bits:BitsInput, Tb:float, fs:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    MSK (Minimum Shift Keying) en banda base.

    MSK es un caso particular de modulación CPM (Continuous Phase Modulation):
    - Índice de modulación: h = 1/2
    - Desviación de frecuencia: Δf = 1 / (4·Tb)
    - Fase continua entre símbolos
    - Es equivalente a OQPSK con pulsos medio-sinusoidales

    Implementación:
    - Los bits 0/1 se transforman a símbolos ±1.
    - Cada bit se expande N veces (N = Tb·fs).
    - La frecuencia instantánea vale: f_inst(t) = Δf · s(t)
    - La fase es la integral de la frecuencia:
          φ(t) = ∫ 2π f_inst(t) dt
    - Salida compleja en banda base:
          I(t) = cos(φ(t))
          Q(t) = sin(φ(t))

    :param bits: Secuencia de bits (0/1)
    :type bits: BitsInput
    :param Tb: Duración del bit
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

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

    df = 1/(4*Tb)

    s_expanded = np.repeat(symbols, N)

    f_inst = df * s_expanded

    # Integral
    phase = 2*np.pi * np.cumsum(f_inst) / fs

    I = np.cos(phase)
    Q = np.sin(phase)
    return t, I, Q

def gmsk(bits:BitsInput, Tb:float, fs:float, BT:float=0.3) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    GMSK (Gaussian Minimum Shift Keying) en banda base.

    GMSK es MSK filtrado previamente por un filtro Gaussiano.
    Se implementa como GFSK con:
        - h = 1/2  (igual que MSK)
        - BT ≈ 0.3 (valor típico en GSM)

    Características:
    - Conserva fase continua (CPM)
    - Ancho de banda reducido respecto a MSK
    - Utilizado en GSM y sistemas móviles clásicos

    :param bits: Secuencia de bits 0/1
    :type bits: BitsInput
    :param Tb: Duración del bit
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float
    :param BT: Parámetro del filtro Gaussiano (Bandwidth · Time)
    :type BT: float, opcional

    :return: (t, I, Q)
        - t: Eje temporal
        - I: Componente I(t)
        - Q: Componente Q(t)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    return gfsk(bits, Tb, fs, BT=BT, h=0.5)
