import numpy as np
from typing import Tuple
from .helpers import BitsInput, _check_array, _padding, _constelate

def m_psk(bits: BitsInput, M:int, Tb: float, fs: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    M-PSK genérico.

    Toma grupos de log2(M) bits.
    Para símbolo k:
        θ_k = 2π * k / M

    :param bits: Bits en grupos de log2(M)
    :type bits: array-like
    :param M: Orden de la modulación (ej: 8, 16, 32...)
    :type M: int
    :param Tb: Tiempo de símbolo
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: t, I(t), Q(t)
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
    constelation = {}
    for i in range(M):
        b = tuple((i >> k)&1 for k in reversed(range(bitsXsym)))

        theta = 2*np.pi*i/M + np.pi/M
        I_b = np.cos(theta)
        Q_b = np.sin(theta)
        constelation[b] = [I_b, Q_b]

    I, Q = _constelate(bits, constelation, int(Tb*fs*bitsXsym))
    return t, I, Q

def bpsk(bits:BitsInput, Tb:float, fs:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    BPSK en banda base.

    Mapea cada bit según:
        0 → +1
        1 → -1

    I(t) contiene la señal modulada (±1),
    Q(t) es siempre cero.

    :param bits: Secuencia de bits 0/1
    :type bits: array-like
    :param Tb: Tiempo de bit
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: t, I(t), Q(t)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    return m_psk(bits, 2, Tb, fs)

def qpsk(bits:BitsInput, Tb:float, fs:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    QPSK en banda base con mapeo Gray.

    Agrupa los bits de a 2. Constellation:
        00 → ( +1/√2 , +1/√2 )
        01 → ( -1/√2 , +1/√2 )
        11 → ( -1/√2 , -1/√2 )
        10 → ( +1/√2 , -1/√2 )

    :param bits: Secuencia de bits (longitud par)
    :type bits: array-like
    :param Tb: Tiempo por símbolo QPSK (= 2 bits)
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: t, I(t), Q(t)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    return m_psk(bits, 4, Tb, fs)

def psk16(bits:BitsInput, Tb:float, fs:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    16-PSK en banda base.

    Cada símbolo de 4 bits se convierte en un ángulo:
        θ_k = 2π * k / 16

    :param bits: Secuencia de bits (múltiplo de 4)
    :type bits: array-like
    :param Tb: Tiempo de símbolo
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: t, I(t)=cos(θ), Q(t)=sin(θ)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """

    return m_psk(bits, 16, Tb, fs)

def oqpsk(bits, Tb, fs):
    """
    OQPSK (Offset QPSK).

    Igual que QPSK, pero la rama Q se retrasa Tb.
    Esto evita que I y Q cambien simultáneamente y
    elimina los cruces por el origen.

    :param bits: Bits en grupos de a 2
    :type bits: array-like
    :param Tb: Tiempo de símbolo QPSK
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: t, I(t), Q(t) desplazado
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    bits = _check_array(bits)
    bits = bits.reshape(-1, 2)

    Ts = 2 * Tb
    samples_per_sym = int(Ts * fs)
    N_half = samples_per_sym // 2

    Tmax = Ts * len(bits)
    t = np.linspace(0, Tmax, int(Tmax * fs), endpoint=False)

    mapping = {
        (0,0): (1, 1),
        (0,1): (1,-1),
        (1,1): (-1,-1),
        (1,0): (-1, 1),
    }
    I = np.zeros(len(t))
    Q = np.zeros(len(t))

    idx = 0
    for pair in bits:
        b = tuple(pair)
        i_sym, q_sym = mapping[b]

        I[idx:idx+samples_per_sym] = i_sym

        q_start = idx + N_half
        q_end   = q_start + samples_per_sym
        Q[q_start:q_end] = q_sym

        idx += samples_per_sym

    return t, I, Q

def pi4_qpsk(bits:BitsInput, Tb:float, fs:float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    π/4-QPSK.

    Alterna entre la constelación QPSK normal
    y otra rotada π/4 rad. Esto da una señal de fase más continua
    y es usada en sistemas móviles (ej: IS-54).

    :param bits: Bits (en pares)
    :type bits: array-like
    :param Tb: Tiempo de símbolo
    :type Tb: float
    :param fs: Frecuencia de muestreo
    :type fs: float

    :return: t, I(t), Q(t)
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    """
    bits = _check_array(bits)
    bits = bits.reshape(-1, 2)

    Ts = 2 * Tb
    samples_per_sym = int(Ts * fs)

    Tmax = Ts * len(bits)
    t = np.linspace(0, Tmax, int(Tmax * fs), endpoint=False)

    phase_states = [np.pi/4, 0]   
    state_idx = 0

    phase_map = {
        (0,0):  np.pi/4,
        (0,1):  3*np.pi/4,
        (1,1): -3*np.pi/4,
        (1,0): -1*np.pi/4,
    }

    I = np.zeros(len(t))
    Q = np.zeros(len(t))
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

    return t, I, Q

