import numpy as np
from numpy.typing import ArrayLike

def parallel(x : ArrayLike) :
    y = None
    for arg in x:
        if y is None:
            y = arg
        else:
            y += 1/arg 
    return 1/y

def rms(xx : ArrayLike, *, axis : int = -1) -> float:
    return np.sqrt(np.mean(xx**2, axis=axis))

def power(xx : ArrayLike, *, axis : int = -1) -> float:
    """
    Compute the average power of a signal.

    The signal power is defined as the mean squared value of the samples.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    axis : int, default=-1
        Axis along which the autocorrelation is computed.
    Returns
    -------
    float
        Average signal power.
    """
    return np.mean(np.abs(xx)**2, axis=axis)

def snr(signal: ArrayLike, noise: ArrayLike, *, axis : int = -1) -> float:
    """
    Compute the signal-to-noise ratio (SNR).

    Parameters
    ----------
    signal : ArrayLike
        Signal component.
    noise : ArrayLike
        Noise component.
    axis : int, default=-1
        Axis along which the autocorrelation is computed.

    Returns
    -------
    float
        Signal-to-noise ratio in decibels (dB).
    """
    return 10 * np.log10(power(signal, axis=axis) / power(noise, axis=axis))

def voltage_db(xx: ArrayLike) -> np.ndarray:
    """
    Compute the magnitude of a quantity in decibels.

    The conversion is defined as
        20 log10(|x|)

    and is typically used for amplitudes or voltage ratios.

    Parameters
    ----------
    xx : ArrayLike
        Input values.

    Returns
    -------
    ndarray
        Magnitude expressed in decibels.
    """
    return 20*np.log10(np.abs(xx))

def power_db(xx: ArrayLike) -> np.ndarray:
    """
    Compute the power of a quantity in decibels.

    The conversion is defined as
        10 log10(|x|)

    and is typically used for power ratios.

    Parameters
    ----------
    xx : ArrayLike
        Input values.

    Returns
    -------
    ndarray
        Power expressed in decibels.
    """
    return 10*np.log10(np.abs(xx))

def get_power(vv_fft : ArrayLike, ii_fft : ArrayLike):
    res = {}

    fases_v = np.angle(vv_fft)
    fases_i = np.angle(ii_fft)
    V_harm_rms = np.abs(vv_fft) / np.sqrt(2)
    I_harm_rms = np.abs(ii_fft) / np.sqrt(2)
    V_harm_rms[0] *= np.sqrt(2) 
    I_harm_rms[0] *= np.sqrt(2)

    V_rms_total = np.sqrt(np.sum(V_harm_rms**2))
    I_rms_total = np.sqrt(np.sum(I_harm_rms**2))

    
    res['S'] = V_rms_total * I_rms_total
    res['P'] = np.sum(V_harm_rms * I_harm_rms * np.cos(fases_v - fases_i))
    res['Q'] = np.sum(V_harm_rms * I_harm_rms * np.sin(fases_v - fases_i))
    D_square = res['S']**2 - res['P']**2 - res['Q']**2
    res['D'] = np.sqrt(max(D_square, 0))
    
    idx_fo = np.argmax(V_harm_rms[1:]) + 1

    irms_0 = I_harm_rms[0]
    irms_1 = I_harm_rms[idx_fo]
    vrms_0 = V_harm_rms[0]
    vrms_1 = V_harm_rms[idx_fo]

    res['THD_V'] = np.sqrt(I_rms_total**2 - irms_0**2 - irms_1**2) / irms_1 if irms_1 != 0 else 1
    res['THD_I'] = np.sqrt(V_rms_total**2 - vrms_0**2 - vrms_1**2) / vrms_1 if vrms_1 != 0 else 1

    return res

def quantizer(xx: ArrayLike, Vfs: float, bits: int = 4) -> np.ndarray:
    """
    Quantize a signal using a uniform ADC model.

    Samples are rounded to the nearest quantization level and clipped to
    the converter input range.

    Parameters
    ----------
    xx : ArrayLike
        Input signal.
    Vfs : float
        Full-scale input voltage.
    bits : int, default=4
        ADC resolution in bits.

    Returns
    -------
    ndarray
        Quantized signal.
    """    
    q = Vfs/(2**bits) 
    xq = np.round(xx/q) * q

    vmax =  q*(2**(bits-1)-1)
    vmin = -q*2**(bits-1)

    np.clip(xq, vmin, vmax, out=xq)
    return xq

