'''
analog.py -- Analog modulation utilities.
Provides functions for DSB, DSB-SC, SSB, FM, PM modulation.

All functions use NumPy arrays for maximum compatibility.
'''

import numpy as np
from scipy.signal import hilbert
from typing import Tuple

def DSB(t:np.ndarray, x:np.ndarray, fc:float, Ac:float=1.0)->Tuple[np.ndarray, np.ndarray]:
    '''
    Double-Sideband modulation with carrier.

    :param t: Time array in seconds.
    :type t: ndarray
    :param x: Message signal.
    :type x: ndarray
    :param fc: Carrier frequency in Hz.
    :type fc: float
    :param Ac: Carrier amplitude.
    :type Ac: float
    :return: Tuple containing (DSB waveform, complex envelope).
    :rtype: Tuple[ndarray, ndarray]
    '''    
    complex_envelopment = Ac + x
    carrier = np.exp(1j * 2*np.pi*fc*t)

    dsb = np.real(complex_envelopment * carrier)
    return dsb, complex_envelopment

def DSB_SC(t:np.ndarray, x:np.ndarray, fc:float, Ac:float=1.0)->Tuple[np.ndarray, np.ndarray]:
    '''
    Double-Sideband suppressed-carrier (DSB-SC).

    :param t: Time array.
    :type t: ndarray
    :param x: Message signal.
    :type x: ndarray
    :param fc: Carrier frequency.
    :type fc: float
    :param Ac: Amplitude scaling.
    :type Ac: float
    :return: Tuple containing (DSB-SC waveform, complex envelope).
    :rtype: Tuple[ndarray, ndarray]
    '''
    complex_envelopment = Ac * x      ##In some cases this don't mulpiply by Ac
    carrier = np.exp(1j * 2*np.pi*fc*t)

    dsb = np.real(complex_envelopment * carrier)
    return dsb, complex_envelopment

def SSB(t:np.ndarray, x:np.ndarray, fc:float, Ac=1.0, upper= True)->Tuple[np.ndarray, np.ndarray]:
    '''
    Single-Sideband modulation using Hilbert transform.

    :param t: Time array.
    :type t: ndarray
    :param x: Real message signal.
    :type x: ndarray
    :param fc: Carrier frequency.
    :type fc: float
    :param Ac: Amplitude scaling.
    :type Ac: float
    :param upper: Whether to generate upper sideband (True) or lower (False).
    :type upper: bool
    :return: Tuple of (SSB waveform, complex envelope).
    :rtype: Tuple[ndarray, ndarray]
    '''
    m_hilbert = hilbert(x)
    if upper:
        complex_envelopment = x + 1j * m_hilbert
    else:
        complex_envelopment = Ac* x - 1j * Ac * m_hilbert
    carrier = np.exp(1j * 2*np.pi*fc*t)

    ssb = np.real(complex_envelopment * carrier)
    return ssb, complex_envelopment

def FM(t:np.ndarray, x:np.ndarray, fc:float, Ac:float=1.0, Kf:float=1)->Tuple[np.ndarray, np.ndarray]:
    '''
    Frequency Modulation (FM).


    :param t: Time array.
    :type t: ndarray
    :param x: Message signal.
    :type x: ndarray
    :param fc: Carrier frequency.
    :type fc: float
    :param Ac: Carrier amplitude.
    :type Ac: float
    :param Kf: Frequency deviation constant.
    :type Kf: float
    :return: Tuple of (FM waveform, complex envelope).
    :rtype: Tuple[ndarray, ndarray]
    '''
    dt = t[1] - t[0]
    integral_mt = np.cumsum(x) * dt
    theta = 2*np.pi*fc*t + Kf * integral_mt
    complex_envelopment = Ac * np.exp(1j * theta)
    carrier = np.exp(1j * 2*np.pi*fc*t)

    fm = np.real(complex_envelopment * carrier)
    return fm, complex_envelopment

def PM(t:np.ndarray, x:np.ndarray, fc:float, Ac:float=1.0, Kp:float=1)->Tuple[np.ndarray, np.ndarray]:
    '''
    Phase Modulation (PM).
    
    :param t: Time array.
    :type t: ndarray
    :param x: Message signal.
    :type x: ndarray
    :param fc: Carrier frequency.
    :type fc: float
    :param Ac: Carrier amplitude.
    :type Ac: float
    :param Kp: Phase deviation constant.
    :type Kp: float
    :return: Tuple of (PM waveform, complex envelope).
    :rtype: Tuple[ndarray, ndarray]
    '''
    theta = 2*np.pi*fc*t + Kp * x
    complex_envelopment = Ac * np.exp(1j * theta)
    carrier = np.exp(1j * 2*np.pi*fc*t)

    pm = np.real(complex_envelopment * carrier)
    return pm, complex_envelopment
